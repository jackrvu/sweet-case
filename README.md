# USPTO Patent Reference Counter

A suite of Python scripts for retrieving and analyzing patent reference data from the USPTO PubWEST database. These scripts automate the process of collecting patent information and their reference counts for a specified company.

## Overview

The system consists of three main scripts that work together:

1. `download_patents.py`: Downloads basic patent information for a company
2. `reference_number_commas.py` or `reference_number_flat.py`: Retrieves reference counts for the patents
3. `sort_csv.py`: Sorts the results by reference count

## Prerequisites

- Python 3.x
- Google Chrome browser
- Required Python packages (install via `pip install -r requirements.txt`):
  - selenium
  - beautifulsoup4
  - pandas
  - webdriver-manager

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.\.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The process involves three steps:

1. **Download Patent Information**
   ```bash
   python download_patents.py "Company Name"
   ```
   This creates a CSV file named `{company_name}_patents.csv` containing:
   - Patent numbers
   - Titles
   - Inventor names
   - Publication dates
   - Initial reference counts

2. **Get Reference Counts**
   Choose either script based on your needs:
   ```bash
   # For comma-formatted patent numbers
   python reference_number_commas.py "Company Name"
   
   # For flat (unformatted) patent numbers
   python reference_number_flat.py "Company Name"
   ```
   This creates `{company_name}_reference_results.csv` with updated reference counts.

3. **Sort Results** (Optional)
   ```bash
   python sort_csv.py
   ```
   This sorts the reference results by patent number in descending order.

## Output Files

- `{company_name}_patents.csv`: Initial patent data
- `{company_name}_reference_results.csv`: Final results with reference counts

## Features

- **Robust Error Handling**: Implements retry mechanisms and graceful error recovery
- **Progress Tracking**: Saves results incrementally to prevent data loss
- **Rate Limiting**: Includes appropriate delays to respect USPTO's rate limits
- **Cross-Platform**: Tested on macOS, Windows, and Ubuntu
- **Browser Management**: Automatically handles Chrome WebDriver installation and updates

## Notes

- The scripts use Selenium WebDriver to interact with the USPTO PubWEST interface
- Results are saved incrementally, so you can safely interrupt and resume the process
- Make sure you have a stable internet connection when running the scripts
- The scripts include appropriate delays to prevent overloading the USPTO website

## Troubleshooting

If you encounter issues:
1. Ensure Chrome is installed and up to date
2. Check your internet connection
3. Verify that all dependencies are installed correctly
4. Make sure you're using the correct company name format

## License

This project is licensed under the terms of the included LICENSE file. 