from pathlib import Path

class PathManager:

    def __init__(self):
        self.repertoire_courant = Path(__file__).parent.resolve()
        self.repertoire_parent = self.repertoire_courant.parent
    
    def getRepCourant(self):
        return self.repertoire_courant
    
    def getRepGrdParent(self):
        return self.repertoire_parent
    
    def getDossierStats(self):
        dossier = self.repertoire_parent /'data' / 'stats'
        return dossier
    
    def getFichierDossierData(self, nom_fichier):
        fichier = self.repertoire_parent/ 'data'/ nom_fichier
        return fichier
    
    def getFichierDossierStats(self, nom_fichier):
        fichier = self.repertoire_parent / 'data' / 'stats' /nom_fichier
        return fichier
    
    def getFichierEquipes(self):
        fichier = self.repertoire_parent /'data' / 'src_stats' / 'Equipes'
        return fichier
    
    def getFichierJoueurs(self):
        fichier = self.repertoire_parent /'data' / 'src_stats' / 'Joueurs'
        return fichier

    def getFichierJoueursErreur(self):
        fichier = self.repertoire_parent /'data' / 'src_stats' / 'Joueurs_erreur'
        return fichier

    def getFichierCotes(self, nom_fichier):
        fichier = self.repertoire_parent /'data' / 'cote' / nom_fichier
        return fichier
    
    def getFichierDossierExtension(self, nom_fichier):
        fichier = self.repertoire_parent / 'extension' / nom_fichier
        return fichier

    def getFichiersCote(self):
        fichiers = self.repertoire_parent / 'data' /'cote'
        return [f.name for f in fichiers.glob('*') if f.is_file()]
