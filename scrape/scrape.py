from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
from selenium.webdriver.firefox.options import Options

# Initialize a Selenium webdriver (Firefox in this case)

firefox_options = Options()
firefox_options.add_argument('--headless')

# Initialize a Selenium webdriver with the Firefox options
def main():
    # Start a Selenium webdriver (You need to have Selenium installed and a WebDriver for a specific browser)
    driver = webdriver.Firefox(options=firefox_options)
    # driver = webdriver.Firefox()  # Example for Firefox

    # Navigate to the webpage
    url = "https://www.wuxiaworld.com/"
    driver.get(url)

    # Define a set to store unique links
    unique_links = set()

    # Define a function to find and print the links
    def find_and_print_links():
        elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/novel/")]')
        for element in elements:
            link = element.get_attribute("href")
            if link != url + 'novel/':  # Exclude the default URL
                if link not in unique_links:
                    unique_links.add(link)
                    print(link)

    # Keep trying to find and print the links for up to 3 seconds
    start_time = time.time()
    while time.time() - start_time < 3:
        try:
            find_and_print_links()
            # You may want to add some delay to give the page time to load or avoid overloading the server
            time.sleep(2)  # Wait for 2 seconds
        except StaleElementReferenceException:
            continue  # If a StaleElementReferenceException occurs, try again

    # Close the browser when done
    driver.quit()
    return unique_links
