import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import csv


driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://ppubs.uspto.gov/pubwebapp/static/pages/ppubsbasic.html')

search_box = driver.find_element(by=By.ID, value='searchText1')
search_box.send_keys('ncr')
select = Select(driver.find_element(by=By.ID, value='searchField1'))
select.select_by_value('AS')
search_button = driver.find_element(by=By.ID, value='basicSearchBtn')
search_button.click()
time.sleep(1)
names = []
patent_ids = []
dates = []
for num in range(50):
    main_body = driver.find_element(by=By.CSS_SELECTOR, value='table')
    html = main_body.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    patents = soup.find_all('tr')[1:]

    for patent in patents:
        current_patent = str(patent)
        patent_ids.append(current_patent[current_patent.index('aria-label=') + 12: current_patent.index('aria-label=') + 29].replace('"', '').replace(' ', '').replace('c', ''))
        left_index = current_patent.index('aria-label=') + 12
        right_index = left_index + 17
        left_name_index = current_patent.index('</a>') + 13
        name = current_patent[left_name_index:]
        index_end = name.index("<")
        date = name[index_end:]
        date = date[date.index('<td>2') + 4:date.index('<td>2') + 14]
        dates.append(date)
        name = name[:index_end]
        names.append(name)
    next_page_button = driver.find_element(by=By.ID, value='paginationNextItem')
    next_page_button.click()
    time.sleep(.5)


csv_file = "ncr_patents.csv"

# Write the lists to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(["Name", "Patent ID", "Date"])

    # Write the rows
    for name, id_, date in zip(names, patent_ids, dates):
        writer.writerow([name, id_, date])
print(f"Successfully pulled {len(patent_ids)} patents and exported to ncr_patents.csv.")
driver.quit()


