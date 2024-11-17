from paris import Paris 
from joueur import Joueur
from equipe import Equipe 
from modele import Modele
from pathManager import PathManager

P = PathManager()

minutes_min = 30
fr_min = 0.85
matchs_min = 8


class Combinaison:

    def __init__(self, fichier_stats, fichier_cotes, fichier_equipes, probaMin):
        self.Paris = Paris(fichier_cotes, fichier_equipes, fichier_stats)
        self.fichierStats = fichier_stats
        self.fichierEquipe = fichier_equipes
        self.probaMin = probaMin
        self.Equipe = Equipe(fichier_equipes, fichier_stats)
        self.Joueur = Joueur(fichier_stats)

    def probaCutJoueur(self, joueur, categorie,  cut):
        proba = Modele().probaCutJoueur(cut, self.Joueur.getMoyenneSansBiais(joueur, categorie), self.Joueur.getEcartTypeSansBiais(joueur, categorie))
        return float(proba) 

    def probaCutEquipe(self, Equipe1, Equipe2, cut):
        moyenne = self.Equipe.getMoyenneDeuxEquipes(Equipe1, Equipe2)
        ecart_type = self.Equipe.getEcartTypeDeuxEquipes(Equipe1, Equipe2)        
        proba = Modele().probaCutEquipe(cut, moyenne, ecart_type) 
        return float(proba)

    def isCutJoueurValide(self, joueur, categorie, cut):
        adversaire = self.Paris.getAdversaireJoueur(joueur)
        proba = Modele().probaCutJoueur(cut, self.Joueur.getMoyenneSansBiais(joueur, categorie), self.Joueur.getEcartTypeSansBiais(joueur, categorie))
        if proba == False:
            probaValide = False
        else:
            probaValide = Modele().probaValide(proba, self.probaMin)
        
        Regulier = Modele().isJoueurRegulier(self.Joueur.getMin(joueur), minutes_min, fr_min)
        Titulaire = Modele().isJoueurTitulaire(self.Joueur.getNbMatch(joueur), matchs_min)
        MatchUp = Modele().isMatchUpValide(self.Joueur.getPtsVsEquipe(joueur, adversaire), cut)


        return probaValide and Regulier and Titulaire and MatchUp

    def isCutEquipeValide(self, Equipe1, Equipe2, cut):
        moyenne = self.Equipe.getMoyenneDeuxEquipes(Equipe1, Equipe2)
        ecart_type = self.Equipe.getEcartTypeDeuxEquipes(Equipe1, Equipe2)

        proba = Modele().probaCutEquipe(cut, moyenne, ecart_type)
        return Modele().probaValide(proba, self.probaMin) 

    def checkOddsMatch(self, match):
        events = []
        events_match = []
        events_joueurs = []
        cuts_match = self.Paris.getCutMatch(match)
        Joueurs_match = self.Paris.getJoueursMatch(match)
        Equipes_match = self.Paris.getEquipesMatch(match)
        events.append(Equipes_match)
        for cut in cuts_match:
            if self.isCutEquipeValide(Equipes_match[0], Equipes_match[1], cut):
                events_match.append([match, 'Total Points', cut, self.Paris.getCoteMatch(match, cut), self.probaCutEquipe(Equipes_match[0], Equipes_match[1], cut)])
        events.append(events_match)
        for joueur in Joueurs_match:
            for categorie in self.Paris.getCategorieJoueur(joueur):
                cuts = self.Paris.getCutJoueur(joueur, categorie)
                for cut in cuts: 
                    if self.isCutJoueurValide(joueur, categorie, cut) :
                        events_joueurs.append([match, joueur, categorie, cut, self.Paris.getCoteJoueur(joueur, categorie, cut), self.probaCutJoueur(joueur, categorie, cut)])
        events.append(events_joueurs)
        return events

    def checkOdds(self):
        Odds = []
        matchs = self.Paris.getMatchs()
        for match in matchs:
            Odds.append(self.checkOddsMatch(match))
        return Odds
    
    def ValueBet(self, combi):
        for match in combi:
            for events in match[1:]:
                for event in events :
                    if len(event) > 5:
                        if event[4] > 1/event[5]:
                            event.append(True)
                            event.append(round(float(1/event[5]), 2))
                        else : 
                            event.append(False)
                            event.append(round(float(1/event[5]), 2))
                    else:
                        if event[3] > 1/event[4]:
                            event.append(True)
                            event.append(round(float(1/event[4]), 2))
                        else : 
                            event.append(False)
                            event.append(round(float(1/event[4]), 2))  
        return combi       

