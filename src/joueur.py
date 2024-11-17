import pandas as pd 
import math
from scipy.stats import norm
import statistics
from pathManager import PathManager
from date import Date

constSeuil = 0.70

class Joueur:
    
    cache_stats = {}

    def __init__(self, fichier_stats):
        self.fichierStats = fichier_stats
        self.Date = Date()
    
    def lireStats(self, joueur):
        #print(joueur)
        if joueur in self.cache_stats:
            return self.cache_stats[joueur]
        else:
            df_complet = pd.read_excel(self.fichierStats, sheet_name=joueur, skiprows=1)
            self.cache_stats[joueur] = df_complet
            return df_complet

    def lireStatsDate(self, joueur, date):
        df = self.lireStats(joueur)
        for index, row in df.iterrows():
            if self.Date.isSameDate(date, row['Date']):
                return row.tolist()
        return None
    
#-------------------------------------------------Lecture Fichier-------------------------------------------------
    def getPts(self, joueur):
        stats = self.lireStats(joueur)
        return stats.iloc[:, 3].tolist()
    
    def getRebonds(self, joueur):
        stats = self.lireStats(joueur)
        return stats.iloc[:, 4].tolist()

    def getPd(self, joueur):
        stats = self.lireStats(joueur)
        return stats.iloc[:, 5].tolist()
    
    def getMin(self, joueur):
        stats = self.lireStats(joueur)
        return stats.iloc[:, 6].tolist()
    
    def getTroisPoints(self, joueur):
        stats = self.lireStats(joueur)
        return stats.iloc[:, 7].tolist()
    
    def getStatsCat(self, joueur, categorie):
        if categorie == 'Points':
            return self.getPts(joueur)
        elif categorie == 'Passes' :
            return self.getPd(joueur)
        elif categorie == 'Rebonds':
            return self.getRebonds(joueur)
        else :
            return None

    def getNbMatch(self, joueur):
        stats = self.lireStats(joueur)
        return len(stats)
    
    def getDate(self, joueur):
        stats = self.lireStats(joueur)
        return stats.iloc[:, 1].tolist()
    
    def getPaniersTentes(self, joueur):
        stats = self.lireStats(joueur)
        deux_points = stats.iloc[:, 7]
        trois_points = stats.iloc[:, 8]
        paniers = 0
        assert(len(deux_points) == len(trois_points))
        
        for i in range(len(deux_points)):
            parties = deux_points[i].split('-')
            paniers += int(parties[1])
            parties = trois_points[i].split('-')
            paniers += int(parties[1])
        return paniers
    
    def getPaniersReussi(self, joueur):
        stats = self.lireStats(joueur)
        deux_points = stats.iloc[:, 7]
        trois_points = stats.iloc[:, 8]
        paniers = 0
        assert(len(deux_points) == len(trois_points))
        
        for i in range(len(deux_points)):
            parties = deux_points[i].split('-')
            paniers += int(parties[0])
            parties = trois_points[i].split('-')
            paniers += int(parties[0])
        return paniers
#-------------------------------------------------Statistiques avancées-------------------------------------------------
    def get_moyenne_sans_biais_forme(self, joueur, valeurs):
        minutes = self.getMin(joueur)[-5:]
        seuil = constSeuil * statistics.mean(minutes)
        valeurs = valeurs[-5:]
        valeurs_filtres = [valeurs[i] for i in range(len(minutes)) if minutes[i] >= seuil]
        return statistics.mean(valeurs_filtres)

    def moyenne_sans_biais(self, joueur, valeurs):
        minutes = self.getMin(joueur)
        seuil = constSeuil * statistics.mean(minutes)
        valeurs_filtres = [valeurs[i] for i in range(len(minutes)) if minutes[i] >= seuil]
        return statistics.mean(valeurs_filtres) 
    
    def ecart_type_sans_biais(self ,joueur ,valeurs):
        minutes = self.getMin(joueur)
        seuil = constSeuil * statistics.mean(minutes)
        valeurs_filtres = [valeurs[i] for i in range(len(minutes)) if minutes[i] >= seuil]
        if len(valeurs_filtres) >= 2:
            return statistics.stdev(valeurs_filtres)

    def getMoyenneSansBiais(self, joueur, categorie):
        if categorie == 'Points':
            return self.moyenne_sans_biais(joueur, self.getPts(joueur))
        
        if categorie == 'Rebonds':
            return self.moyenne_sans_biais(joueur, self.getRebonds(joueur))
        
        if categorie =='Passes':
            return self.moyenne_sans_biais(joueur, self.getPd(joueur))
        
        if categorie == 'TroisPoints':
            return self.moyenne_sans_biais(joueur, self.getTroisPoints(joueur))

    def getEcartTypeSansBiais(self, joueur, categorie):
        if categorie == 'Points':
            return self.ecart_type_sans_biais(joueur, self.getPts(joueur))
        
        if categorie == 'Rebonds':
            return self.ecart_type_sans_biais(joueur, self.getRebonds(joueur))
        
        if categorie =='Passes':
            return self.ecart_type_sans_biais(joueur, self.getPd(joueur))
        
        if categorie == 'TroisPoints':
            return self.ecart_type_sans_biais(joueur, self.getTroisPoints(joueur))

    def getMoyennePaniersReussi(self, joueur):
        paniers = self.getPaniersReussi(joueur)
        nbMatch = self.getNbMatch(joueur)
        return paniers/nbMatch
    
    def getPourcentageTir(self, joueur):
        stats = self.lireStats(joueur)
        tirs = stats.iloc[:, 9].tolist()
        return [int(float(t.strip('%'))) for t in tirs]

    def getRecord(self, joueur, cut, categorie):
        if categorie == 'Points':
            stats = self.getPts(joueur)
        if categorie == 'Passes': 
            stats = self.getPd(joueur)
        if categorie == 'Rebonds':
            stats = self.getRebonds(joueur)

        done = 0
        for s in stats : 
            if s > cut :
                done +=1 
        return str(str(done) + '/' + str(len(stats)))    
    
    def getPourcentageMoyenTir(self, joueur):
        return statistics.mean(self.getPourcentageTir(joueur))
