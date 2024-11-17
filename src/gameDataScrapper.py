from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pathManager import PathManager
from time import sleep  


#Cette constante represente la cote minimum à recuperer 
CONST_COTEMIN = 1.3

P = PathManager()

class GameDataScrapper:

    def __init__(self, url):
        chrome_options = Options()
        # Spécifier le répertoire des données utilisateur Chrome
        user_data_dir = '~/.config/google-chrome'
        profile_name = "Profile 1"  # Nom du profil spécifique
        # Utiliser le répertoire de données utilisateur et le profil spécifique
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument(f"--profile-directory={profile_name}")
        chrome_options.add_argument("--no-first-run")  # Éviter les invites lors du premier démarrage
        chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU
        fichier_extension = P.getFichierDossierExtension('idontcareaboutcookies.crx')
        chrome_options.add_extension(fichier_extension)
        service = ChromeService(ChromeDriverManager().install())
        self.url = url
        
        self.driver = webdriver.Chrome(service = service, options =chrome_options)
        try:
            print("Chargement de l'URL...")
            self.driver.get(self.url)
            print("URL chargée.")
        except Exception as e:
            print(f"Erreur lors du chargement de l'URL : {e}")
        
        self.driver.execute_script("window.focus();")
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

#-------------------------------------------------------------------Carré-------------------------------------------------------------------#
        
    def getClassCarre(self, categorie):
        try:
            sections = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{categorie}')]")
            useless_section = []
            for section in sections:
                #self.driver.execute_script("arguments[0].scrollIntoView(true);", section)
                if section.get_attribute('class') in useless_section:
                    continue
                parent_element = section.find_element(By.XPATH, "./..")
                siblings = parent_element.find_elements(By.XPATH, "./preceding-sibling::* | ./following-sibling::*")
                if len(siblings) == 1:
                    sibling = siblings[0]
                    fils = sibling.find_element(By.XPATH, './*/*/*')
                    converted_fils = "." + fils.get_attribute('class').replace(" ", ".")
                    return converted_fils
                else :
                    useless_section.append(section.get_attribute('class')) 
        except Exception as e :
            print(f'Plus delements {categorie}')

    def ClickCarre(self):
        #cliquer sur le bouton avec les quatre petits carrés
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".sc-jiPWxV.cDBJAb"))
            )
            button.click()

        except Exception as e:
            print("Le bouton carré n'a pas pu etre cliqué.")
            self.driver.quit()
            raise e

    def ClickCarreCategorie(self, categorie):
        class_bouton = self.getClassCarre(categorie)
        try:
            buttonsCarre = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, class_bouton))
            )
            for button in buttonsCarre:
                child_text = button.find_element(By.XPATH, '../../../../*[1]/*[1]').text
                if categorie in child_text:
                    ActionChains(self.driver).move_to_element(button).perform()
                    button.click()
                    break
        except Exception as e :
            print("rien trouvé")
            self.driver.quit()
            raise e
        
