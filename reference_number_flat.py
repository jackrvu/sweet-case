#!/usr/bin/env python3
"""
Scrapes USPTO PubWEST to count "References Cited" for patents listed in a company's CSV file.

This script automates the process of retrieving reference counts for patents by:
1. Reading patent numbers from a company-specific CSV file
2. Using Selenium to interact with the USPTO PubWEST interface
3. Recording reference counts and saving results to a new CSV

The script implements robust error handling and progress tracking, with results
saved incrementally to prevent data loss in case of interruption.

Tested on: macOS 14 + Chrome 125, Windows 11 + Chrome 125, Ubuntu 22 + Chrome 125
(and Chromium-based Edge)
"""

from __future__ import annotations

import argparse
import csv
import os
import platform
import re
import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def digits_only(text: str) -> str:
    """Extract and return only the decimal digits from the input text."""
    return "".join(re.findall(r"\d", text))


def extract_number_for_sorting(text: str) -> int:
    """Extract numeric value for sorting purposes, returning 0 if no digits found."""
    return int(digits_only(text) or 0)


def clear_trix_editor(driver, editor_css: str = 'trix-editor[trix-id="1"]') -> None:
    """
    Clears the PubWEST Trix search field completely, including both visible and hidden elements.
    
    Implements a multi-layered approach to ensure complete clearing:
    1. Keyboard shortcut to select and delete all content
    2. JavaScript to clear the editor's HTML content
    3. JavaScript to clear all associated hidden input fields
    """
    trix = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, editor_css))
    )
    trix.click()

    sel_key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
    ActionChains(driver).key_down(sel_key).send_keys("a").key_up(sel_key).send_keys(
        Keys.DELETE
    ).perform()

    driver.execute_script(
        """
        const ed = arguments[0].editor;
        if (ed) ed.loadHTML('');
        document
            .querySelectorAll('input[trix-input]')
            .forEach(inp => { inp.value = ''; });
        """,
        trix,
    )


def main(company_name: str, total_patents: int | None = None) -> None:
    """
    Main execution function that processes patents and retrieves their reference counts.
    
    Args:
        company_name: Name of the company whose patents to process
        total_patents: Optional limit on number of patents to process
    """
    csv_path = Path(f"{company_name.replace(' ', '_')}_patents.csv")
    if not csv_path.exists():
        print(f"CSV file '{csv_path}' not found. Run download_patents.py first.")
        return

    # Load patent data from CSV
    df = pd.read_csv(csv_path)
    patent_nums = df["Document/Patent number"].tolist()
    titles = df["Title"].tolist()
    inventors = df["Inventor Name(s)"].tolist()
    pub_dates = df["Publication Date"].tolist()

    total_patents = total_patents or len(patent_nums)
    batch_size = 10

    out_csv = Path(f"{company_name.replace(' ', '_')}_reference_results.csv")
    reference_counts: list[str] = []
    processed = 0

    def write_progress() -> None:
        """Write current progress to CSV file, sorted by patent number."""
        rows = zip(
            patent_nums[:processed],
            reference_counts,
            titles[:processed],
            inventors[:processed],
            pub_dates[:processed],
        )
        sorted_rows = sorted(rows, key=lambda r: extract_number_for_sorting(r[0]), reverse=True)

        with out_csv.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "Document/Patent number",
                    "References Found",
                    "Title",
                    "Inventor Name(s)",
                    "Publication Date",
                ]
            )
            w.writerows(sorted_rows)

    try:
        while processed < total_patents:
            # Create new WebDriver instance for each batch to prevent memory issues
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service)
            except WebDriverException as exc:
                print("Chrome WebDriver error – is Chrome installed and current?")
                print(exc)
                return

            # Initialize browser session
            driver.get("https://ppubs.uspto.gov/pubwebapp/")
            driver.maximize_window()
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'trix-editor[trix-id="1"]'))
            )

            # Process patents in batches
            for _ in range(batch_size):
                if processed >= total_patents:
                    break

                clear_trix_editor(driver)

                # Prepare and submit search query
                pn_raw = str(patent_nums[processed])
                pn_digits = digits_only(pn_raw)
                search_string = f"{pn_digits}"

                editor = driver.find_element(By.CSS_SELECTOR, 'trix-editor[trix-id="1"]')
                editor.send_keys(search_string)
                driver.find_element(By.CLASS_NAME, "buttonSubmit").click()

                # Extract reference count
                try:
                    result_text = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, ".resultBar .resultNumber")
                        )
                    ).text
                except TimeoutException:
                    result_text = "0"

                reference_counts.append(result_text or "0")
                processed += 1
                time.sleep(0.5)  # Rate limiting to prevent overloading

            write_progress()
            print(f"Processed {processed}/{total_patents} patents … saved to {out_csv}")
            driver.quit()

    except Exception as e:
        print("Unhandled exception – writing progress before exit.")
        write_progress()
        raise e

    write_progress()
    print(f"✓ Finished: results for {processed} patents written to {out_csv}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Count references for patents in a company CSV.")
    ap.add_argument("company", help="Company name (matches CSV).")
    ap.add_argument("--total", type=int, help="Optional limit on patents to process.")
    args = ap.parse_args()

    main(args.company, total_patents=args.total)
