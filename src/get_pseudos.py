from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

def scroll_to_bottom(driver):
    # Scrolle jusqu'à la fin de la page
    while True:
        driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)  # temps d'attente entre les défilements
        # check si fin de page atteint
        end_of_page = driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight;")
        if end_of_page:
            break



def extract_pseudos(html, output_directory):
    soup = BeautifulSoup(html, 'html.parser')

    contenuInClass1 = soup.find_all('div', class_='sc-853f2479-7 jBFBhi') #ADN comentaire
    contenuInClass2 = soup.find_all('div', class_='sc-853f2479-7 jYPWes') #ADN reponse
    contenuInClass3 = soup.find_all('div', class_='comment__username--dNChO') #Crunchyroll comentaire

    contenuInAllClass = contenuInClass1 + contenuInClass2 + contenuInClass3

    #sauvegarde des pseudos
    if contenuInAllClass:
        with open(f'{output_directory}/pseudos.txt', 'a', encoding='utf-8') as fichier:
            for pseudos in contenuInAllClass:
                contenu = pseudos.get_text(strip=True)
                fichier.write(contenu + '\n')
        print("Pseudos sauvegardés dans pseudos.txt.")
    else:
        print("Balises non trouvées")

