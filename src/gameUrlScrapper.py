from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re 
from pathManager import PathManager

P = PathManager()

class GameUrlScrapper:

    def __init__(self, url):
        chrome_options = Options()
        # Spécifier le répertoire des données utilisateur Chrome
        user_data_dir = '~/.config/google-chrome'
        profile_name = "Profile 1"  # Nom du profil spécifique
        # Utiliser le répertoire de données utilisateur et le profil spécifique
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument(f"--profile-directory={profile_name}")
        chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU
        chrome_options.add_argument("--no-first-run")  # Éviter les invites lors du premier démarrage
        fichier_extension = P.getFichierDossierExtension('idontcareaboutcookies.crx')
        chrome_options.add_extension(fichier_extension)
        service = ChromeService(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service = service, options =chrome_options)
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.bypass()

    def bypass(self):
        self.driver.implicitly_wait(5)
        #cette fonction sert à passer les cookies et les pop up  
        #Fermer la fenêtre pop-up si elle apparaît
        try:
            self.driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)
        except Exception as e:
            print("Échec lors de la tentative de fermeture du pop-up avec la touche 'Échap'.")

        self.driver.implicitly_wait(5)
    
    def getUrls(self):
        urls = []
        heights = []
        try:
            middle_column_element = self.driver.find_element(By.XPATH, '//*[@data-testid="middleColumn"]')
            sections = middle_column_element.find_elements(By.XPATH, ".//*[contains(@data-testid, 'match-card')]")
            for section in sections :
                important_link_element = section.find_element(By.XPATH, ".//a")  # Modifiez ce sélecteur si nécessaire
                important_link = important_link_element.get_attribute('href')
                urls.append(important_link)
                    
        except Exception as e:
            print(f'Erreur lors de la récupération de l\'élément middleColumn: {e}')
        
        self.driver.quit()
        return urls