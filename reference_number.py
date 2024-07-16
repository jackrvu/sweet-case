import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv

# Function to extract the number from the string
def extract_number(string):
    return int(''.join(filter(str.isdigit, string)))

patents = pd.read_csv("/Users/jackvu/Desktop/PDS/patent_lookup/venv/ncr_patents.csv")
patent_names = patents["Name"]
patent_ids = patents["Patent ID"]
patent_dates = patents["Date"]
result_numbers = []
current_patent = 0
total_patents = 100

while current_patent < total_patents:
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get('https://ppubs.uspto.gov/pubwebapp/')
    driver.maximize_window()
    for num in range(25): # close and reopen after every 25 requests to the uspto
        while True:
            try:
                trix_editor = driver.find_element(By.CSS_SELECTOR, 'trix-editor[trix-id="1"]')
                break
            except:
                continue
        input_value = patent_ids[current_patent][3:11] + '.ref'
        # Click on the editor to focus
        trix_editor.click()
        # Send keys to the editor

        trix_editor.send_keys(input_value)
        search_button = driver.find_element(by=By.CLASS_NAME, value='buttonSubmit')

        while True:
            try:
                search_button.click()
                break
            except:
                continue
        result_number_individual = driver.find_element(by=By.CLASS_NAME, value='resultBar').find_element(by=By.CLASS_NAME, value='resultNumber').text
        if len(result_number_individual) > 0:
            result_numbers.append(result_number_individual)
        else:
            result_numbers.append('0')
        trix_editor.clear()
        current_patent += 1
    csv_file = "ncr_reference_results.csv"
    temp_patent_ids = patent_ids[0:current_patent + 1]
    temp_patent_names = patent_names[0:current_patent + 1]
    temp_patent_dates = patent_dates[0:current_patent + 1]

    # Combine the lists
    combined = list(zip(temp_patent_ids, result_numbers, temp_patent_names, temp_patent_dates))

    # Sort the combined list based on the numerical value in list4
    combined_sorted = sorted(combined, key=lambda x: extract_number(x[0]), reverse=True)

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(["Patent ID", "References Found", "Patent Name", "Patent Date"])

        # Write the rows
        for id_, number, name, date in combined_sorted:
            writer.writerow([id_, number, name, date])

    print(f"Successfully found number of references {len(result_numbers)} patents and exported to ncr_reference_results.csv.")

    driver.quit()

csv_file = "ncr_reference_results.csv"

# Combine the lists
combined = list(zip(patent_ids, result_numbers, patent_names, patent_dates))

# Sort the combined list based on the numerical value in list4
combined_sorted = sorted(combined, key=lambda x: extract_number(x[0]), reverse=True)

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(["Patent ID", "References Found", "Patent Name", "Patent Date"])

    # Write the rows
    for id_, number, name, date in combined_sorted:
        writer.writerow([id_, number, name, date])

print(f"Successfully found number of references {len(result_numbers)} patents and exported to ncr_reference_results.csv.")


