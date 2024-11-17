from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from pathManager import PathManager
import pandas as pd
from bs4 import BeautifulSoup
import os

P = PathManager()

file_path = P.getFichierCotes('tab')

class UpdateLinks:
    def __init__(self, url):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # Exécute Chrome en mode headless si nécessaire
        chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = ChromeService(ChromeDriverManager().install())
        fichier_extension = P.getFichierDossierExtension('idontcareaboutcookies.crx')
        chrome_options.add_extension(fichier_extension)
        self.driver = webdriver.Chrome(service = service, options =chrome_options)
        self.url = url
        self.driver.get(self.url)
        



    def getLink(self, nom):
        try:
            self.driver.implicitly_wait(10)
            barre_recherche = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'form-control.mr-sm-2.ui-autocomplete-input'))
            )
            barre_recherche.clear()
            barre_recherche.send_keys(nom)
            
            self.driver.implicitly_wait(10)
            time.sleep(2)  # Attendre un court instant pour que les suggestions se chargent

            body_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body'))
            )
            player_link = WebDriverWait(body_element, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "player-search")]'))
            )
            link = player_link.get_attribute('href')
            self.driver.get(link)
            clean_link = self.driver.current_url
            link_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'equipe')]"))
            )
            link_urls = [element.get_attribute('href') for element in link_elements]
            link_team = link_urls[1]

            #self.driver.quit()
            return [clean_link, link_team]
        except Exception as e:
            print(f"Aucune suggestion trouvée pour {nom} : {e}")
            #self.driver.quit()
            return
# Utilisation de la nouvelle méthode
#url = 'https://www.proballers.com/fr/basketball/equipe/115/minnesota-timberwolves/calendrier'
#update_links = UpdateLinks(url)
#update_links.getPlayers()


class UpdateErrorsLinks:

    def __init__(self, url):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # Exécute Chrome en mode headless si nécessaire
        chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = ChromeService(ChromeDriverManager().install())
        fichier_extension = P.getFichierDossierExtension('idontcareaboutcookies.crx')
        chrome_options.add_extension(fichier_extension)
        self.driver = webdriver.Chrome(service = service, options =chrome_options)
        self.url = url
        self.driver.get(self.url)
    
    
    def getTeam(self):
        try:
            self.driver.implicitly_wait(5)
            # Utilisation d'attentes explicites pour s'assurer que les éléments sont présents
            link_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'equipe')]"))
            )
            
            # Récupérer les URLs des liens
            link_urls = [element.get_attribute('href') for element in link_elements]

            # S'assurer qu'il y a au moins deux liens trouvés
            if len(link_urls) < 2:
                print("Moins de deux liens trouvés pour l'équipe")
                self.driver.quit()
                return None
            
            link_team = link_urls[1]
            
            return link_team
        except Exception as e:
            print(f"Erreur lors de la récupération du lien de l'équipe : {e}")
            return None
        finally:
            self.driver.quit()


#joueurs = ['Jaden Ivey','Cameron Johnson', 'Tobias Harris', 'Jalen Duren', 'Tim Hardaway Jr.', 'Dorian Finney-Smith', 'Malik Beasley','Ziaire Williams', 'Ben Simmons']
#for joueur in joueurs:
#    print(s.getLink(joueur))

#liens = ['https://www.proballers.com/fr/basketball/joueur/41001/anthony-davis/matchs','https://www.proballers.com/fr/basketball/joueur/183633/nikola-jovic/matchs', 'https://www.proballers.com/fr/basketball/joueur/243787/jabari-smith-jr/matchs' ,'https://www.proballers.com/fr/basketball/joueur/257924/gradey-dick/matchs', 'https://www.proballers.com/fr/basketball/joueur/75027/santiago-aldama/matchs', 'https://www.proballers.com/fr/basketball/joueur/257054/brandon-miller/matchs','https://www.proballers.com/fr/basketball/joueur/192499/jalen-williams/matchs']
#for lien in liens :
#    s = UpdateErrorsLinks(lien)
#    print(s.getTeam())
#print(s.getTeam('https://www.proballers.com/fr/basketball/joueur/252855/anthony-black/matchs'))