#-------------------------------------------------------------------Selections-------------------------------------------------------------------#
    def getClassSelections(self, categorie):
        try:
            sections = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{categorie}')]")
            useless_section = []
            for section in sections:
                if section.get_attribute('class') in useless_section :
                    continue
                try:
                    parent_element = section.find_element(By.XPATH, "./../../../../*[2]")
                    siblings = parent_element.find_elements(By.XPATH, "./*[2]")
                    if len(siblings) != 0 : 
                        sibling = siblings[0]
                        bouton = sibling.find_element(By.XPATH, './*[2]/*')
                        bouton_converted = "." + bouton.get_attribute('class').replace(" ", ".")
                        return bouton_converted
                    else : 
                        useless_section.append(section.get_attribute('class')) 
                except NoSuchElementException:
                    print('Pas de bouton selection trouvé ; le programme continue')
                    return None
        except Exception as e :
            print(f'Plus delements {categorie}')

    def ClickSelections(self):
        #cliquer sur le bouton pour afficher toutes les selections 
        try:
            button_selections = WebDriverWait(self.driver,10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".sc-gMZIbH.DpfRO"))
            )
            button_selections.click()
        
        except Exception as e:
            print("Le bouton pour afficher toutes les sections n'a pas pu etre cliqué ")
            self.driver.quit()
            raise e

    def ClickSelectionsCategorie(self, categorie):
        class_bouton = self.getClassSelections(categorie)
        if class_bouton != None:
            try : 
                buttonsSelection = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, class_bouton))
                )
                for button in buttonsSelection:
                    child_text = button.find_element(By.XPATH, '../../../../*[1]/*[1]').text
                    if categorie in child_text:
                        ActionChains(self.driver).move_to_element(button).perform()
                        button.click()
                        break
            
            except Exception as e :
                print("fail selec")
                self.driver.quit()
                raise e 
 
  #-------------------------------------------------------------------Template-------------------------------------------------------------------#
    def getClassTemplatesPointsMatch(self, categorie):
        try : 
            class_list = []
            sections = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{categorie}')]")
            useless_section = []
            for section in sections:
                parent = section.find_element(By.XPATH, './../../../..')
                siblings = parent.find_elements(By.XPATH, './*')
                if len(siblings) == 3:
                    sibling = siblings[1]
                    template = sibling.find_element(By.XPATH, './*[2]/*')
                    class_list.append(template.get_attribute('class'))
                    intermediate_div = template.find_element(By.XPATH, './*')
                    class_list.append(intermediate_div.get_attribute('class'))
                    events = intermediate_div.find_element(By.XPATH, './*')
                    class_list.append(events.get_attribute('class'))
                    cuts = events.find_elements(By.XPATH, './*')
                    if len(cuts) == 1 :
                        cut = cuts[0]
                        cut_class = events.find_element(By.XPATH, ".//*[contains(text(), 'Plus de')]")
                        class_list.append(cut_class.get_attribute('class'))
                        cote_class = cut_class.find_element(By.XPATH, './../*[3]/*[1]')
                        class_list.append(cote_class.get_attribute('class'))
                        return class_list
        except Exception as e :
            print('Plus delements nombre de points')    
            self.driver.quit()
            raise e 

 #-------------------------------------------------------------------Menu-------------------------------------------------------------------#
    def getClassMarqueurs(self):
        classes = []
        try:
            middle_column_element = self.driver.find_element(By.XPATH, '//*[@data-testid="middleColumn"]')
            #print(middle_column_element.get_attribute('class'))
            marqueurs = middle_column_element.find_element(By.XPATH, "//*[contains(text(), 'Marqueurs')]")
            #print(marqueurs.get_attribute('class'))
            #span_marqueurs = marqueurs.find_element(By.XPATH,'./*[1]')
            #class_marqueurs = '.' + marqueurs.get_attribute('class').replace('  ', '.').replace(' ', '.')
            #span_marqueurs = 'span.' + span_marqueurs.get_attribute('class').replace(' ', '.')
            papa = marqueurs.find_element(By.XPATH, '..')
            enfants = papa.find_elements(By.XPATH, './*')
            classes.append('.' + enfants[0].get_attribute('class').replace('  ', '.').replace(' ', '.'))
            classes.append('span.' + enfants[1].get_attribute('class').replace(' ', '.'))
            #classes.append(span_marqueurs)
            #print(classes)
            return classes

        except Exception as e:
            print(f'Erreur lors de la récupération de l\'élément middleColumn: {e}')

    def ClickMarqueurs(self):
        classes = self.getClassMarqueurs()
        #print(classes)
        class_marqueurs = classes[0]
        span_marqueurs = classes[1]
        #selector = f"{class_marqueurs} > {span_marqueurs}"
        selector = 'span' + class_marqueurs
        try:
            # Sélectionner le bouton 'Marqueurs' en combinant plusieurs sélecteurs
            button_marqueurs = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector ))
            )
            #print("Élément trouvé et cliquable")
            button_marqueurs.click()
        except Exception as e:
            print("Le bouton 'marqueurs' n'a pas pu être cliqué : ", e)
            self.driver.quit()

        self.driver.implicitly_wait(5)
    

    def getClassBoutonStatsJoueurs(self):
        class_stats = []
        try:
            middle_column_element = self.driver.find_element(By.XPATH, '//*[@data-testid="middleColumn"]')
            statsJoueurs = middle_column_element.find_element(By.XPATH, "//*[contains(text(), 'Stats joueurs')]")
            #print(statsJoueurs.get_attribute('class'))
            papa = statsJoueurs.find_element(By.XPATH, '..')
            enfants = papa.find_elements(By.XPATH, './*')
            class_stats.append('.' + enfants[0].get_attribute('class').replace('  ', '.').replace(' ', '.'))
            class_stats.append('span.' + enfants[1].get_attribute('class').replace(' ', '.'))           
            #span_statsJoueurs = statsJoueurs.find_element(By.XPATH,'./*[1]')
            #class_statsJoueurs = '.' + statsJoueurs.get_attribute('class').replace('  ', '.').replace(' ', '.')
            #class_stats.append(class_statsJoueurs)
            #span_statsJoueurs = '.' + span_statsJoueurs.get_attribute('class').replace(' ', '.')
            #class_stats.append(span_statsJoueurs)
            return class_stats
        
        except Exception as e:
            print(f'Erreur lors de la récupération de l\'élément middleColumn: {e}')

    def ClickStatsJoueurs(self):
        class_stats = self.getClassBoutonStatsJoueurs()
        class_stats_joueurs = class_stats[0]
        span_stats_joueurs = class_stats[1]
        #selector = f"{class_stats_joueurs} > {span_stats_joueurs}"
        selector = 'span' + class_stats_joueurs
        try : 
            buttonStats = self.driver.find_elements(By.CSS_SELECTOR, selector)
            for button in buttonStats:
                if 'Stats joueurs' in button.text : 
                    button.click()
                    return 
        except Exception as e:
            print("Échec stats")
        
