import xml.etree.ElementTree as ET

XML_FILE = "modified_sms_v2.xml"


def parse_xml():
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    transactions = []

    # loop through every child node
    for record in root:

        tx = {}

        # CASE 1: normal nested tags
        if len(record) > 0:
            for child in record.iter():
                if child is not record:
                    tx[child.tag] = child.text

        # CASE 2: attributes fallback
        if not tx:
            tx = record.attrib

        # CASE 3: direct text fallback
        if not tx and record.text:
            tx["value"] = record.text

        transactions.append(tx)

    return transactions


if __name__ == "__main__":
    data = parse_xml()
    print("Loaded:", len(data))
    print("Sample:", data[0])
