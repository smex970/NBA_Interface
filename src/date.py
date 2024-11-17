import datetime

class Date:
    def __init__(self):
        self.mois = {1: "janv.", 2: "févr.", 3: "mars", 4: "avr.", 5: "mai", 6: "juin",7: "juil.", 8: "août", 9: "sept.", 10: "oct.", 11: "nov.", 12: "déc."}
        self.mois_inv = {v: f"{k:02}" for k, v in self.mois.items()}

    def convertir_date_fichier_cote(self, date):
        # Split the date string into day, month, and year using '-' as the separator
        jour, mois, annee = date.split('-')
        # Reformat the date to use '/' as the separator
        return f"{jour}/{mois}/{annee}"
    
    def convertir_date_str(self, date_str):
        jour, mois_nom, annee = date_str.split()
        mois_num = self.mois_inv[mois_nom]
        return f"{jour}/{mois_num}/{annee}"

    def estAvant(self, date, date_to_test):
        # Convertir la date en format 18-07-2024 à un objet datetime
        date_format = "%d/%m/%Y"
        date_obj = datetime.datetime.strptime(self.convertir_date_fichier_cote(date), date_format)
        
        # Convertir la date en format 18 juil. 2024 à un objet datetime
        date_to_test_format = "%d/%m/%Y"
        date_to_test_str = self.convertir_date_str(date_to_test)
        date_to_test_obj = datetime.datetime.strptime(date_to_test_str, date_to_test_format)
        
        # Comparer les objets datetime
        return date_to_test_obj < date_obj
    
    def isSameDate(self, date_game, date_excel):
        date_format = "%d/%m/%Y"
        date_obj = datetime.datetime.strptime(self.convertir_date_fichier_cote(date_game), date_format)

        date_to_test_format = "%d/%m/%Y"
        date_to_test_str = self.convertir_date_str(date_excel)
        date_to_test_obj = datetime.datetime.strptime(date_to_test_str, date_to_test_format)

        return date_obj == date_to_test_obj