from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Initialize a Selenium webdriver (Firefox in this case)

firefox_options = Options()
firefox_options.add_argument('--headless')

# Initialize a Selenium webdriver with the Firefox options
def main():
    # Start a Selenium webdriver (You need to have Selenium installed and a WebDriver for a specific browser)
    driver = webdriver.Firefox(options=firefox_options)
    # driver = webdriver.Firefox()  # Example for Firefox

    # Navigate to the webpage
    url = "https://allnovelfull.net/"
    driver.get(url)
    driver.set_page_load_timeout(1)  # Set a 60-second timeout (adjust as needed)

    # Define a set to store unique links
    unique_links = set()


    # Keep trying to find and print the links for up to 3 seconds

    # Extract book information using BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    book_items = soup.find_all("div", class_="item")

    for item in book_items:
        book_link = url+item.find("a")["href"]
        img_link = url+item.find("img")["src"]
        book_name = item.find("h3").text

        book_link = book_link.replace("//","/")
        img_link=img_link.replace("//","/")
        print("Book Link:", book_link)
        print("Image Link:", img_link)
        print("Book Name:", book_name)
        print()
        unique_links.add((book_link,img_link,book_name))
    # print(unique_links)
    # Close the browser when done
    driver.quit()
    return unique_links

if __name__ == "__main__":
    main()