#-------------------------------------------------------------------Teams-------------------------------------------------------------------#
    def getDataTeams(self):
        data = []
        self.ClickCarreCategorie('Nombre de points')
        self.driver.implicitly_wait(5)
        self.ClickSelectionsCategorie('Nombre de points')
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data.append(self.getTeams())
        data.append(self.getCutCoteMatch(soup))
        self.driver.quit()
        return data

    def getTeams(self):
        try:
            middle_column_element = self.driver.find_element(By.XPATH, '//*[@data-testid="middleColumn"]')
            team1 = middle_column_element.find_element(By.XPATH, './*/*[3]/*[2]/*[1]/*[2]/*[1]/*[1]/*[1]')
            team2 = middle_column_element.find_element(By.XPATH, './*/*[3]/*[2]/*[1]/*[2]/*[1]/*[3]/*[2]')
            return team1.text, team2.text
        except Exception as e:
            print(f'Erreur lors de la récupération de l\'élément middleColumn: {e}')

    def getCutCoteMatch(self, soup):
        cuts_list = []
        cotes_list = []
        PointsMatch = []
        
        class_list = self.getClassTemplatesPointsMatch('Nombre de points')
        
        class_template = class_list[0]
        class_intermediaire = class_list[1]
        class_events = class_list[2]
        class_cut = class_list[3]
        class_cote = class_list[4]

        # Localiser la section "Nombre de points"
        points_section = soup.find(class_=class_template)

        if points_section:
            # Localiser la div intermédiaire
            intermediate_div = points_section.find(class_=class_intermediaire)
            
            if intermediate_div:
                # Récupérer toutes les occurrences de la classe "sc-dsxidx kqUbIh" sous cette div
                events = intermediate_div.find_all(class_=class_events)
                
                # Parcourir chaque occurrence pour récupérer les cuts et les cotes
                for index, event in enumerate(events):
                    
                    # Récupérer les cuts et les cotes
                    cuts = event.find_all(class_=class_cut)
                    odds = event.find_all(class_=class_cote)
                    for cut in cuts:
                        cuts_list.append(cut.text)
                    
                    for odd in odds:
                        cotes_list.append(odd.text)
            else:
                print("Div intermédiaire 'sc-iUVXnI glFavy' non trouvée.")
        else:
            print("Section 'Nombre de points' non trouvée.")
        
        i=0
        while i<len(cuts_list):
            if 'Moins' in cuts_list[i] and float(cotes_list[i].replace(',','.')) < CONST_COTEMIN:
                parts = cuts_list[i].split()
                clean_cut = 0 - float(parts[-1].replace(',', '.'))
                PointsMatch.append((clean_cut,float(cotes_list[i].replace(',','.'))))
            if 'Plus' in cuts_list[i] and float(cotes_list[i].replace(',','.')) < CONST_COTEMIN:
                parts = cuts_list[i].split()
                clean_cut =float(parts[-1].replace(',', '.'))
                PointsMatch.append((clean_cut,float(cotes_list[i].replace(',','.'))))
            i+=1
        
        self.driver.quit()
        #print(PointsMatch)
        return PointsMatch

