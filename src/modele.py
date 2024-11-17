import math
from scipy.stats import norm

class Modele:
    
    def probaCutJoueur(self, cut, moyenne, ecartType):
        if ecartType == None or moyenne == None:
            return False
        else:
            proba = norm.cdf(cut+0.49, loc = moyenne, scale = ecartType)
            return 1 - proba 

    def probaCutEquipe(self, cut , moyenne, ecartType):
        proba = norm.cdf(abs(cut) + 0.49 , loc = moyenne, scale = ecartType)
        if cut > 0 :
            return 1 - proba 
        else :
            return proba 
    
    def probaValide(self, proba, probaMin):
        return proba > probaMin
    
    def isJoueurRegulier(self, minutes, nbMinutesMin, frequence):
        minutes_sup = [minutes[i] for i in range(len(minutes)) if minutes[i] >= nbMinutesMin]
        return len(minutes_sup)/len(minutes) >= frequence

    def isJoueurTitulaire(self, nbMatch, nbMatchMin):
        return nbMatch >= nbMatchMin

    def isMatchUpValide(self, points, cut):
        for pt in points:
            if pt < cut :
                return False
        return True 
    
    def isProjectionValide(self, m_EquipeJoueur, m_EquipeAdverse, frequenceJoueur, cut):
        projection = (m_EquipeJoueur + m_EquipeAdverse)/2
        if frequenceJoueur * cut > projection:
            return True
        else :
            return False