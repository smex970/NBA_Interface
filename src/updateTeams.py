from pathManager import PathManager

class UpdateTeams:

    def __init__(self, file, joueur, url_equipe):
        self.file = file
        self.joueur = joueur
        self.url_equipe = url_equipe
        self.equipe = self.convertUrl(url_equipe)
        self.update_team_file()

    def convertUrl(self, url):
        team = url.split('/')[-1]
        formatted_team = team.replace('-', ' ')
        formatted_team = formatted_team.title()
        return formatted_team

    def read_file(self):
        teams = {}
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    parts = line.strip().split(';')
                    team_name = parts[0]
                    players = parts[1:]
                    teams[team_name] = players
        except FileNotFoundError:
            pass  # Le fichier n'existe pas encore, ce qui est normal pour une première exécution
        return teams

    def write_file(self, teams):
        with open(self.file, 'w') as f:
            for team, players in teams.items():
                line = f"{team};" + ";".join(players) + "\n"
                f.write(line)

    def update_team_file(self):
        teams = self.read_file()
        
        if self.equipe in teams:
            if self.joueur not in teams[self.equipe]:
                teams[self.equipe].append(self.joueur)
        else:
            teams[self.equipe] = [self.joueur]

        self.write_file(teams)