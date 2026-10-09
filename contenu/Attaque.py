
dict_efficacité = {"Normal" :     {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Feu" :        {"Normal" : 1, "Feu" : 0.5, "Eau" : 0.5, "Plante" : 2, "Electrique" : 1, "Vol" : 1, "Sol" : 1},
                   "Eau" :        {"Normal" : 1, "Feu" : 2, "Eau" : 0.5, "Plante" : 0.5, "Electrique" : 1, "Vol" : 1, "Sol" : 2},
                   "Plante" :     {"Normal" : 1, "Feu" : 0.5, "Eau" : 2, "Plante" : 0.5, "Electrique" : 1, "Vol" : 0.5, "Sol" : 2},
                   "Electrique" : {"Normal" : 1, "Feu" : 1, "Eau" : 2, "Plante" : 0.5, "Electrique" : 0.5, "Vol" : 2, "Sol" : 0},
                   "Vol" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 2, "Electrique" : 0.5, "Vol" : 1, "Sol" : 1},
                   "Sol" :        {"Normal" : 1, "Feu" : 2, "Eau" : 1, "Plante" : 0.5, "Electrique" : 2, "Vol" : 0, "Sol" : 1},
                  }
            

class Attaque:
    def __init__(self, nom, type, puissance, precision, pp, effet):
        self.nom = nom
        self.type = type
        self.__puissance_base = puissance 
        self.precision = precision
        self.pp = pp
        self.pp_max = pp
        self.effet = effet
        self.priorité = 0


    def get_puissance(self):
        return self.__puissance_base 

    def set_puissance(self, valeur):
        self.__puissance_base = valeur
    
    def calculer_efficacite(attaque, defenseur):
        multiplicateur = 1

        for type_defenseur in defenseur.types: # permet de gerer les doubles types , car l'efficacité s'accumule
            multiplicateur *= dict_efficacité[attaque.type][type_defenseur]

        return multiplicateur


class Physique(Attaque):
    def __init__(self, nom, type, puissance, precision, pp, effet):
        super().__init__(nom, type, puissance, precision, pp, effet)
        self.categorie = "physique"


class Speciale(Attaque):
    def __init__(self, nom, type, puissance, precision, pp, effet):
        super().__init__(nom, type, puissance, precision, pp, effet)
        self.categorie = "Spéciale"

class Statut(Attaque):
    def __init__(self, nom, type, puissance, precision, pp, effet):
        super().__init__(nom, type, puissance, precision, pp, effet) # on met la puissance a 0 directement car les attaques de statut ne font pas de degats 
        self.categorie = "Statut"

#exemple sur les attaques de ho-ho :
rapace = Attaque("Rapace", "Vol", 120, 100, 15, "recul")
feu_sacre = Speciale("Feu Sacré", "Feu", 100, 95, 5, "brulure") # <= implique la creation d'un dossier effets pour les attaques qui ont des effets speciaux
seisme = Attaque("Séisme", "Sol", 100, 100, 10, None)
soin = Statut("Soin", "Normal", 0, 100, 5, "soin")