#----------------------------------------------Avant Date-------------------------------------------
    def probaCutJoueurAvantDate(self, joueur, categorie, cut, date):
        proba = Modele().probaCutJoueur(cut, self.Joueur.getMoyenneSansBiaisAvantDate(joueur, categorie, date), self.Joueur.getEcartTypeSansBiaisAvantDate(joueur, categorie, date))
        return float(proba) 

    def probaCutEquipeAvantDate(self, Equipe1, Equipe2, cut, date):
        moyenne = self.Equipe.getMoyenneDeuxEquipesAvantDate(Equipe1, Equipe2, date)
        ecart_type = self.Equipe.getEcartTypeDeuxEquipesAvantDate(Equipe1, Equipe2, date)
        proba = Modele().probaCutEquipe(cut, moyenne, ecart_type)
        return float(proba)

    def isCutJoueurValideAvantDate(self, joueur, categorie, cut, date):
        adversaire = self.Paris.getAdversaireJoueur(joueur)
        proba = self.probaCutJoueurAvantDate(joueur, categorie, cut, date)

        probaValide = Modele().probaValide(proba, self.probaMin)
        Regulier = Modele().isJoueurRegulier(self.Joueur.getMinAvantDate(joueur, date), minutes_min, fr_min)
        Titulaire = Modele().isJoueurTitulaire(self.Joueur.getNbMatchAvantDate(joueur, date), matchs_min)
        MatchUp = Modele().isMatchUpValide(self.Joueur.getPtsJoueurVsEquipeAvantDate(joueur, adversaire, date), cut)

        return probaValide and Regulier and Titulaire and MatchUp

    def isCutEquipeValideAvantDate(self, Equipe1, Equipe2, cut, date):
        proba = self.probaCutEquipeAvantDate(Equipe1, Equipe2, cut, date)
        return Modele().probaValide(proba, self.probaMin)

    def checkOddsMatchAvantDate(self, match, date):
        events = []
        events_match = []
        events_joueurs = []
        cuts_match = self.Paris.getCutMatch(match)
        Joueurs_match = self.Paris.getJoueursMatch(match)
        Equipes_match = self.Paris.getEquipesMatch(match)
        events.append(Equipes_match)
        for cut in cuts_match:
            if self.isCutEquipeValideAvantDate(Equipes_match[0], Equipes_match[1], cut, date):
                events_match.append([match, Equipes_match[0], Equipes_match[1], 'Total Points', cut, self.Paris.getCoteMatch(match, cut), self.probaCutEquipeAvantDate(Equipes_match[0], Equipes_match[1], cut, date)])
        events.append(events_match)
        for joueur in Joueurs_match:
            for categorie in self.Paris.getCategorieJoueur(joueur):
                cuts = self.Paris.getCutJoueur(joueur, categorie)
                for cut in cuts: 
                    if self.isCutJoueurValideAvantDate(joueur, categorie, cut, date) :
                        events_joueurs.append([match, joueur, categorie, cut, self.Paris.getCoteJoueur(joueur, categorie, cut), self.probaCutJoueurAvantDate(joueur, categorie, cut, date)])
        events.append(events_joueurs)
        return events

    def checkOddsAvantDate(self, date):
        Odds = []
        matchs = self.Paris.getMatchs()
        for match in matchs:
            Odds.append(self.checkOddsMatchAvantDate(match, date))
        return Odds

    def getEventsDate(self, date):
        return self.ValueBet(self.checkOddsAvantDate(date))

#file_cote = P.getFichierCotes('14-11-2024')
#file_stat = P.getFichierDossierData('Statistiques_Joueurs.xlsx')
#file_equipes = P.getFichierEquipes()

#C = Combinaison(file_stat, file_cote, file_equipes, 0.9)
#print(C.ValueBet(C.checkOdds()))