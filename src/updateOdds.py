from gameDataManager import GameDataManager
from pathManager import PathManager
from gameUrlScrapper import GameUrlScrapper
from time import sleep

P = PathManager()

class UpdateOdds : 
    def __init__(self, url, chemin, nb_match):
        self.nb_match = nb_match
        G = GameUrlScrapper(url)
        self.urls = G.getUrls()
        self.chemin = chemin
        self.categorie = ['Points', 'Rebonds', 'Passes']    
    
    def write_match(self, data, n):
        teams = data[0]
        PointsMatch = data[1]
        players = data[2]
        with open(self.chemin, "a") as fichier :
            nb_match = ''.join(['Match', str(n)])
            fichier.write(nb_match)
            fichier.write(';')
            for team in teams:
                fichier.write(team)
                fichier.write(';')
            fichier.write('PointsMatch')
            for point in PointsMatch:
                for p in point:
                    fichier.write(';')
                    fichier.write(str(p))
            for p in players:
                if p not in self.categorie and isinstance(p, str):
                    fichier.write('\n')
                    fichier.write(p)
                else:
                    fichier.write(';')
                    fichier.write(str(p))
            fichier.write('\n')
        
    def updateFileOdds(self):
        for i in range(self.nb_match):
            G = GameDataManager(self.urls[i])
            try:
                data = G.getDataGame()
                self.write_match(data, i + 1)
                print(f'{i+1}/{self.nb_match}')
            except Exception as e:
                print(f"Erreur pour l'URL {self.urls[i]}: {e}")
            sleep(2)
        print('Le fichier a bien été enregistré')


#url = 'https://www.winamax.fr/paris-sportifs/sports/2/15/177'


#urls = ['https://www.winamax.fr/paris-sportifs/match/52629931']
#urls = ['https://www.winamax.fr/paris-sportifs/match/52630683', 'https://www.winamax.fr/paris-sportifs/match/52630739', 'https://www.winamax.fr/paris-sportifs/match/52630423', 'https://www.winamax.fr/paris-sportifs/match/52630503', 'https://www.winamax.fr/paris-sportifs/match/52631655', 'https://www.winamax.fr/paris-sportifs/match/52630647']
#chemin = P.getFichierCotes('03-11-2024')
#W = Writer(urls, chemin)
#W.write_file()
#print(urls)
