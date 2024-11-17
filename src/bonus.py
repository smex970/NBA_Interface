from joueur import Joueur

class Bonus():
    
    def __init__(self, fichier_stats):
        self.Joueur = Joueur(fichier_stats)
    
    def getBonusPoints(self, joueur, cut):
        pourcentage_moyen = self.Joueur.getPourcentageMoyenTir(joueur)
        record = self.Joueur.getRecord(joueur, cut, 'Points')
        moyenne_panier = self.Joueur.getMoyennePaniersReussi(joueur)
        moyenne_pts = self.Joueur.moyenne_sans_biais(joueur, self.Joueur.getPts(joueur))

        pourcentage_moyen_forme = self.Joueur.getPourcentageForme(joueur)
        record_forme = self.Joueur.getRecordForme(joueur, cut, 'Points')
        moyenne_panier_forme = self.Joueur.getMoyennePaniersReussiForme(joueur)
        moyenne_pts_forme = self.Joueur.get_moyenne_sans_biais_forme(joueur,self.Joueur.getPts(joueur))


        return [record, pourcentage_moyen, moyenne_panier_forme,moyenne_pts, '|', record_forme, pourcentage_moyen_forme, moyenne_panier_forme, moyenne_pts_forme]

    def getBonusRebonds(self, joueur, cut):
        record = self.Joueur.getRecord(joueur, cut, 'Rebonds')
        record_forme = self.Joueur.getRecordForme(joueur, cut, 'Rebonds')
        moyenne_rebonds = self.Joueur.moyenne_sans_biais(joueur, self.Joueur.getRebonds(joueur))
        moyenne_rebonds_forme = self.Joueur.get_moyenne_sans_biais_forme(joueur, self.Joueur.getRebonds(joueur))
        
        return [record,  moyenne_rebonds, '|', record_forme, moyenne_rebonds_forme]
    
    def getBonusPasses(self, joueur, cut):
        record = self.Joueur.getRecord(joueur, cut, 'Passes')
        moyenne_passes = self.Joueur.moyenne_sans_biais(joueur, self.Joueur.getPd(joueur))
        
        record_forme = self.Joueur.getRecordForme(joueur, cut, 'Passes')
        moyenne_passes_forme = self.Joueur.get_moyenne_sans_biais_forme(joueur, self.Joueur.getPd(joueur))


        return [record, moyenne_passes, '|', record_forme, moyenne_passes_forme]


