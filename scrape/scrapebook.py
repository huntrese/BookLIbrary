from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scrape import main

from selenium.webdriver.firefox.options import Options

# Initialize a Selenium webdriver (Firefox in this case)

firefox_options = Options()
firefox_options.add_argument('--headless')

# Initialize a Selenium webdriver with the Firefox options
driver = webdriver.Firefox(options=firefox_options)

# Assuming you have a list of links named "links"
links = main()

# Create a dictionary to store elements grouped by website URL
elements_by_website = {}

for link in links:
    driver.get(link)  # Navigate to the link

    try:
        # Find the <h1> element with the specified class using CSS selector
        h1_element = driver.find_element(By.CSS_SELECTOR, 'h1.font-set-b24.text-gray-t1.line-clamp-2.sm2\\:font-set-b32')

        # Extract the text of the <h1> element
        h1_text = h1_element.text

        # Find the <div> element with the specified class using CSS selector
        div_element = driver.find_element(By.CSS_SELECTOR, 'div.font-set-sb15.break-word.line-clamp-1.sm2\\:font-set-sb15')

        # Extract the text of the <div> element
        div_text = div_element.text

        # Find the <div> element with the specified class structure using CSS selector
        desc_element = driver.find_element(By.CSS_SELECTOR, 'div.font-set-r13.text-gray-desc.sm2\\:font-set-r15')

        # Find all the <span> elements within the <div> element
        span_elements = desc_element.find_elements(By.TAG_NAME, 'span')

        # Extract and concatenate text from all <span> elements
        description_text = ''
        for span in span_elements:
            description_text += span.text + ' '  # Add space between <span> texts

        # Create a tuple containing extracted elements and their text
        elements_tuple = (h1_text, div_text, description_text.strip())  # Remove trailing space

        # Add the tuple to the corresponding website URL in the dictionary
        if link in elements_by_website:
            elements_by_website[link].append(elements_tuple)
        else:
            elements_by_website[link] = [elements_tuple]

    except NoSuchElementException:
        print("Elements not found on this page:", link)

# Close the browser when done
driver.quit()

# Print the found elements grouped by website URL
for website_url, elements_list in elements_by_website.items():
    print("Website URL:", website_url)
    for elements_tuple in elements_list:
        h1_text, div_text, description_text = elements_tuple
        print("Title:", h1_text)
        print("Text:", div_text)
        print("Description:", description_text)
        print()
