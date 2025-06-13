#!/usr/bin/env python3
"""
Sorts a CSV file containing patent reference data by reference count in descending order.

This script processes a CSV file containing patent information and reference counts,
sorting the entries by the number of references in descending order. The sorted data
is written back to the same file, preserving all original columns and data.
"""

import csv
from pathlib import Path

# Read the input CSV file into memory
input_file = Path("Rice_reference_results.csv")
rows = []

with input_file.open("r", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Sort rows by reference count in descending order
# Convert reference counts to integers for proper numeric sorting
sorted_rows = sorted(rows, key=lambda x: int(x["References Found"]), reverse=True)

# Write the sorted data back to the CSV file
with input_file.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Document/Patent number", "References Found", 
                                         "Title", "Inventor Name(s)", "Publication Date"])
    writer.writeheader()
    writer.writerows(sorted_rows)

print(f"✓ Sorted {len(rows)} patents by reference count in {input_file}")
