from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import threading
import queue
from scrape import main

# Create a thread-safe queue to hold book URLs
book_urls = queue.Queue()

# Extract book URL, image URL, and book name
def scrapeBookInfo():
    info = []

    def initialize_webdriver():
        # Initialize a Selenium webdriver with Firefox options
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        driver = webdriver.Edge(options=firefox_options)
        return driver

    def extract_chapters_and_book_info(driver, book_url, book_name, img_url):
        time.sleep(0.5)
        driver.get(book_url)

        # Find the div element with class "list-chapter"
        div_element = driver.find_element(By.CSS_SELECTOR, 'ul.list-chapter')

        # Find all list items within the div
        li_elements = div_element.find_elements(By.TAG_NAME, 'li')

        # Extract chapter links
        chapter_links = [li.find_element(By.TAG_NAME, 'a').get_attribute('href') for li in li_elements]

        author_name = driver.find_element(By.XPATH, "//div[@class='info']//h3[text()='Author:']/following-sibling::a").text

        # Extract book description
        description_element = driver.find_element(By.CSS_SELECTOR, 'div.desc-text')
        description_inner_html = description_element.get_attribute('innerHTML')

        return book_name, img_url, author_name, description_inner_html, chapter_links

    def scrape_book_info_thread():
        while not book_urls.empty():
            book_url, book_name, img_url = book_urls.get()
            driver = initialize_webdriver()
            book_name, img_url, author_name, description_text, chapter_links = extract_chapters_and_book_info(driver, book_url, book_name, img_url)
            driver.quit()
            
            info.append([book_name, book_url, img_url, author_name, description_text, chapter_links])

    # Example usage:
    book_info = main()

    for i in book_info:
        book_url = i[0]
        img_url = i[1]
        book_name = i[2]
        book_urls.put((book_url, book_name, img_url))

    # Create and start multiple threads to scrape book information in parallel
    num_threads = 10  # You can adjust the number of threads as needed
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=scrape_book_info_thread)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return info

if __name__ == '__main__':
    scraped_info = scrapeBookInfo()
    # Process the scraped data as needed
