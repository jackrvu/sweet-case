import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv
import argparse
import sys
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(company_name):
    try:
        # Use webdriver-manager to get the correct ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    except WebDriverException as e:
        print("Error initializing Chrome WebDriver. Make sure Chrome is installed and up to date.")
        print(e)
        sys.exit(1)

    driver.get('https://ppubs.uspto.gov/pubwebapp/static/pages/ppubsbasic.html')
    time.sleep(4)
    # Wait for the search box to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'searchText1'))
    )
    search_box = driver.find_element(by=By.ID, value='searchText1')
    search_box.send_keys(company_name)
    time.sleep(2)
    select = Select(driver.find_element(by=By.ID, value='searchField1'))
    select.select_by_value('AS')
    time.sleep(2)
    # Use the correct search button
    search_button = driver.find_element(by=By.ID, value='search-btn-search')
    search_button.click()
    time.sleep(5)
    # Wait for the results table to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
    )
    # Prepare lists for each field
    patent_numbers = []
    titles = []
    inventors = []
    pub_dates = []
    citation_counts = []
    max_retries = 3
    for num in range(50):
        retries = 0
        while retries < max_retries:
            try:
                main_body = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
                )
                html = main_body.get_attribute('innerHTML')
                soup = BeautifulSoup(html, 'html.parser')
                patents = soup.find_all('tr')[1:]
                if not patents:
                    raise Exception('No patent rows found')
                for i, patent in enumerate(patents):
                    try:
                        tds = patent.find_all('td')
                        if len(tds) < 6:
                            print(f"Row does not have enough columns: {patent}")
                            continue
                        # Extract fields by index
                        patent_number = tds[1].get_text(strip=True)
                        title = tds[3].get_text(strip=True)
                        inventor = tds[4].get_text(strip=True)
                        pub_date = tds[5].get_text(strip=True)
                        patent_numbers.append(patent_number)
                        titles.append(title)
                        inventors.append(inventor)
                        pub_dates.append(pub_date)
                        # Click the patent number link to go to the detail page
                        try:
                            # Find the link in the patent number cell
                            link_elem = driver.find_elements(By.CSS_SELECTOR, 'table tr')[i+1].find_elements(By.TAG_NAME, 'td')[1].find_element(By.TAG_NAME, 'a')
                            driver.execute_script("arguments[0].click();", link_elem)
                            # Wait for the citation count to be present
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'resultNumber'))
                            )
                            citation_elem = driver.find_element(By.CLASS_NAME, 'resultNumber')
                            citation_count = citation_elem.text.strip()
                            # Try to convert to int, fallback to 0
                            try:
                                citation_count = int(citation_count)
                            except Exception:
                                citation_count = 0
                            citation_counts.append(citation_count)
                            driver.back()
                            # Wait for the table to be present again
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
                            )
                            time.sleep(1)
                        except Exception as e:
                            print(f"Error extracting citation count: {e}")
                            citation_counts.append(0)
                            driver.back()
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
                            )
                            time.sleep(1)
                    except Exception as e:
                        print(f"Error parsing patent row: {e}")
                        print(f"Problematic row: {patent}")
                        continue
                break  # Success, break out of retry loop
            except Exception as e:
                print(f"Error finding or parsing table (attempt {retries+1}/{max_retries}): {e}")
                time.sleep(3)
                retries += 1
                if retries == max_retries:
                    print("Giving up on this page.")
                    break
        try:
            # Check if we are on the last page using the pageInfo element
            try:
                page_info_elem = driver.find_element(by=By.ID, value='pageInfo')
                page_info_text = page_info_elem.text.strip()  # e.g., 'Page 1 of 29'
                if page_info_text.lower().startswith('page') and 'of' in page_info_text:
                    parts = page_info_text.split()
                    current_page = int(parts[1])
                    total_pages = int(parts[3])
                    if current_page >= total_pages:
                        print(f"Reached last page ({current_page} of {total_pages}). Ending pagination.")
                        break
            except Exception as e:
                print(f"Could not read pageInfo element: {e}")
                # If we can't read it, fall back to next button logic

            next_page_button = driver.find_element(by=By.ID, value='paginationNextItem')
            # Check if the next button is disabled or not displayed
            if not next_page_button.is_displayed() or not next_page_button.is_enabled():
                print("Next button is not available (disabled or hidden). Ending pagination.")
                break
            next_page_button.click()
            # Wait for the table to update (wait for presence again)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
            )
            time.sleep(2)  # Extra wait to ensure page is fully loaded
        except Exception:
            print("No more pages or error clicking next page.")
            break

    csv_file = company_name.replace(" ", "_") + "_patents.csv"

    # Write the lists to the CSV file, sorted by citation count
    rows = list(zip(patent_numbers, titles, inventors, pub_dates, citation_counts))
    rows_sorted = sorted(rows, key=lambda x: x[4], reverse=True)
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Document/Patent number", "Title", "Inventor Name(s)", "Publication Date", "Reference Count"])
        for pn, title, inventor, pub_date, citation_count in rows_sorted:
            writer.writerow([pn, title, inventor, pub_date, citation_count])
    print(f"Successfully pulled {len(patent_numbers)} patents and exported to {csv_file}.")
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download patents for a given company from USPTO.")
    parser.add_argument("company", type=str, help="Company name to search for")
    args = parser.parse_args()
    main(args.company)


