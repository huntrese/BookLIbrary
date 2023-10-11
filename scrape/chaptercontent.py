import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from scrape import main
from chapterscrape import extract_chapters_and_book_name

# Initialize a Selenium webdriver (Firefox in this case)

firefox_options = Options()
firefox_options.add_argument('--headless')

# Initialize a Selenium webdriver with the Firefox options
driver = webdriver.Firefox(options=firefox_options)

# Assuming you have a list of links named "links"
links = main()  # This will return a set of links

for url in links:
    book_name, chapter_links, image_src, author_name = extract_chapters_and_book_name(url)
    if book_name and chapter_links:
        # Create a directory for the book if it doesn't exist
        book_directory = os.path.join("books", book_name)
        os.makedirs(book_directory, exist_ok=True)

        # Save the author's name within the book directory
        if author_name:
            author_filename = os.path.join(book_directory, "author.txt")
            with open(author_filename, 'w', encoding='utf-8') as author_file:
                author_file.write(f"Author Name: {author_name}")
                print(f"Author's name saved to {author_filename}")

        # Download the image and save it in the book directory
        if image_src:
            image_response = requests.get(image_src)
            if image_response.status_code == 200:
                image_filename = os.path.join(book_directory, "cover.jpg")
                with open(image_filename, 'wb') as image_file:
                    image_file.write(image_response.content)
                print(f"Cover image saved to {image_filename}")
            else:
                print(f"Failed to download cover image for {book_name}")

        print(f"Book Name: {book_name}")
        print(f"Chapter Links: {chapter_links}")

        # Loop through chapter links
        for i, chapter_link in enumerate(chapter_links, 1):
            try:
                time.sleep(0.3)

                driver.get(chapter_link)
                chapter_content_element = driver.find_element(By.CSS_SELECTOR, 'div.fr-view')
                chapter_content = chapter_content_element.text
                chapter_name_element = driver.find_element(By.CSS_SELECTOR, 'h4.font-set-b18 > span')
                chapter_name = chapter_name_element.text

                # Create a file for the chapter and write the content to it
                chapter_file_path = os.path.join(book_directory, f"Chapter_{i}.txt")
                with open(chapter_file_path, 'w', encoding='utf-8') as chapter_file:
                    chapter_file.write(f"Chapter Name: {chapter_name}\n")
                    chapter_file.write("Chapter Content:\n")
                    chapter_file.write(chapter_content)
            except:
                continue

            print(f"Chapter {i} saved to {chapter_file_path}")
    else:
        print(f"Book name and chapter links not found on {url}")

# Close the Selenium webdriver
driver.quit()
