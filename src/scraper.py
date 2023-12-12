# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
from get_pseudos import *

def scrape(url, output_directory):
    # Configuration de Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200x600')

    if "crunchyroll" in url:
        driver = uc.Chrome()
        driver.get(url)

        wait = WebDriverWait(driver, 2)

        # Scrolle jusqu'à la fin de la page
        scroll_to_bottom(driver)
        html = driver.page_source

    if "animationdigitalnetwork" in url:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time.sleep(5)

        # scroll_to_bottom(driver)
        html = driver.page_source

    # Sauvegarde le contenu de la page dans un fichier
    with open(f'{output_directory}/page.html', 'w', encoding='utf-8') as file:
        file.write(html)

    driver.quit()
    print(f"La page HTML est sauvegardée dans {output_directory}")

    extract_pseudos(html, output_directory)