#-------------------------------------------------Statistiques Equipes-------------------------------------------------
    def getPtsVsEquipe(self,joueur,Equipe):
        pts = []
        stats = self.lireStats(joueur)
        adversaires = stats.iloc[:, 0].tolist()
        ptsJoueur = self.getPts(joueur)
        i=0
        for adversaire in adversaires: 
            if Equipe in adversaire :
                pts.append(ptsJoueur[i])
            i+=1 
        return pts
    
    def getPourcentageMoyen(self, joueur):
        listePourcentage = []
        pointsEquipe = self.getPointsEquipe(joueur)
        pointsJoueuse = self.getPts(joueur)
        #penser à mettre un assert si les deux len sont different
        for i in range(len(pointsJoueuse)):
            listePourcentage.append(round(pointsJoueuse[i]/pointsEquipe[i],2))
        return statistics.mean(listePourcentage)        
    
    def getPointsEquipe(self, joueur):
        stats = self.lireStats(joueur)
        resultat = stats.iloc[:, 2].tolist()
        adversaires = stats.iloc[:, 0].tolist()
        points = []
        i = 0
        for jour in adversaires :
            if '@' in jour:
                pts_away = resultat[i].split('-')
                if len(pts_away) > 1 :
                    points.append(int(pts_away[1].strip()))
        
            else:
                pts = resultat[i].split('\n')
                if len(pts) > 1:
                    pts_home = pts[1].split('-')
                    if len(pts_home) > 1:
                        points.append(int(pts_home[0].strip()))
            i+=1 

        return points 

    def getPointsEquipeContre(self, joueur):
        stats = self.lireStats(joueur)
        resultat = stats.iloc[:, 2].tolist()
        adversaires = stats.iloc[:, 0].tolist()
        points = []
        i = 0
        for jour in adversaires :
            if '@' in jour:
                pts = resultat[i].split('\n')
                if len(pts) > 1:
                    pts_away = pts[1].split('-')
                    if len(pts_away) > 1 :
                        points.append(int(pts_away[0].strip()))
            else:
                pts_home = resultat[i].split('-')
                if len(pts_home) > 1 :
                    points.append(int(pts_home[1].strip()))
            i+=1
        return points
#-------------------------------------------------Statistiques Forme-------------------------------------------------
    def getRecordForme(self, joueur, cut, categorie):
        if categorie == 'Points':
            stats = self.getPts(joueur)
        if categorie == 'Passes': 
            stats = self.getPd(joueur)
        if categorie == 'Rebonds':
            stats = self.getRebonds(joueur)
        
        stats = stats[-5:]
        done = 0
        if len(stats) < 5:
            for s in stats :
                if s > cut:
                    done +=1
            return str(str(done) + '/' + str(5))

        for i in range(5):
            if stats[i] > cut : 
                done +=1 
        return str(str(done) + '/' + str(5))
    
    def getPourcentageForme(self, joueur):
        valeurs = self.getPourcentageTir(joueur)
        valeurs = valeurs[-5:]
        return statistics.mean(valeurs)

    def getMoyennePaniersReussiForme(self, joueur):
        stats = self.lireStats(joueur)
        deux_points = stats.iloc[:, 7]
        trois_points = stats.iloc[:, 8]
        paniers = 0
        assert(len(deux_points) == len(trois_points))
        if len(deux_points) < 5:
            for i in range(len(deux_points)):
                parties = deux_points[i].split('-')
                paniers += int(parties[0])
                parties = trois_points[i].split('-')
                paniers += int(parties[0])
            return paniers/len(deux_points)

        for i in range(5):
            parties = deux_points[i].split('-')
            paniers += int(parties[0])
            parties = trois_points[i].split('-')
            paniers += int(parties[0])
        return paniers/5

