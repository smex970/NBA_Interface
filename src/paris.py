from equipe import Equipe
from pathManager import PathManager
P = PathManager()

class Paris:
    
    def __init__(self, fichier_cotes, fichier_equipes, fichier_stats):
        self.fichier_cotes = fichier_cotes
        self.fichierEquipes = fichier_equipes
        self.fichierStats = fichier_stats
        self.data = self.lire_events()
    
    def lire_events(self):
        evenements_data = {}
        match_key = None

        with open(self.fichier_cotes, 'r') as file: 
            lines = file.readlines()

            for line in lines:
                #print(line)
                parts = line.strip().split(';')
                if parts[0].startswith('Match'):
                    # Nouvelle entrée pour un nouveau match
                    match_key = parts[0]
                    evenements_data[match_key] = {}
                    evenements_data[match_key]['Teams'] = [parts[1], parts[2]]

                    # Lire les points du match
                    points_match_info = parts[4:]
                    points_match = []
                    for i in range(0, len(points_match_info), 2):
                        points_match.append([float(points_match_info[i]), float(points_match_info[i+1])])
                    evenements_data[match_key]['Points Match'] = points_match
                else:
                    # Lire les événements des joueurs
                    nom = parts[0]
                    if nom not in evenements_data[match_key]:
                        evenements_data[match_key][nom] = {}

                    i = 1
                    while i < len(parts):
                        categorie = parts[i]
                        if categorie.isalpha():
                            if categorie not in evenements_data[match_key][nom]:
                                evenements_data[match_key][nom][categorie] = []
                            i += 1
                            while i < len(parts) and not parts[i].isalpha():
                                try:
                                    valeur = float(parts[i])
                                    cote = float(parts[i+1])
                                    evenements_data[match_key][nom][categorie].append([valeur, cote])
                                    i += 2
                                except ValueError:
                                    break
                        else:
                            i += 1

        return evenements_data

    def getMatchs(self):
        data = self.lire_events()
        return list(data.keys())

    def getEquipesMatch(self, match):
        data = self.lire_events()
        if match in data:
            return data[match].get('Teams', None)
        return None

    def getEquipesMatchJoueur(self, joueur):
        data = self.lire_events()
        equipes = []
        for match_key, match_data in data.items():
            if joueur in match_data:
                equipes.append(data[match_key]['Teams'])
        return equipes

    def getCutMatch(self, match):
        data = self.lire_events()
        if match in data:
            points_match = data[match].get('Points Match', [])
            cuts = [cut[0] for cut in points_match]
            return cuts
        return None

    def getCoteMatch(self, match, cut):
        data = self.lire_events()
        if match in data:
            points_match = data[match].get('Points Match', [])
            for value, cote in points_match:
                if value == cut:
                    return cote
        return None

    def getJoueursMatch(self, match):
        joueurs = []
        data = self.lire_events()
        if match in data:
            match_data = data[match]
            for key in match_data.keys():
                if key not in ['Teams', 'Points Match']:
                    joueurs.append(key)
        return joueurs
        
    def getCategorieJoueur(self, joueur):
        categories = []
        with open(self.fichier_cotes, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(';')
                i = 1
                if parts[0] == joueur:
                    while i < len(parts):
                        categorie = parts[i]
                        if categorie.isalpha() and categorie not in categories:
                            categories.append(categorie)
                        i+= 1        
        return categories 

    def getCutJoueur(self, joueur, categorie):
        data = self.lire_events()
        for match_key, match_data in data.items():
            if joueur in match_data:
                joueur_data = match_data[joueur]
                if categorie in joueur_data:
                    return [cut[0] for cut in joueur_data[categorie]]
        return None

    def getCotesJoueur(self, joueur, categorie):
        cotes = []
        data = self.lire_events()
        for match_key, match_data in data.items():
            if joueur in match_data:
                joueur_data = match_data[joueur]
                if categorie in joueur_data:
                    for value, cote in joueur_data[categorie]:
                        cotes.append(cote)
                    return cotes
        return None


    def getCoteJoueur(self, joueur, categorie, cut):
        data = self.lire_events()
        for match_key, match_data in data.items():
            if joueur in match_data:
                joueur_data = match_data[joueur]
                if categorie in joueur_data:
                    for value, cote in joueur_data[categorie]:
                        if value == cut :
                            return cote
        return False

    def getAdversaireJoueur(self, joueur):
        E = Equipe(self.fichierEquipes, self.fichierStats)
        EquipeJoueur = E.getEquipeJoueur(joueur)
        EquipesMatch = self.getEquipesMatchJoueur(joueur)[0]
        for e in EquipesMatch:
            if e != EquipeJoueur:
                return e
        return None

#file_cote = P.getFichierCotes('17-11-2024')
#file_stats = P.getFichierDossierData('Statistiques_Joueurs.xlsx')
#file_teams = P.getFichierEquipes()

#Pr = Paris(file_cote, file_teams, file_stats)
#print(Pr.getCotesJoueur('Luka Doncic', 'Points'))