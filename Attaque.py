From Maths import *

dict_faiblesses = {"Normal" :     {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Feu" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Eau" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Plante" :     {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Electrique" : {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Vol" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Sol" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                  }
            

class Attaques:
    def __init__(self, nom, type, categorie, puissance, precision, pp, effet):
        self.nom = nom
        self.type = type
        self.categorie = categorie
        self.__puissance_base = puissance
        self.nvpuissance = -
        self.precision = precision
        self.pp = pp
        self.effet = effet