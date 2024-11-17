from joueur import Joueur 
import statistics
from scipy.stats import norm
import math

class Equipe:
    
    def __init__(self, fichier_equipes, fichier_stats):
        self.fichier_equipes = fichier_equipes
        self.data = self.lires_equipes()
        self.Joueur = Joueur(fichier_stats)
    
    def lires_equipes (self):
        equipes_data = {}
        with open(self.fichier_equipes, 'r') as file :
            lines = file.readlines()
            for line in lines :
                parts = line.strip().split(';')
                nom_equipe = parts[0]
                if nom_equipe not in equipes_data:
                    equipes_data[nom_equipe] = []
                
                i=1
                while i< len(parts):
                    joueur = parts[i]
                    equipes_data[nom_equipe].append(joueur)
                    i+=1 
        
        return equipes_data

    def getJoueursEquipe(self, Equipe):
        #Cette methode renvoi les joueurs d'une equipe donné en paramètre 
        Equipes = self.data
        if Equipe not in Equipes:
            return None
        else: 
            return Equipes[Equipe]

    def getEquipeJoueur(self, joueur):
        #Cette methode renvoi l'equipe d'un joueur donné en paramètre 
        Equipes = self.data
        for Equipe in Equipes:
            joueurs = self.getJoueursEquipe(Equipe)
            if joueur in joueurs:
                return Equipe

    def joueurMaxMatch(self, Equipe):
        #print(Equipe)
        joueurs = self.getJoueursEquipe(Equipe)
        max = 1 
        for joueur in joueurs :
            if self.Joueur.getNbMatch(joueur) > max :
                max = self.Joueur.getNbMatch(joueur)
                j_max = joueur 
        return j_max 
    
    def getPtsEquipe(self, Equipe):
        #cette méthode renvoi les points marqués par une equipe
        return self.Joueur.getPointsEquipe(self.joueurMaxMatch(Equipe))
        

    def getPtsEquipeEncaisse(self, Equipe):
        #cette méthode renvoi les points encaissés par une equipe
        return self.Joueur.getPointsEquipeContre(self.joueurMaxMatch(Equipe))
    
    def getPtsTotal(self , Equipe):
        ptsIn = self.getPtsEquipe(Equipe)
        ptsContre = self.getPtsEquipeEncaisse(Equipe)
        PtsTotal = [x + y for x, y in zip (ptsIn , ptsContre)]
        return PtsTotal    

    def getMoyenneDeuxEquipes(self, Equipe1, Equipe2):
        m_Equipe1 = statistics.mean(self.getPtsTotal(Equipe1))
        m_Equipe2 = statistics.mean(self.getPtsTotal(Equipe2))
        m_total = (m_Equipe1 + m_Equipe2)/2 
        return m_total

    def getEcartTypeDeuxEquipes(self, Equipe1, Equipe2):
        e_Equipe1 = statistics.stdev(self.getPtsTotal(Equipe1))
        e_Equipe2 = statistics.stdev(self.getPtsTotal(Equipe2))
        n_Equipe1 = len(self.getPtsTotal(Equipe1))
        n_Equipe2 = len(self.getPtsTotal(Equipe2))
        e_total = math.sqrt(((n_Equipe1 - 1) * e_Equipe1**2 + (n_Equipe2 - 1) * e_Equipe2**2) / (n_Equipe1 + n_Equipe2 - 2))
        return e_total

#--------------------------------------Avant Date--------------------------------------#
    def getPtsEquipeAvantDate(self, Equipe, date):
        return self.Joueur.getPointsEquipeAvantDate(self.joueurMaxMatch(Equipe), date)

    def getPtsEquipeEncaisseAvantDate(self, Equipe, date):
        return self.Joueur.getPointsEquipeContreAvantDate(self.joueurMaxMatch(Equipe), date)

    def getPtsTotalAvantDate(self, Equipe, date):
        ptsIn = self.getPtsEquipeAvantDate(Equipe, date)
        ptsContre = self.getPtsEquipeEncaisseAvantDate(Equipe, date)
        PtsTotal = [x + y for x,y in zip (ptsIn, ptsContre)]
        return PtsTotal

    def getMoyenneDeuxEquipesAvantDate(self, Equipe1, Equipe2, date):
        m_Equipe1 = statistics.mean(self.getPtsTotalAvantDate(Equipe1, date))
        m_Equipe2 = statistics.mean(self.getPtsTotalAvantDate(Equipe2, date))
        m_total = (m_Equipe1 + m_Equipe2)/2
        return m_total

    def getEcartTypeDeuxEquipesAvantDate(self, Equipe1, Equipe2, date):
        e_Equipe1 = statistics.stdev(self.getPtsTotalAvantDate(Equipe1, date))
        e_Equipe2 = statistics.stdev(self.getPtsTotalAvantDate(Equipe2, date))
        n_Equipe1 = len(self.getPtsTotalAvantDate(Equipe1, date))
        n_Equipe2 = len(self.getPtsTotalAvantDate(Equipe2, date))
        e_total = math.sqrt(((n_Equipe1 - 1) * e_Equipe1**2 + (n_Equipe2 - 1) * e_Equipe2**2) / (n_Equipe1 + n_Equipe2 - 2))
        return e_total   