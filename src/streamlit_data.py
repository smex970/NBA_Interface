from joueur import Joueur
from pathManager import PathManager
from paris import Paris
from combinaison import Combinaison 
from datetime import datetime

class streamlit_data:

    def __init__(self):
        self.P = PathManager()
        self.file_teams = self.P.getFichierEquipes()
        self.file_stats = self.P.getFichierDossierData('Statistiques_Joueurs.xlsx')
        self.Joueur = Joueur(self.file_stats)

    def getAllOddsStats(self, joueur, categorie, cut):
        odds = []
        stats =[]
        calc_odds =[]
        dates = []
        minutes = []
        fichiers = self.P.getFichiersCote()
        for fichier in fichiers:
            stat = self.Joueur.getStatDate(joueur, fichier, categorie)
            if stat != False:
                with open(self.P.getFichierCotes(fichier), 'r') as file:
                    joueurs = file.read()
                    if joueur in joueurs:
                        odd = self.extractCote(self.P.getFichierCotes(fichier), joueur, categorie, cut)
                        if odd != False:
                            odds.append(odd)
                        else :
                            odds.append(None)
                        Combi = Combinaison(self.file_stats, self.P.getFichierCotes(fichier), self.file_teams, 0.9)
                        calc_odd = 1/Combi.probaCutJoueurAvantDate(joueur, categorie, cut, fichier)
                        calc_odds.append(round(calc_odd, 4))
                        dates.append(fichier)
                        stats.append(stat)
                        minutes.append(self.Joueur.getMinDate(joueur, fichier))
        if len(dates) != 0:
            Dates_sorted, Cotes_sorted, Stats_sorted, Cal_Cote_sorted, Minutes_Sorted= zip(*sorted(zip(dates, odds, stats, calc_odds, minutes), key=lambda x: datetime.strptime(x[0], '%d-%m-%Y')))
            return Dates_sorted, Cotes_sorted, Stats_sorted, Cal_Cote_sorted, Minutes_Sorted
        else: 
            return None
   
    def extractCote(self, fichier, joueur, categorie, cut):        
        Pr = Paris(fichier, self.file_teams, self.file_stats)
        return Pr.getCoteJoueur(joueur, categorie, cut)
    
    def getAllResults(self, joueur, categorie):
        return self.getAllOddsStats(joueur, categorie, 1)[1]
        

    def getAllOdds(self, joueur, categorie, cut):        
        return self.getAllOddsStats(joueur, categorie, cut)[0]

    def getCalculatedOdd(self, joueur, categorie, cut):
        return self.getAllOddsStats(joueur, categorie, cut)[2]

    def getAllPlayers(self):
        players = []
        with open(self.P.getFichierJoueurs()) as file:
            file = file.readlines()
            for ligne in file:
                players.append(ligne.split(';')[0])
        return players
    
    def getAllDates(self, joueur, categorie, cut):
        return self.getAllOddsStats(joueur, categorie, cut)[3]

    def getAllCuts(self, joueur, categorie):
        cuts = []
        fichiers = self.P.getFichiersCote()
        for fichier in fichiers:
            paris = Paris(self.P.getFichierCotes(fichier), self.file_teams, self.file_stats)
            cut = paris.getCutJoueur(joueur, categorie)
            if cut != None:
                if len(cut) > 0 :
                    for c in cut :
                        if c not in cuts :
                            cuts.append(c)
                else : 
                    if cut not in cuts :
                        cuts.append(cut)
        return cuts
    
    def getAllMin(self, joueur, categorie, cut):
        return self.getAllOddsStats(joueur, categorie, cut)[4]

        
S = streamlit_data()
#PT = PathManager()
#file = PT.getFichierCotes('09-11-2024')
g = (S.getAllOddsStats('Nikola Vucevic', 'Points', 14.5))
#g = S.getAllCuts('LeBron James', 'Points')
#g = S.getAllMin('Nikola Vucevic')
print(g)
#for G in g :
#    print(G)
#print(S.getAllOdds('LeBron James', 'Points', 14.5))
#print(S.getAllResults('LeBron James', 'Points'))
#print(S.getAllResultsEvent('LeBron James', 'Points'))
#print(S.getAllPlayers())