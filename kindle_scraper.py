from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import requests
import os

def get_highlights(email, password):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

    chrome_options.add_argument("--no-sandbox")

    # DRIVER_PATH = '/Users/lucasgen/Downloads/chromedriver'
    # driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)

    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


    print("getting driver---------------")
    driver.get('https://read.amazon.com/kp/notebook')
    print(driver.title)

    email_input = driver.find_element(By.XPATH, '//*[@id="ap_email"]')
    pass_input = driver.find_element(By.XPATH, '//*[@id="ap_password"]')
    email_input.send_keys(email)
    pass_input.send_keys(password)


    pass_input.send_keys(Keys.ENTER)

    print("logging in...")

    # wait for page to load
    elem = WebDriverWait(driver, 45).until(
    EC.presence_of_element_located((By.ID, "library-section"))
    )

    print("logged in")

    def get_book_list():
        books = []
        books = driver.find_elements(By.XPATH, "//div[contains(@class, 'kp-notebook-library-each-book')]")
        return books

    print("retrieving books...")

    books = get_book_list()

    book_highlights = {}

    i = 0
    while True:
        if i >= len(books): break
        book = books[i]
        title = book.text.splitlines()[0]
        author = book.text.splitlines()[1][4:]
        print(title)
        print(author)
        i += 1
        book.click()

        # wait for page to load
        elem = WebDriverWait(driver, 45).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@id, 'highlight')]")) 
        )

        highlights = []
        highlight_text = []
        highlights = driver.find_elements(By.XPATH, "//span[contains(@id, 'highlight')]")

        # skip the first one since it's just a number
        for highlight in highlights[1:]:
            highlight_text.append(highlight.text)
        
        book_highlights[title] = {
            "highlights": highlight_text,
            "author": author,
        }
        books = get_book_list()

    return book_highlights