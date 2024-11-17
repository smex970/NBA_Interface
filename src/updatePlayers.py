from updateLinks import UpdateLinks
from updateLinks import UpdateErrorsLinks
from updateTeams import UpdateTeams

class UpdatePlayers:
    def __init__(self, url, input_file, output_file, team_file, file_error):
        self.url = url
        self.file_error = file_error
        self.input_file = input_file
        self.output_file = output_file
        self.team_file = team_file

    def read_input_file(self):
        with open(self.input_file, 'r') as f:
            return f.readlines()

    def extract_names(self, lines):
        prenoms_noms = []
        for ligne in lines:
            if 'Match' not in ligne:
                parties = ligne.split(';')
                if len(parties) > 1:  # Vérifier que la ligne a au moins deux éléments
                    prenom_nom = parties[0]
                    prenoms_noms.append(prenom_nom)
        return prenoms_noms

    def read_output_file(self):
        try:
            with open(self.output_file, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            return []  # Si le fichier n'existe pas, initialiser avec une liste vide

    def extract_existing_names(self, lines):
        noms_deja_presents = set()
        for ligne in lines:
            partie = ligne.split(';')
            if partie:
                noms_deja_presents.add(partie[0])
        return noms_deja_presents

    def write_to_output_file(self, nom, link, link_team):

        with open(self.output_file, 'a') as f:
            if link and link_team:
                f.write(nom + ';' + link + '/matchs' + '\n')
                Ut = UpdateTeams(self.team_file, nom, link_team)
            else:
                with open(self.file_error, 'a') as f:
                    f.write(nom + ';' + '\n')

    def updateFiles(self):
        input_lines = self.read_input_file()
        prenoms_noms = self.extract_names(input_lines)

        output_lines = self.read_output_file()
        noms_deja_presents = self.extract_existing_names(output_lines)
        U = UpdateLinks(self.url)
        for nom in prenoms_noms:
            if nom not in noms_deja_presents:
                print(nom)
                links = U.getLink(nom)
                if links is not None and len(links) > 0:
                    link = links[0]
                    link_team = links[1]
                    self.write_to_output_file(nom, link, link_team)
                else:
                    self.write_to_output_file(nom, None, None)

    def updateErrors(self):
        with open(self.file_error, 'r') as f : 
            lines = f.readlines()
            if lines : 
                for line in lines : 
                    parties = line.split(';')
                    with open(self.output_file, 'a') as out:
                        out.write(line)
                    
                    U = UpdateErrorsLinks(parties[1])
                    #print('on est la')
                    team = U.getTeam()
                    UT = UpdateTeams(self.team_file, parties[0], team)
                with open(self.file_error, 'w') as f:
                    f.write('')  # Écrire une chaîne vide pour vider le fichier 
            else : 
                print('Aucune correction nécessaire')


#U = UpdatePlayers(url, file, out_file, file_team)
#U.updateFiles()