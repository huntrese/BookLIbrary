import os
import time
import re
import requests
import urllib
import threading
import urllib.request
from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrape import main
from chapterscrape import scrapeBookInfo
# Define a function to extract chapter content
def sanitize_chapter_name(chapter_name):
    # Remove invalid characters from the chapter name
    sanitized_name = re.sub(r'[\/:*?"<>|]', '', chapter_name)
    # Truncate the name if it's too long
    max_filename_length = 255  # Maximum filename length on many systems
    if len(sanitized_name) > max_filename_length:
        sanitized_name = sanitized_name[:max_filename_length]
    return sanitized_name

def extract_chapter_content(chapter_link, book_directory):
    try:
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)

        driver.get(chapter_link)

        # Extract chapter name (from the <h3> element)
        chapter_name = None
        chapter_name_element = driver.find_element(By.ID, 'chapter-content')
        chapter_name_element2 = driver.find_element(By.ID, 'container')


        # Use BeautifulSoup to parse the element and find the chapter name
        soup = BeautifulSoup(chapter_name_element.get_attribute('innerHTML'), 'html.parser')
        for element in soup.find_all(text=re.compile(r'Chapter \d+')):
            chapter_name = element.strip()
            break  # Stop after the first match

        if chapter_name:
            chapter_name = re.sub(r'[^\w\s-]', '', chapter_name)  # Sanitize the chapter name
        else:
            soup = BeautifulSoup(chapter_name_element2.get_attribute('innerHTML'), 'html.parser')
            for element in soup.find_all(text=re.compile(r'Chapter \d+')):
                chapter_name = element.strip()
                chapter_name = re.sub(r'[^\w\s-]', '', chapter_name)  # Sanitize the chapter name

                break  # Stop after the first match

        # Extract chapter content (everything else in the #chapter-content div)
        chapter_content_element = driver.find_element(By.ID, 'chapter-content')
        chapter_content = chapter_content_element.get_attribute('innerHTML')

        soup = BeautifulSoup(chapter_content, 'html.parser')

        # Remove script and style elements
        for script in soup.find_all('script'):
            script.extract()

        # Remove specific div elements
        for div in soup.find_all('div', class_='ads'):
            div.extract()

        for div in soup.find_all('div', id='pf-3133-1'):
            div.extract()

        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # Get the cleaned content as a string
        cleaned_chapter_content = str(soup)

        # Create a file for the chapter and write the content to it
        chapter_name = sanitize_chapter_name(chapter_name)
        chapter_file_path = os.path.join(book_directory, f"{chapter_name}.txt")
        with open(chapter_file_path, 'w', encoding='utf-8') as chapter_file:
            chapter_file.write(cleaned_chapter_content)

        print(f"Chapter saved to {chapter_file_path}")

    except Exception as e:
        print(f"Error while extracting chapter: {str(e)}")

    driver.quit()

def process_book(book_name, book_url, img_url, author_name, description_text, chapter_links):
    if book_name and chapter_links:
        # Create a directory for the book if it doesn't exist
        book_name = re.sub(r'[^a-zA-Z0-9\s]', '', book_name).replace(' ', '-').lower()
        book_directory = os.path.join("books", book_name)
        os.makedirs(book_directory, exist_ok=True)

        # Save the author's name within the book directory
        if author_name:
            author_filename = os.path.join(book_directory, "author.txt")
            with open(author_filename, 'w', encoding='utf-8') as author_file:
                author_file.write(f"{author_name}")
                print(f"Author's name saved to {author_filename}")
        if description_text:
            description_file_path = os.path.join(book_directory, "description.txt")
            with open(description_file_path, 'w', encoding='utf-8') as description_file:
                description_file.write(f"{description_text}")
                print(f"Author's name saved to {description_file_path}")

        # Download the image and save it in the book directory
        if img_url:
            try:
                if not img_url.startswith("https//"):
                    img_url = "https://" + img_url[7:]
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    image_path = os.path.join(book_directory, 'cover.jpg')
                    with open(image_path, 'wb') as img_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            img_file.write(chunk)
                    print(f"Cover image saved to {image_path}")
                else:
                    print(f"Failed to download cover image for {book_name}: Status code {response.status_code}")

            except Exception as e:
                print(f"Failed to download cover image for {book_name}: {str(e)}")

        print(f"Book Name: {book_name}")
        print(f"Chapter Links: {chapter_links}")

        # Loop through chapter links and extract content
        for i, chapter_link in enumerate(chapter_links, 1):
            # time.sleep(0.3)
           
            extract_chapter_content(chapter_link, book_directory)

# Initialize a Selenium webdriver (Firefox in this case)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Assuming you have a list of links named "links"
links = scrapeBookInfo()  # This will return a set of links

# Create a thread for each book and start them concurrently
threads = []
for book_info in links:
    thread = threading.Thread(target=process_book, args=book_info)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Close the Selenium webdriver
