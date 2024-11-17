#from updateStats import UpdateStats
from updatePlayers import UpdatePlayers
from updateTeams import UpdateTeams
from pathManager import PathManager
from updateOdds import UpdateOdds
import os


P = PathManager()

url_proballers = "https://www.proballers.com/fr"

url_winamax = 'https://www.winamax.fr/paris-sportifs/sports/2/15/177'
nb_match = 5

fichier_joueur = P.getFichierJoueurs()
fichier_equipes = P.getFichierEquipes()
fichier_joueur_erreur = P.getFichierJoueursErreur()

fichier_cote = P.getFichierCotes("17-11-2024")


if not os.path.exists(fichier_cote):
    odds = UpdateOdds(url_winamax, fichier_cote, nb_match)
    odds.updateFileOdds()

players_teams = UpdatePlayers(url_proballers, fichier_cote, fichier_joueur, fichier_equipes, fichier_joueur_erreur)
players_teams.updateErrors()
players_teams.updateFiles()

#stats = UpdateStats()
