from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

import time
import retrying  # Import the retrying library

# Define a retry decorator
@retrying.retry(
    stop_max_attempt_number=3,  # Number of retries
    wait_fixed=1000  # Time to wait (in milliseconds) between retries
)
def initialize_webdriver():
    # Initialize a Selenium webdriver with Firefox options
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options)
    return driver

def extract_chapters_and_book_name(base_url):
    # Function to generate chapter links
    def generate_chapter_links(base_url):
        chapter_links = []
        for i in range(1, 11):  # Iterate from 1 to 10
            chapter_url = f"{base_url[:-1]}-{i}"  # Append the chapter number
            chapter_links.append(chapter_url)
        return chapter_links

    try:
        # Initialize the WebDriver with retries
        driver = initialize_webdriver()

        time.sleep(1.5)
        driver.get(base_url)
        found_href = None  # To store the href when found
        image_src = None  # To store the image source
        author_name = None  # To store the author's name

        # Find all div elements matching the given styling
        div_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="mt-[16px]"]')

        # Find the image element and get the src attribute
        img_element = driver.find_element(By.CSS_SELECTOR, 'img.absolute.top-0.left-0')
        image_src = img_element.get_attribute('src')

        # Find the author's name element
        author_element = driver.find_element(By.CSS_SELECTOR, 'div.font-set-sb15.break-word.line-clamp-1.sm2\\:font-set-sb15')
        author_name = author_element.text.strip()

        # Loop through the matching div elements
        for div_element in div_elements:
            try:
                # Find the anchor element within the div
                a_element = div_element.find_element(By.TAG_NAME, 'a')

                # Get the href attribute of the anchor element
                href = a_element.get_attribute('href')

                if href:
                    found_href = href
                    break  # Stop searching once href is found
            except:
                pass  # Continue searching if the element is not found

        if found_href:
            # Split the URL and replace the chapter number iteratively
            base_parts = found_href.split("-")
            book_name = found_href.split('/')[4]

            chapter_links = generate_chapter_links('-'.join(base_parts[:-2]) + '-chapter-')
            return book_name, chapter_links, image_src, author_name
        else:
            return None, [], image_src, author_name

    finally:
        driver.quit()



