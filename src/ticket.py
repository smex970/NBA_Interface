import itertools
from combinaison import Combinaison
from pathManager import PathManager
from bonus import Bonus

P = PathManager()


nb_match_saison = 20
capital_depart = 50

class Ticket:
    def __init__(self, ProbaEvenementMin, nbEvenementMax, fichier_cotes, fichier_equipes, fichier_stats):
        self.fichier_stats = fichier_stats
        self.nbEvenementMax = nbEvenementMax
        self.Combinaison = Combinaison(fichier_stats, fichier_cotes, fichier_equipes, ProbaEvenementMin)
        #self.events_value = self.getValueEvents()
        self.events = self.getAllEventsWithValue()
        self.flat_events = self.getFlatEvents()
        self.date = str(fichier_cotes).split('/')[-1]
        
        
    def getAllEventsWithValue(self):
        return self.Combinaison.ValueBet(self.Combinaison.checkOdds())
    
    def getValueEvents(self):
        return self.Combinaison.ValueBetOnly(self.Combinaison.checkOdds())
    
    def filter_duplicates(self):
        filtered_events = []
        for match in self.events:
            team_info = match[0]
            match_events = match[1]
            player_events = match[2]

            filtered_match_events = self._filter_best_events(match_events)
            filtered_player_events = self._filter_best_events(player_events)

            filtered_events.append([team_info, filtered_match_events, filtered_player_events])
        
        return filtered_events
    
    def _filter_best_events(self, events):
        best_events = {}
        for event in events:
            if 'Total Points' in event:
                key = (event[0], event[1])  # ('Match', 'Total Points') or ('Player Name', 'Category')
                bookmaker_odds = event[3]
                calculated_odds = event[6]
                is_profitable = event[5]
            else :
                key = (event[1], event[2])  # ('Match', 'Total Points') or ('Player Name', 'Category') 
                bookmaker_odds = event[4]
                calculated_odds = event[7]
                is_profitable = event[6]
            difference = abs(calculated_odds - bookmaker_odds)
            best_events[key] = event + [difference]
            
            """if key not in best_events:
                best_events[key] = event + [difference]
            else:
                current_best_event = best_events[key]
                current_best_difference = current_best_event[-1]
                current_best_is_profitable = current_best_event[5]

                # Prioritize True events, then compare differences
                if (is_profitable and not current_best_is_profitable) or \
                   (is_profitable == current_best_is_profitable and difference < current_best_difference):
                    best_events[key] = event + [difference]"""
        
        return [value[:-1] for value in best_events.values()]
    
    def getFlatEvents(self):
        filtered_events = self.filter_duplicates()
        flat_events = [event for match in filtered_events for event in match[1] + match[2]]
        return flat_events


    def getTriEventsOpti(self, events, matchs):
        sorted_events = sorted(events, key=lambda x: (not x[5], x[0] not in matchs, -x[3]/x[6]) if 'Total Points' in x else (not x[6],  x[0] not in matchs, -x[4]/x[7]))
        return sorted_events
        
    def getTriEvents(self, events):
        sorted_events = sorted(events, key=lambda x: (not x[5], -x[3]/x[6]) if 'Total Points' in x else (not x[6], -x[4]/x[7]))
        return sorted_events


    def ticketProbaNOpti(self, N, nb_ticket):
            
        def getCoteEvent(event):
            if 'Total Points' in event :
                return event[3]
            else : 
                return event[4]
            
        def getProbaEvent(event):
            if 'Total Points' in event:
                return event[4]
            else : 
                return event[5]

        nb_t = 0
        tickets = []
        matchs = []
        events = self.getTriEventsOpti(self.flat_events, matchs)


        while nb_t <= nb_ticket:
            ticket = []
            cote_ticket = 1
            proba_ticket = 1
            matchs = []
            while len(ticket) <= self.nbEvenementMax and proba_ticket > N and len(events) > 0:
                ticket.append(events[0])
                cote_ticket *= getCoteEvent(events[0])
                proba_ticket *= getProbaEvent(events[0])
                i=0
                while (events[0][1:3]) in ticket :
                    i+=1
                matchs.append(events[0][i])
                events.pop(0)
                events = self.getTriEventsOpti(events, matchs)
            ticket.append((cote_ticket, proba_ticket, self.date))
            tickets.append(ticket)
            nb_t +=1 
        return tickets


    def applyBonus(self, tickets):
        B = Bonus(self.fichier_stats)
        for ticket in tickets:
            for t in ticket[:-1]:
                if 'Points' in t : 
                    t.append(B.getBonusPoints(t[1], t[3]))
                if 'Passes' in t :
                    t.append(B.getBonusPasses(t[1], t[3]))
                if 'Rebonds' in t :
                    t.append(B.getBonusRebonds(t[1], t[3]))
        return tickets


file_cote = P.getFichierCotes('17-11-2024')
file_stat = P.getFichierDossierData('Statistiques_Joueurs.xlsx')
file_equipes = P.getFichierEquipes()

T = Ticket(0.93, 10, file_cote, file_equipes, file_stat)
p = 0.7
nbre_ticket = 0
G = T.applyBonus(T.ticketProbaNOpti(p, nbre_ticket))
print(G)