#--------------------------------------Avant Date--------------------------------------#
    def getPtsDate(self, joueur, date): #date au format dd-mm-aaaa
        DatesToTest = self.getDate(joueur)
        Points = self.getPts(joueur)
        assert(len(Points) == len(DatesToTest))
        for i in range(len(Points)):
            if self.Date.isSameDate(date, DatesToTest[i]):
                return Points[i]
        return False
    
    def getRebDate(self, joueur, date):
        DatesToTest = self.getDate(joueur)
        Rebonds = self.getRebonds(joueur)
        assert(len(Rebonds) == len(DatesToTest))
        for i in range(len(Rebonds)):
            if self.Date.isSameDate(date, DatesToTest[i]):
                return Rebonds[i]
        return False

    def getPdDate(self, joueur, date):
        DatesToTest = self.getDate(joueur)
        Passes = self.getPd(joueur)
        assert(len(Passes) == len(DatesToTest))
        for i in range(len(Passes)):
            if self.Date.isSameDate(date, DatesToTest[i]):
                return Passes[i]
        return False

    def getStatDate(self, joueur, date, categorie):
        if categorie == 'Points':
            return self.getPtsDate(joueur, date)
        elif categorie == 'Passes':
            return self.getPdDate(joueur, date)
        elif categorie == 'Rebonds':
            return self.getRebDate(joueur, date)
        else:
            return None

    def getPtsAvantDate(self, joueur, date):
        PtsAvantDate = []
        Pts = self.getPts(joueur)
        DatesToTest = self.getDate(joueur)
        for i in range(len(Pts)):
            if self.Date.estAvant(date, DatesToTest[i]):
                PtsAvantDate.append(Pts[i])
        return PtsAvantDate

    def getPdAvantDate(self, joueur, date):
        PdAvantDate = []
        Pd = self.getPd(joueur)
        DateToTest = self.getDate(joueur)
        for i in range(len(Pd)):
            if self.Date.estAvant(date, DateToTest[i]):
                PdAvantDate.append(Pd[i])
        return PdAvantDate

    def getRebAvantDate(self, joueur, date):
        RebAvantDate = []
        Reb = self.getRebonds(joueur)
        DateToTest = self.getDate(joueur)
        for i in range(len(Reb)):
            if self.Date.estAvant(date, DateToTest[i]):
                RebAvantDate.append(Reb[i])
        return RebAvantDate

    def getMinAvantDate(self, joueur, date):
        MinAvantDate = []
        Min = self.getMin(joueur)
        DateToTest = self.getDate(joueur)
        for i in range(len(Min)):
            if self.Date.estAvant(date, DateToTest[i]):
                MinAvantDate.append(Min[i])
        return MinAvantDate

    def getNbMatchAvantDate(self, joueur, date):
        NbMatchAvantDate = 0
        DateToTest = self.getDate(joueur)
        for i in range(len(DateToTest)):
            if self.Date.estAvant(date, DateToTest[i]):
                NbMatchAvantDate+=1
        
        return NbMatchAvantDate

    def getAdversairesAvantDate(self, joueur, date):
        adversairesAvantDate = []
        stats = self.lireStats(joueur)
        adversaires = stats.iloc[:, 0].tolist()
        DateToTest = self.getDate(joueur)
        for i in range(len(adversaires)):
            if self.Date.estAvant(date, DateToTest[i]):
                adversairesAvantDate.append(adversaires[i])
        return adversairesAvantDate

    def getResultatsAvantDate(self, joueur, date):
        ResultatsAvantDate = []
        stats = self.lireStats(joueur)
        Resultats = stats.iloc[:, 2].tolist()
        DateToTest = self.getDate(joueur)
        for i in range(len(Resultats)):
            if self.Date.estAvant(date, DateToTest[i]):
                ResultatsAvantDate.append(Resultats[i])
        return ResultatsAvantDate

    def moyenne_sans_biais_avant_date(self, joueur, valeurs, date):
        minutes = self.getMinAvantDate(joueur, date)
        if(len(minutes)!=0) :
            seuil = constSeuil * statistics.mean(minutes)
            valeurs_filtres = [valeurs[i] for i in range(len(minutes)) if minutes[i] >= seuil]
            return statistics.mean(valeurs_filtres)
        else: 
            return 0
    
    def ecart_type_sans_biais_avant_date(self, joueur, valeurs, date):
        minutes = self.getMinAvantDate(joueur, date)
        if (len(minutes) != 0):
            seuil = constSeuil * statistics.mean(minutes)
            valeurs_filtres = [valeurs[i] for i in range(len(minutes)) if minutes[i] >= seuil]
            if(len(valeurs_filtres)) > 1 :
                return statistics.stdev(valeurs_filtres)
            else: 
                return 0
        else :
            return 0

    def getEcartTypeSansBiaisAvantDate(self, joueur, categorie, date):
        if categorie == 'Points':
            return self.ecart_type_sans_biais_avant_date(joueur, self.getPtsAvantDate(joueur, date), date)
        
        if categorie == 'Rebonds':
            return self.ecart_type_sans_biais_avant_date(joueur, self.getRebAvantDate(joueur, date), date)
        
        if categorie =='Passes':
            return self.ecart_type_sans_biais_avant_date(joueur, self.getPdAvantDate(joueur, date), date)

    def getMoyenneSansBiaisAvantDate(self, joueur, categorie, date):
        if categorie == 'Points':
            return self.moyenne_sans_biais_avant_date(joueur, self.getPtsAvantDate(joueur, date), date)
        
        if categorie == 'Rebonds':
            return self.moyenne_sans_biais_avant_date(joueur, self.getRebAvantDate(joueur, date), date)
        
        if categorie =='Passes':
            return self.moyenne_sans_biais_avant_date(joueur, self.getPdAvantDate(joueur, date), date)
    
    def getPtsJoueurVsEquipeAvantDate(self,joueur,Equipe, date):
        pts = []
        adversaires = self.getAdversairesAvantDate(joueur, date)
        ptsJoueur = self.getPtsAvantDate(joueur, date)
        i=0
        for adversaire in adversaires: 
            if Equipe in adversaire :
                pts.append(ptsJoueur[i])
            i+=1 
        return pts
    
    def getPourcentageMoyenAvantDate(self, joueur, date):
        listePourcentage = []
        pointsEquipe = self.getPointsEquipeAvantDate(joueur, date)
        pointsJoueur = self.getPtsAvantDate(joueur, date)
        for i in range(len(pointsJoueur)):
            listePourcentage.append(pointsJoueur[i]/pointsEquipe[i])
        return statistics.mean(listePourcentage)

    def getPointsEquipeAvantDate(self, joueur, date):
        resultats = self.getResultatsAvantDate(joueur, date)
        adversaires = self.getAdversairesAvantDate(joueur, date)
        points = []
        i = 0
        for jour in adversaires :
            if '@' in jour:
                pts_away = resultats[i].split('-')
                if len(pts_away) > 1 :
                    points.append(int(pts_away[1].strip()))
        
            else:
                pts = resultats[i].split('\n')
                if len(pts) > 1:
                    pts_home = pts[1].split('-')
                    if len(pts_home) > 1:
                        points.append(int(pts_home[0].strip()))
            i+=1 

        return points   

    def getPointsEquipeContreAvantDate(self, joueur, date):
        resultat = self.getResultatsAvantDate(joueur, date)
        adversaire = self.getAdversairesAvantDate(joueur, date)
        points = []
        i = 0
        for jour in adversaire: 
            if '@' in jour:
                pts = resultat[i].split('\n')
                if len(pts) > 1:
                    pts_away = pts[1].split('-')
                    if len(pts_away) > 1 :
                        points.append(int(pts_away[0].strip()))
            else:
                pts_home = resultat[i].split('-')
                if len(pts_home) > 1 :
                    points.append(int(pts_home[1].strip()))
            i+=1
        return points
#P = PathManager()
#file_stat = P.getFichierDossierData('Statistiques_Joueurs.xlsx')
#J = Joueur(file_stat)
#print(J.lireStatsDate('Brandon Ingram', '02-11-2024'))
#print(J.getPaniersReussi('Brandon Ingram'))
#print(J.getPourcentageMoyenTir('Brandon Ingram'))
#print(J.getMoyennePaniersReussi('Brandon Ingram'))
#print(J.getRecord('Brandon Ingram', 9.5))

#print(J.getPourcentageForme('Brandon Ingram'))
#print(J.getMoyennePaniersReussiForme('Brandon Ingram'))
#print(J.getRecordForme('Brandon Ingram', 9.5))
