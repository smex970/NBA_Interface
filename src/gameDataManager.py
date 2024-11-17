from gameDataScrapper import GameDataScrapper

class GameDataManager: 
    def __init__(self, url):
        self.url = url 
    
    def getDataGame(self):
        DataGame = []
        M = GameDataScrapper(self.url)
        Match = M.getDataTeams()
        DataGame = Match
        DataPlayers = self.getDataPlayers()
        DataGame.append(DataPlayers)
        return DataGame


    def getDataPlayers(self):
        data = []
        P = GameDataScrapper(self.url)
        Points = P.getPointsPlayers()
        for p in Points:
            data.append(p)
        S = GameDataScrapper(self.url)
        Stats = S.getStatsPlayers()
        for e in Stats :
            for s in e :
                data.append(s)


        def flatten_stats(data):
            player_stats = {}
            categories_order = ['Points', 'Rebonds', 'Passes']
            
            i = 0
            while i < len(data):
                item = data[i]
                if isinstance(item, str) and item not in categories_order:
                    player = item
                    if player not in player_stats:
                        player_stats[player] = [player]
                elif item in categories_order:
                    current_category = item
                    if player_stats[player][-1] != current_category:
                        player_stats[player].append(current_category)
                    i += 1
                    while i < len(data) and not isinstance(data[i], str):
                        player_stats[player].append(data[i])
                        player_stats[player].append(data[i + 1])
                        i += 2
                    continue
                i += 1

            # Transformer le dictionnaire en liste plate
            flat_list = []
            for stats in player_stats.values():
                flat_list.extend(stats)

            return flat_list
        
        clean_data = flatten_stats(data)
        return clean_data
    
    
    
#url = 'https://www.winamax.fr/paris-sportifs/match/46601877'
#G = GameDataManager(url)
#print(G.getDataGame())