import re
import json
import os
import xml.etree.ElementTree as ET


class SMSParser:
    def __init__(self):
        # Regex patterns for each transaction type
        self.patterns = {
            'received': r'you have received (\d+(?:,\d+)*) (\w+) from (.+?) \(\*+(\d+)\) on your mobile money account at ([\d-]+ [\d:]+)\. message from sender:. your new balance:(\d+(?:,\d+)*) (\w+)\. financial transaction id: (\d+)',
            'payment': r'txid: (\d+)\. your payment of ([\d,]+) (\w+) to (.+?) (\w+) has been completed at ([\d-]+ [\d:]+)\. your new balance: ([\d,]+) (\w+)\. fee was 0 (\w+)',
            'transfer': r'\*165\*s\*(\d+(?:,\d+)*) (\w+) transferred to (.+?) \((\d+)\) from (\d+) at ([\d-]+ [\d:]+) \. fee was: (\d+) (\w+)\. new balance: (\d+(?:,\d+)*) (\w+)',
            'bank_transfer': r'you have transferred (\d+(?:,\d+)*) (\w+) to (.+?) \((\d+)\) from your mobile money account (\w+) (.+?) at ([\d-]+ [\d:]+)\. your new balance: (.*?)\. message from sender: (.*?)\. message to receiver: (.*?)\. financial transaction id: (\d+)',
            'bank_deposit': r'\*113\*r\*a bank deposit of (\d+(?:,\d+)*) (\w+) has been added to your mobile money account at ([\d-]+ [\d:]+)\. your new balance :(\d+(?:,\d+)*) (\w+)\. (.*?)\.',
            'airtime': r'\*162\*txid:(\d+)\*s\*your payment of (\d+(?:,\d+)*) (\w+) to airtime with token .* has been completed at ([\d-]+ [\d:]+)\. fee was 0 (\w+)\. your new balance: (\d+(?:,\d+)*) (\w+)',
            'bundle': r'\*162\*txid:(\d+)\*s\*your payment of (\d+(?:,\d+)*) (\w+) to (bundles and packs|bundle) with token .* has been completed at ([\d-]+ [\d:]+)\. fee was 0 (\w+)\. your new balance: (\d+(?:,\d+)*) (\w+)',
            'cash_power': r'\*162\*txid:(\d+)\*s\*your payment of (\d+(?:,\d+)*) (\w+) to mtn cash power with token (.+?) has been completed at ([\d-]+ [\d:]+)\. fee was 0 (\w+)\. your new balance: (\d+(?:,\d+)*) (\w+)',
            'external_transaction': r'\*164\*s\*y\'ello,a transaction of (\d+(?:,\d+)*) (\w+) by (.+?) on your momo account was successfully completed at ([\d-]+ [\d:]+)\. message from debit receiver: (.*?)\. your new balance:(\d+(?:,\d+)*) (\w+)\. fee was 0 (\w+)\. financial transaction id: (\d+)\. external transaction id: (.+?)\.',
            'withdrawal': r'you (.+?) \(\*+(\d+)\) have via agent: (.+?) \((\d+)\), withdrawn (\d+(?:,\d+)*) (\w+) from your mobile money account: (\d+) at ([\d-]+ [\d:]+) .* your new balance: (\d+(?:,\d+)*) (\w+)\. fee paid: (\d+) (\w+)\. message from agent: financial transaction id: (\d+)'
        }
        
        # Category information for each transaction type
        self.categories = {
            'received':             {'category_id': 1,  'category_name': 'Received',         'category_desc': 'Money received from MoMo user or external sender.'},
            'payment':              {'category_id': 2,  'category_name': 'Payment', 'category_desc': 'Payment made to a registered merchant code.'},
            'transfer':             {'category_id': 3,  'category_name': 'Transfer to Mobile Money',     'category_desc': 'Money transferred to another mobile money account.'},
            'bank_transfer':        {'category_id': 4,  'category_name': 'Bank Transfer',          'category_desc': 'Money transferred from MoMo to a bank account.'},
            'bank_deposit':         {'category_id': 5,  'category_name': 'Bank Deposit',           'category_desc': 'Money deposited from a bank into a MoMo account.'},
            'airtime':              {'category_id': 6,  'category_name': 'Airtime Purchase',       'category_desc': 'Airtime bought from MoMo balance.'},
            'bundle':               {'category_id': 7,  'category_name': 'Data Bundle Purchase',   'category_desc': 'Voice or data bundle bought from MoMo balance.'},
            'cash_power':           {'category_id': 8,  'category_name': 'Cash Power',             'category_desc': 'Electricity tokens purchased through MoMo.'},
            'external_transaction': {'category_id': 9,  'category_name': 'External Transaction',   'category_desc': 'Third-party transaction processed through the MoMo account.'},
            'withdrawal':           {'category_id': 10, 'category_name': 'Withdrawal',             'category_desc': 'Cash withdrawn from MoMo via an agent.'},
        }
        
        # Catching duplicate phone numbers for userid
        self.seen_users = {}
        self.next_user_id = 1
    
    def clean_amount(self, amount_str):
        return float(amount_str.replace(',', ''))
    
    # Returns the user object, reusing user_id if it is a duplicate phone number
    def create_user(self, name, phone):
        if phone in self.seen_users:
            return self.seen_users[phone]
        user = {
            'user_id': self.next_user_id,
            'user_names': name.strip(),
            'phone_number': phone
        }
        self.seen_users[phone] = user
        self.next_user_id += 1
        return user
    
    # Categorize message type based on keywords
    def categorize(self, body):
        if 'received' in body:
            return 'received'
        elif 'transferred' in body and 'financial transaction id' in body:
            return 'bank_transfer'
        elif 'transferred' in body:
            return 'transfer'
        elif 'bundle' in body:
            return 'bundle'
        elif 'cash power' in body:
            return 'cash_power'
        elif 'airtime' in body:
            return 'airtime'
        elif ('external transaction' in body or 'external transaction id' in body) and 'bundle' not in body and 'payment' not in body:
            return 'external_transaction'
        elif 'bank deposit' in body:
            return 'bank_deposit'
        elif 'payment' in body and 'external transaction' not in body:
            return 'payment'
        elif 'withdrawn' in body:
            return 'withdrawal'
        else:
            return None
    
    # Parsing methods for each transaction category
    def parse_received(self, match):
        return {
            'amount': self.clean_amount(match.group(1)),
            'currency': match.group(2).upper(),
            'transaction_date': match.group(5),
            'reference_code': match.group(8),
            'new_balance': self.clean_amount(match.group(6)),
            'parties': [
                {'party_role': 'sender', 'user': self.create_user(match.group(3), match.group(4))}
            ]
        }
    
    def parse_payment(self, match):
        return {
            'amount': self.clean_amount(match.group(2)),
            'currency': match.group(3).upper(),
            'transaction_date': match.group(6),
            'reference_code': match.group(1),
            'new_balance': self.clean_amount(match.group(7)),
            'parties': [
                {'party_role': 'recipient', 'user': self.create_user(match.group(4), match.group(5))}
            ]
        }
    
    def parse_transfer(self, match):
        return {
            'amount': self.clean_amount(match.group(1)),
            'currency': match.group(2).upper(),
            'transaction_date': match.group(6),
            'reference_code': None,
            'fee': float(match.group(7)),
            'new_balance': self.clean_amount(match.group(9)),
            'sender_account': match.group(5),
            'parties': [
                {'party_role': 'recipient', 'user': self.create_user(match.group(3), match.group(4))}
            ]
        }
    
    def parse_bank_transfer(self, match):
        return {
            'amount': self.clean_amount(match.group(1)),
            'currency': match.group(2).upper(),
            'transaction_date': match.group(7),
            'reference_code': match.group(11),
            'bank': match.group(6).strip(),
            'sender_account': match.group(5),
            'parties': [
                {'party_role': 'recipient', 'user': self.create_user(match.group(3), match.group(4))}
            ]
        }
    
    def parse_bank_deposit(self, match):
        return {
            'amount': self.clean_amount(match.group(1)),
            'currency': match.group(2).upper(),
            'transaction_date': match.group(3),
            'reference_code': None,
            'new_balance': self.clean_amount(match.group(4)),
            'deposit_reference': match.group(6).strip(),
            'parties': []
        }
    
    def parse_airtime(self, match):
        return {
            'amount': self.clean_amount(match.group(2)),
            'currency': match.group(3).upper(),
            'transaction_date': match.group(4),
            'reference_code': match.group(1),
            'new_balance': self.clean_amount(match.group(6)),
            'parties': []
        }
    
    def parse_bundle(self, match):
        return {
            'amount': self.clean_amount(match.group(2)),
            'currency': match.group(3).upper(),
            'transaction_date': match.group(5),
            'reference_code': match.group(1),
            'new_balance': self.clean_amount(match.group(7)),
            'service': match.group(4),
            'parties': []
        }
    
    def parse_cash_power(self, match):
        return {
            'amount': self.clean_amount(match.group(2)),
            'currency': match.group(3).upper(),
            'transaction_date': match.group(5),
            'reference_code': match.group(1),
            'new_balance': self.clean_amount(match.group(7)),
            'token': match.group(4).strip(),
            'parties': []
        }
    
    def parse_external_transaction(self, match):
        return {
            'amount': self.clean_amount(match.group(1)),
            'currency': match.group(2).upper(),
            'transaction_date': match.group(4),
            'reference_code': match.group(9),
            'external_transaction_id': match.group(10).strip(),
            'new_balance': self.clean_amount(match.group(6)),
            'parties': [
                {'party_role': 'merchant', 'user': self.create_user(match.group(3), match.group(3).strip())}
            ]
        }
    
    def parse_withdrawal(self, match):
        return {
            'amount': self.clean_amount(match.group(5)),
            'currency': match.group(6).upper(),
            'transaction_date': match.group(8),
            'reference_code': match.group(13),
            'fee': float(match.group(11)),
            'new_balance': self.clean_amount(match.group(9)),
            'account': match.group(7),
            'parties': [
                {'party_role': 'customer', 'user': self.create_user(match.group(1), match.group(2))},
                {'party_role': 'agent', 'user': self.create_user(match.group(3), match.group(4))}
            ]
        }
    
    # Parsing the XML file
    def parse_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        all_sms = root.findall('sms')
        
        parsed_data = []
        uncategorized = []
        unparsed = []
        transactions_id = 1
        
        for sms in all_sms:
            body = sms.get('body', '').lower()
            if not body:
                continue
            
            # Categorizing the message
            transaction_type = self.categorize(body)
            if transaction_type is None:
                uncategorized.append({'body': body})
                continue
            
            # Extracting fields with regex
            pattern = self.patterns[transaction_type]
            match = re.search(pattern, body, re.IGNORECASE)
            if not match:
                unparsed.append({'body': body, 'type': transaction_type})
                continue
            
            # Calling the right parsing method
            parser_method = getattr(self, f'parse_{transaction_type}')
            data = parser_method(match)
            
            data['transactions_id'] = transactions_id
            data['transaction_status'] = 'completed'
            data['sms_raw_text'] = body
            data['category'] = self.categories[transaction_type]
            
            parsed_data.append(data)
            transactions_id += 1
        
        return parsed_data, uncategorized, unparsed
    
    # Dump to JSON files
    def write_output(self, parsed_data, uncategorized, unparsed, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(os.path.join(output_dir, 'transactions.json'), 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2)
        
        # Debug for messages that failed to parse cleanly
        if uncategorized:
            with open(os.path.join(output_dir, 'uncategorized.json'), 'w', encoding='utf-8') as f:
                json.dump(uncategorized, f, indent=2)
        
        if unparsed:
            with open(os.path.join(output_dir, 'unparsed.json'), 'w', encoding='utf-8') as f:
                json.dump(unparsed, f, indent=2)


if __name__ == "__main__":
    parser = SMSParser()
    
    xml_file = 'modified_sms_v2.xml'
    output_dir = 'output'
    
    parsed_data, uncategorized, unparsed = parser.parse_xml(xml_file)
    parser.write_output(parsed_data, uncategorized, unparsed, output_dir)
    
    # Print a quick summary
    print(f"Total parsed: {len(parsed_data)}")
    print(f"Users: {len(parser.seen_users)}")
    print(f"Uncategorized: {len(uncategorized)}")
    print(f"Failed to parse: {len(unparsed)}")
    print(f"Output saved to {output_dir}/transactions.json")