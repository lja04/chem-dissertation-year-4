'''
This script merges the Wiswesser Line Notation (WLN) results back into the original compound dataset CSV.

Created by: Leo Arogundade
'''

import csv

BASE = "wln_conversion"

original_file = f"{BASE}/input/compound_dataset_1m_cleaned.csv"
wln_file = f"{BASE}/results/final_wln_output.csv"
output_file = f"{BASE}/results/compound_dataset_1m_with_wln.csv"

# Loading WLN results

print("Loading WLN results...")

wln_dict = {}
with open(wln_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 2:
            smiles, wln = row[0], row[1]
            wln_dict[smiles] = wln

print(f"Loaded {len(wln_dict)} WLN mappings.")
print("Starting merge into original CSV...\n")

# Merging WLN into original CSV

with open(original_file, newline="", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["wln_string"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    missing = 0
    written = 0
    total = 0

    for row in reader:
        total += 1
        smiles = row["connectivity_smiles"]

        # Insert WLN or "MISSING"
        wln = wln_dict.get(smiles, "MISSING")
        if wln == "MISSING":
            missing += 1
        else:
            written += 1

        row["wln_string"] = wln
        writer.writerow(row)

        # Print progress every 1000 rows
        if total % 1000 == 0:
            print(f"Processed {total} rows...")

# Final summary

print("\nMerge complete!")
print(f"WLN found for: {written}")
print(f"WLN missing for: {missing}")
print(f"Total rows processed: {total}")
print(f"Output written to: {output_file}")
