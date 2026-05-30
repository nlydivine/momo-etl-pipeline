import time
from xml_parser import parse_xml

data = parse_xml()

# FIX: create proper IDs
for i, tx in enumerate(data):
    tx["id"] = str(i)


# build dictionary
transaction_dict = {tx["id"]: tx for tx in data}


# LINEAR SEARCH
def linear_search(target_id):
    for tx in data:
        if tx["id"] == target_id:
            return tx
    return None


# DICTIONARY LOOKUP
def dict_lookup(target_id):
    return transaction_dict.get(target_id)


# PERFORMANCE TEST
def test(target_id):
    print(f"\nSearching ID: {target_id}")

    start = time.time()
    linear_search(target_id)
    t1 = time.time() - start

    start = time.time()
    dict_lookup(target_id)
    t2 = time.time() - start

    print(f"Linear Search: {t1:.6f} sec")
    print(f"Dictionary Lookup: {t2:.6f} sec")


if __name__ == "__main__":
    print(f"Total records: {len(data)}")

    # test multiple IDs
    for i in [0, 1, 2]:
        test(str(i))
