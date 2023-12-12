from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time 

def scroll_to_bottom(driver):
    # Scrolle jusqu'à la fin de la page
    while True:
        driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)  # temps d'attente entre les défilements
        # check si fin de page atteint
        end_of_page = driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight;")
        if end_of_page:
            break

def scrape(url):
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

        #scroll_to_bottom(driver)
        html = driver.page_source

    # Sauvegarde le contenu de la page dans un fichier
    with open('page.html', 'w', encoding='utf-8') as file:
        file.write(html)

    driver.quit()
    print(f"La page HTML est sauvegardée")

    extractPseudos(html)

def extractPseudos(html):
    soup = BeautifulSoup(html, 'html.parser')


    contenuInClass1 = soup.find_all('div', class_='sc-853f2479-7 jBFBhi') #ADN comentaire
    contenuInClass2 = soup.find_all('div', class_='sc-853f2479-7 jYPWes') #ADN reponse
    contenuInClass3 = soup.find_all('div', class_='comment__username--dNChO') #Crunchyroll comentaire

    contenuInAllClass = contenuInClass1 + contenuInClass2 + contenuInClass3

    #sauvegarde des pseudos
    if contenuInAllClass:
        with open('pseudo.txt', 'a', encoding='utf-8') as fichier:
            for pseudos in contenuInAllClass:
                contenu = pseudos.get_text(strip=True)
                fichier.write(contenu + '\n')
        print("Pseudos sauvegardés dans pseudos.txt.")
    else:
        print("Balises non trouvées")




#sur ADN,après le nom de l'anime dans l'url les ep sont numéroter ex:ep1 de fairy tail => https://animationdigitalnetwork.fr/video/fairy-tail/3628
#for epID in range(3628,3631):
 #   url = 'https://animationdigitalnetwork.fr/video/fairy-tail/' + str(epID)
  #  scrape(url)

url = 'https://www.crunchyroll.com/fr/watch/G69XGG44R/ryomen-sukuna'
scrape(url)