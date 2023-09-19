"""This script was constructed to make use of the Selenium scraping tool to collect vulnerable, endangered, and
critically endangered specie data.

The Selenium tool makes use of the Firefox web-browser extension to render a live web-page which can be interacted with
and at which HTML elements can be extracted using their XPATH.

Please make sure the correct files are specified when running this document:
Line 54: Specify the txt file to which the collected data will be written to. The file must already exist.
Line 65: Specify the txt file to which the urls at which errors occur are written to for manual investigation
The position.csv file must specify the value 0 at the start of data collection.
This will track the current url to be collected and allow stopping and starting the process with no repeated data collection


Author: Travis Dawson
Disclaimer: ChatGPT was used in the creation of certain eqlements within this script.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.webdriver.firefox.options import Options



def extract_element_by_xpath(xpath: str):
    """This method extracts HTML elements from the HTML page by means of specifying the XPath of the element.

    Args:
        xpath (str): The XPATH leading to the HTML element to be extracted

    Returns:
        (str): The extracted html content in a usable string format
    """
    wait = WebDriverWait(driver, 4)
    extracted_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    return extracted_element.text.strip()


def extract_justification_and_assessors():
    """This method extracts both the justification and assessor elements due to the need to click a button to render elements.

    Returns:
        (str) justification: The extracted justification
        (str) assessors: The extracted assessors
    """
    button = driver.find_element(By.XPATH, "//div[contains(text(), 'Assessment Information in detail')]")

    driver.execute_script("arguments[0].click();", button)

    justification = extract_element_by_xpath("/html/body/div[3]/div[2]/main/div/div/div[5]/article[2]/div[3]/div[2]/div/div[2]/div/p")
    assessors = extract_element_by_xpath("/html/body/div[3]/div[2]/main/div/div/div[5]/article[2]/div[3]/div[2]/div/div[1]/div[4]")
    return justification, assessors


def write_to_file(scientific_name, criteria, country, justification, assessors):
    """This method will record the collected data and write it to a file.
    Please specify the correct file to which data should be written to

    Args:
        scientific_name (str): The scientific name of the specie
        criteria (str): The criteria of the specie vulnerability classification
        country (str): The country in which the specie is found
        justification (str): The justification behind the criteria rating
        assessors (str): The names of the assessors passing the criteria and justification
    """
    with open("results/data_no_justification.txt", "a") as f:
        f.write(scientific_name + "\n")
        f.write(criteria + "\n")
        f.write(country + "\n")
        f.write(justification + "\n")
        f.write("Assessors: " + assessors + "\n")
        f.write("\n")


def write_error_to_file(url):
    """This method write the passed url to a file for further investigation as an error in collection occurred

    Args:
        url (str): The URl at which the error occurred
    """
    with open("errors/errors_no_justification.txt", "a") as file:
        file.write(url + "\n")


def read_position():
    """This method reads the current position, specifying the url to start collecting data from.

    Please reset the value inside of position.csv to zero when starting a new data collection process
    Returns:
        (int): The position of the url to continue data collection from
    """
    with open("position.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            return int(row[0])


def write_position(position):
    """This method updates the current position in the position.csv file

    Args:
        position (int): An integer value representing the current url position at which it should collect data from.
    """
    with open("position.csv", "w") as file:
        file.write(str(position))


def extract_information(url, driver):
    """This method extracts the required information from the specified url.

    This information will be saved in the form:
    Scientific Name
    Criteria
    Country
    Justification
    Assessors
    New line

    The information will be displayed to the terminal during collection

    Args:
        url (str): The url at which the data is to be extracted from
        driver (Selenium driver): The Selenium driver enabling data scraping

    """
    driver.get(url)  # Create the web-page specified by the url

    try:
        scientific_name = extract_element_by_xpath("/html/body/div[3]/div[2]/main/div/div/header/div/div/div/div[1]/p")  # Extract the scientific name using method 1
        print(scientific_name)
    except Exception:
        print("Error in method 1")

    try:
        scientific_name = extract_element_by_xpath("/html/body/div[3]/div[2]/main/div/div/header/div/div/div/h1")  # Extract the scientific name using method 2
        print(scientific_name)
    except:
        print("Error in method 2")

    criteria = extract_element_by_xpath("/html/body/div[3]/div[2]/main/div/div/div[5]/article[2]/div[2]/div/p[1]")  # Extract the criteria elements
    print(criteria)

    country = extract_element_by_xpath(
        "/html/body/div[3]/div[2]/main/div/div/div[5]/article[3]/div[1]/div/div/div[2]/p")  # Extract the country elements
    print(country)

    justification, assessors = extract_justification_and_assessors()  # Extract the justification and assessor elements
    justification = justification.strip()
    print(justification)
    print(assessors)

    write_to_file(scientific_name, criteria, country, justification, assessors)  # Save all of the collected data to file
    print("-------------------------------------------------------")


if __name__ == "__main__":
    position = read_position()
    with open("links/no_justification_links.csv", "r") as file:  # Specify the file in which the species url links are composed
        csv_reader = csv.reader(file)
        for index, row in enumerate(csv_reader):  # Loop through all collected url in the file
            if index < position:  # Skip already collected urls to speed up the collection process
                continue
            print(position)
            try:
                firefox_options = Options()  # Specify options to not render the generated webpage
                firefox_options.add_argument('--headless')

                driver = webdriver.Firefox(options=firefox_options)  # Configure the selenium driver using the Firefox browser
                extract_information(row[0], driver)  # Extract the information for the current url
                driver.quit()  # Close the rendered html page, so the new url can generate the next page to extract data
            except Exception:  # An error occured in data extraction, write the url responsible to an error file for manual investigation
                write_error_to_file(row[0])

            position = position + 1  # Update the position
            write_position(position)  # Write the position to file




