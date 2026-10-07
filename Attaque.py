From Maths import *

dict_efficacité = {"Normal" :     {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Feu" :        {"Normal" : 1, "Feu" : 0.5, "Eau" : 0.5, "Plante" : 2, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Eau" :        {"Normal" : 1, "Feu" : 2, "Eau" : 0.5, "Plante" : 0.5, "Electrique" : 1, "Vol" : 1, "Sol" : 2},
                   "Plante" :     {"Normal" : 1, "Feu" : 0.5, "Eau" : 2, "Plante" : 0.5, "Electrique" : 1, "Vol" : 0.5, "Sol" : 2},
                   "Electrique" : {"Normal" : 1, "Feu" : 1, "Eau" : 2, "Plante" : 0.5, "Electrique" : 0.5, "Vol" : 2, "Sol" : 0},
                   "Vol" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 2, "Electrique" : 0.5, "Vol" : 1, "Sol" : 1},
                   "Sol" :        {"Normal" : 1, "Feu" : 2, "Eau" : 1, "Plante" : 0.5, "Electrique" : 2, "Vol" : 0, "Sol" : 1},
                  }
            

class Attaque:
    def __init__(self, nom, type, categorie, puissance, precision, pp, effet):
        self.nom = nom
        self.type = type
        self.categorie = categorie
        self.__puissance_base = puissance 
        self.nvpuissance = -
        self.precision = precision
        self.pp = pp
        self.pp_max = pp
        self.effet = effet
        self.priorité = 0


    def calculer_efficacite(attaque, defenseur):
        multiplicateur = 1

        for type_defenseur in defenseur.types: # permet de gerer les doubles types , car l'efficacité s'accumule
            multiplicateur *= dict_efficacité[attaque.type][type_defenseur]

        return multiplicateur


#exemple sur lmes attaques de ho-ho :
rapace = Attaque("Rapace", "Vol", "Physique", 120, 100, 15, 0, "recul")
feu_sacre = Attaque("Feu Sacré", "Feu", "Physique", 100, 95, 5, 0, "brulure") # <= implique la creation d'un dossier effets pour les attaques qui ont des effets speciaux
seisme = Attaque("Séisme", "Sol", "Physique", 100, 100, 10, 0, None)
soin = Attaque("Soin", "Normal", "Statut", 0, 100, 5, 0, "soin")