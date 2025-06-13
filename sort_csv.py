#!/usr/bin/env python3
"""Sort Rice_reference_results.csv by References Found in descending order."""

import csv
from pathlib import Path

# Read the input CSV file
input_file = Path("Rice_reference_results.csv")
rows = []

with input_file.open("r", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Sort rows by References Found in descending order
# Convert References Found to int for proper numeric sorting
sorted_rows = sorted(rows, key=lambda x: int(x["References Found"]), reverse=True)

# Write the sorted data back to the CSV
with input_file.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Document/Patent number", "References Found", 
                                         "Title", "Inventor Name(s)", "Publication Date"])
    writer.writeheader()
    writer.writerows(sorted_rows)

print(f"✓ Sorted {len(rows)} patents by reference count in {input_file}")
