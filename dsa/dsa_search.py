import json
import time
import random
import os


def load_transactions(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def linear_search(transactions, target_id):
    for record in transactions:
        if record["transactions_id"] == target_id:
            return record
    return None


def build_dict(transactions):
    return {record["transactions_id"]: record for record in transactions}


def dict_lookup(lookup_dict, target_id):
    return lookup_dict.get(target_id, None)


def benchmark(transactions, lookup_dict, sample_size=25, runs=10_000):
    all_ids = [r["transactions_id"] for r in transactions]
    sample_ids = random.sample(all_ids, min(sample_size, len(all_ids)))

    print(f"\n{'='*65}")
    print(f"  DSA SEARCH COMPARISON")
    print(f"  Total records: {len(transactions)}  |  Sample: {sample_size} IDs  |  Runs: {runs:,}")
    print(f"{'='*65}")
    print(f"  {'ID':<8} {'Linear Search (us)':>20} {'Dict Lookup (us)':>18} {'Speedup':>10}")
    print(f"{'─'*65}")

    total_linear = 0
    total_dict = 0

    for tid in sample_ids:
        t0 = time.perf_counter()
        for _ in range(runs):
            linear_search(transactions, tid)
        t1 = time.perf_counter()
        avg_linear = (t1 - t0) / runs * 1_000_000

        t0 = time.perf_counter()
        for _ in range(runs):
            dict_lookup(lookup_dict, tid)
        t1 = time.perf_counter()
        avg_dict = (t1 - t0) / runs * 1_000_000

        speedup = avg_linear / avg_dict if avg_dict > 0 else 0
        print(f"  {tid:<8} {avg_linear:>20.4f} {avg_dict:>18.4f} {speedup:>9.1f}x")

        total_linear += avg_linear
        total_dict += avg_dict

    avg_l = total_linear / sample_size
    avg_d = total_dict / sample_size
    overall = avg_l / avg_d if avg_d > 0 else 0

    print(f"{'─'*65}")
    print(f"  {'AVERAGE':<8} {avg_l:>20.4f} {avg_d:>18.4f} {overall:>9.1f}x")
    print(f"{'='*65}\n")

    return avg_l, avg_d, overall


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base, "output", "transactions.json")

    transactions = load_transactions(json_path)
    print(f"Loaded {len(transactions)} transactions.")

    lookup_dict = build_dict(transactions)

    benchmark(transactions, lookup_dict, sample_size=25, runs=10_000)

    summary = {
        "total_records": len(transactions),
        "sample_size": 25,
        "runs_per_id": 10_000,
    }

    out_path = os.path.join(base, "output", "dsa_results.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Results saved to: {out_path}")