#-------------------------------------------------------------------Players-------------------------------------------------------------------#
    def getClassPointsJoueurs(self):
        try : 
            class_list = []
            middle_column_element = self.driver.find_element(By.XPATH, '//*[@data-testid="middleColumn"]')
            template = middle_column_element.find_element(By.XPATH, "//*[contains(@class, 'bet-group-template')]")
            #print(temp.get_attribute('class'))
            #template = middle_column_element.find_element(By.XPATH, './*[1]/*[5]/*[2]/*[1]/*[1]/*[1]/*[1]/*[1]/*[2]/*[2]/*[1]')
            class_list.append(template.get_attribute('class'))
            class_intermediaire = template.find_element(By.XPATH, './*[1]')
            class_list.append(class_intermediaire.get_attribute('class'))
            class_events = class_intermediaire.find_element(By.XPATH, './*[1]')
            class_list.append(class_events.get_attribute('class'))
            class_player_name = class_events.find_element(By.XPATH, './*[1]/*[1]/*[2]/*[1]')
            class_list.append(class_player_name.get_attribute('class'))
            #print(class_list)
            class_cut = class_events.find_element(By.XPATH, ".//*[contains(text(), 'Plus de')]")
            class_list.append(class_cut.get_attribute('class'))
            class_cote = class_cut.find_element(By.XPATH, './../*[3]/*[1]')
            class_list.append(class_cote.get_attribute('class'))
            return class_list

        except Exception as e :
            print('Categorie Points non trouvee')    
            self.driver.quit()
            raise e 

    def getClassRebondsJoueurs(self):
        class_list = []
        categorie = 'Nombre de rebonds du joueur (paliers)'
        try : 
            sections = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{categorie}')]")
            for section in sections:
                parent = section.find_element(By.XPATH, './../../../..')
                template = parent.find_element(By.XPATH, './*[2]/*[2]/*[1]')
                class_list.append(template.get_attribute('class'))
                intermediaire = template.find_element(By.XPATH, './*[1]')
                class_list.append(intermediaire.get_attribute('class'))
                event = intermediaire.find_element(By.XPATH, './*[1]')
                class_list.append(event.get_attribute('class'))
                class_player_name = event.find_element(By.XPATH, './*[1]/*[1]/*[2]/*[1]')
                class_list.append(class_player_name.get_attribute('class'))
                class_cut = event.find_element(By.XPATH, ".//*[contains(text(), 'Plus de')]")
                class_list.append(class_cut.get_attribute('class'))
                class_cote = class_cut.find_element(By.XPATH, './../*[3]/*[1]')
                class_list.append(class_cote.get_attribute('class'))
                return class_list

        except Exception as e :
            print('categorie Rebonds non trouve')

    def getClassPassesJoueurs(self):
        class_list = []
        categorie = 'Nombre de passes décisives du joueur (paliers)'
        try : 
            sections = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{categorie}')]")
            for section in sections:
                parent = section.find_element(By.XPATH, './../../../..')
                template = parent.find_element(By.XPATH, './*[2]/*[2]/*[1]')
                class_list.append(template.get_attribute('class'))
                intermediaire = template.find_element(By.XPATH, './*[1]')
                class_list.append(intermediaire.get_attribute('class'))
                event = intermediaire.find_element(By.XPATH, './*[1]')
                class_list.append(event.get_attribute('class'))
                class_player_name = event.find_element(By.XPATH, './*[1]/*[1]/*[2]/*[1]')
                class_list.append(class_player_name.get_attribute('class'))
                class_cut = event.find_element(By.XPATH, ".//*[contains(text(), 'Plus de')]")
                class_list.append(class_cut.get_attribute('class'))
                class_cote = class_cut.find_element(By.XPATH, './../*[3]/*[1]')
                class_list.append(class_cote.get_attribute('class'))
                return class_list

        except Exception as e :
            print('Categorie Passes non trouve')


    def getPointsPlayers(self):
        dataPlayers = []
        l = []
        categorie = 'Nombre de points du joueur (paliers)'
        self.driver.implicitly_wait(5)
        self.ClickMarqueurs()
        self.driver.implicitly_wait(5)
        self.ClickCarreCategorie(categorie)
        self.driver.implicitly_wait(5)
        self.ClickSelectionsCategorie(categorie)
        
        class_list = self.getClassPointsJoueurs()
        class_template = class_list[0]
        class_intermediaire = class_list[1]
        class_events = class_list[2]
        class_player = class_list[3]
        class_cut = class_list[4]
        class_cote = class_list[5]
        
        
        html = self.driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        points_section = soup.find(class_= class_template)

        if points_section:
            # Localiser la div intermédiaire si elle existe
            # (adaptation, si nécessaire, remplace par la classe réelle utilisée)
            intermediate_div = points_section.find(class_= class_intermediaire)
            if intermediate_div:
                # Récupérer toutes les occurrences de la classe "sc-dsxidx kqUbIh" sous cette div
                events = intermediate_div.find_all(class_= class_events)        
                # Parcourir chaque occurrence pour récupérer les joueurs, cuts et cotes
                for index, event in enumerate(events):
                    
                    # Récupérer le nom du joueur
                    player_name = event.find(class_= class_player).text
                    

                    # Récupérer les cuts et les cotes
                    cuts = event.find_all(class_=class_cut)
                    odds = event.find_all(class_=class_cote)
                    i = 0 

                    if float(odds[i].text.replace(',','.')) > CONST_COTEMIN :
                        continue
                    else : 
                        l.append(player_name)
                        l.append('Points')

                    while i<len(cuts):
                        if float(odds[i].text.replace(',','.')) < CONST_COTEMIN :
                            parts = cuts[i].text.split()
                            clean_cut = float(parts[-1].replace(',','.'))
                            clean_odd = float(odds[i].text.replace(',','.'))
                            l.append(clean_cut)
                            l.append(clean_odd)
                            i+=1
                        else:
                            i+=1 



            else:
                print("Div intermédiaire 'sc-iUVXli gLfavY' non trouvée.")
        else:
            print("Section 'Nombre de points' non trouvée.")
        self.driver.quit()
        return l 

    def getRebondsPlayers(self):
        RebondsPlayers = []
        categorie = 'Nombre de rebonds du joueur (paliers)'

        #self.ClickStatsJoueurs()
        self.ClickCarreCategorie(categorie)
        self.driver.implicitly_wait(5)
        self.ClickSelectionsCategorie(categorie)

        class_list = self.getClassRebondsJoueurs()
        class_template = class_list[0]
        class_intermediaire = class_list[1]
        class_events = class_list[2]
        class_player = class_list[3]
        class_cut = class_list[4]
        class_cote = class_list[5]
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        sections = soup.find_all(class_=class_template)
        for section in sections : 
            parent_section = section.find_parent().find_parent().find_parent()
            first_child = parent_section.find_all(recursive=False)[0]
            nom_section = first_child.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0]

            if 'Nombre de rebonds du joueur (paliers)' in nom_section:
                rebonds_section = section
                    # Localiser la div intermédiaire
                intermediate_div = rebonds_section.find(class_=class_intermediaire)
                        
                if intermediate_div:
                    events = intermediate_div.find_all(class_=class_events)        
                    for index, event in enumerate(events):
                                
                        # Récupérer le nom du joueur
                        player_name = event.find(class_=class_player).text
                        # Récupérer les cuts et les cotes
                        cuts = event.find_all(class_=class_cut)
                        odds = event.find_all(class_=class_cote)         
                        i = 0 
                        
                        if float(odds[i].text.replace(',','.')) > CONST_COTEMIN :
                            continue
                        else:
                            RebondsPlayers.append(player_name)
                            RebondsPlayers.append('Rebonds')
                        
                        
                        while i<len(cuts):
                            if float(odds[i].text.replace(',','.')) < CONST_COTEMIN :
                                parts = cuts[i].text.split()
                                clean_cut = float(parts[-1].replace(',','.'))
                                clean_odd = float(odds[i].text.replace(',','.'))
                                RebondsPlayers.append(clean_cut)
                                RebondsPlayers.append(clean_odd)
                                i+=1
                            else:
                                i+=1 

                else:
                    print("Div intermédiaire 'sc-iUVXli gLfavY' non trouvée.") 

                break
        return RebondsPlayers

    def getPassesPlayers(self):
        PassesPlayers = []
        #self.ClickStatsJoueurs()
        categorie = 'Nombre de passes décisives du joueur (paliers)'
        self.ClickCarreCategorie(categorie)
        self.driver.implicitly_wait(5)
        self.ClickSelectionsCategorie(categorie)
        self.driver.implicitly_wait(5)

        class_list = self.getClassPassesJoueurs()
        class_template = class_list[0]
        class_intermediaire = class_list[1]
        class_events = class_list[2]
        class_player = class_list[3]
        class_cut = class_list[4]
        class_cote = class_list[5]
        
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        sections = soup.find_all(class_=class_template)
        for section in sections : 
            parent_section = section.find_parent().find_parent().find_parent()
            first_child = parent_section.find_all(recursive=False)[0]
            nom_section = first_child.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0]

            if 'Nombre de passes décisives du joueur (paliers)' in nom_section:
                passes_section = section
                    # Localiser la div intermédiaire
                intermediate_div = passes_section.find(class_=class_intermediaire)
                        
                if intermediate_div:
                    events = intermediate_div.find_all(class_=class_events)        
                    for index, event in enumerate(events):
                                
                        # Récupérer le nom du joueur
                        player_name = event.find(class_=class_player).text
                        
                        # Récupérer les cuts et les cotes
                        cuts = event.find_all(class_=class_cut)
                        odds = event.find_all(class_=class_cote)         
                        
                        i = 0
                        
                        if float(odds[i].text.replace(',','.')) > CONST_COTEMIN:
                            continue
                        else : 
                            PassesPlayers.append(player_name)
                            PassesPlayers.append('Passes')

                        while i<len(cuts):
                            if float(odds[i].text.replace(',','.')) < CONST_COTEMIN :
                                parts = cuts[i].text.split()
                                clean_cut = float(parts[-1].replace(',','.'))
                                clean_odd = float(odds[i].text.replace(',','.'))
                                PassesPlayers.append(clean_cut)
                                PassesPlayers.append(clean_odd)
                                i+=1
                            else:
                                i+=1 

                else:
                    print("Div intermédiaire 'sc-iUVXli gLfavY' non trouvée.") 

                break
        return PassesPlayers


    def getStatsPlayers(self):
        stats = []
        self.ClickStatsJoueurs()
        self.driver.implicitly_wait(5)
        stats.append(self.getRebondsPlayers())
        self.driver.implicitly_wait(5)
        stats.append(self.getPassesPlayers())
        self.driver.quit()
        return stats

#url = 'https://www.winamax.fr/paris-sportifs/match/52629931'

#d = []
#url = 'https://www.winamax.fr/paris-sportifs/match/46601551'
#M = GameDataScrapper(url)
#print(M.getStatsPlayers())
#sleep(5)
#P = GameDataScrapper(url)
#d.append(P.getPointsPlayers())
#S = GameDataScrapper(url)
#d.append(S.getStatsPlayers())
#print(d)
#G = GameDataScrapper(url)
#print(G.getStatsPlayers())