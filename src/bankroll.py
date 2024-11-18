import random

class Bankroll:

    def __init__(self, nbMatchTotal,capital, i_c, i_p):
        self.i_c = i_c
        self.i_p = i_p
        self.nbMatchTotal = nbMatchTotal
        self.capital = capital

    def miseIdeal(self, proba, cote):
        #calcul avec le critere de Kelly
        q = 1 - proba
        b = cote - 1
        f = (b * proba - q)/b
        capital = self.capital
        return (f * capital)

    def nSimulation(self):
        l = []
        for k in range(1000):
            bk = self.capital
            for _ in range(self.nbMatchTotal):
                cote = random.uniform(*self.i_c)
                proba = random.uniform(*self.i_p)
                mise = self.miseIdeal(proba, cote)
                if random.random() < proba:
                    bk += mise * (cote - 1)
                else: 
                    bk -= mise

            l.append(bk)
        
        bkFinal=(sum(l)/len(l))     
        return bkFinal

    def getPourcentageRentabilite(self):
        total = self.nSimulation()    
        return total/self.capital

cote = 1.37
proba = 0.77
inter_c = (cote, cote)
inter_p =(proba, proba)
b = Bankroll(60, 20, inter_c, inter_p)
print(b.miseIdeal(proba, cote))
print(b.nSimulation())


cote = 1.62
proba = 0.68
inter_c = (cote, cote)
inter_p =(proba, proba)
b = Bankroll(60, 20, inter_c, inter_p)
print(b.miseIdeal(proba, cote))
print(b.nSimulation())