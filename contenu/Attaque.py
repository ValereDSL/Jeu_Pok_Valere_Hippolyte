
dict_efficacité = {"Normal" :     {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrik" : 1, "Vol" : 1, "Sol" : 1, "psy" : 1, "roche" : 0.5},
                   "Feu" :        {"Normal" : 1, "Feu" : 0.5, "Eau" : 0.5, "Plante" : 2, "Electrik" : 1, "Vol" : 1, "Sol" : 1, "psy" : 1, "roche" : 0.5},
                   "Eau" :        {"Normal" : 1, "Feu" : 2, "Eau" : 0.5, "Plante" : 0.5, "Electrik" : 1, "Vol" : 1, "Sol" : 2, "psy" : 1, "roche" : 2},
                   "Plante" :     {"Normal" : 1, "Feu" : 0.5, "Eau" : 2, "Plante" : 0.5, "Electrik" : 1, "Vol" : 0.5, "Sol" : 2, "psy" : 1, "roche" : 2},
                   "Electrik" : {"Normal" : 1, "Feu" : 1, "Eau" : 2, "Plante" : 0.5, "Electrik" : 0.5, "Vol" : 2, "Sol" : 0, "psy" : 1, "roche" : 1},
                   "Vol" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 2, "Electrik" : 0.5, "Vol" : 1, "Sol" : 1, "psy" : 1, "roche" : 0.5},
                   "Sol" :        {"Normal" : 1, "Feu" : 2, "Eau" : 1, "Plante" : 0.5, "Electrik" : 2, "Vol" : 0, "Sol" : 1, "psy" : 1, "roche" : 2},
                   "psy" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrik" : 1, "Vol" : 1, "Sol" : 1, "psy" : 1, "roche" : 1},
                   "roche" :      {"Normal" : 1, "Feu" : 2, "Eau" : 1, "Plante" : 1, "Electrik" : 1, "Vol" : 2, "Sol" : 0.5, "psy" : 0.5, "roche" : 1},
                  }

TYPES = {"Normal", "Feu", "Eau", "Plante", "Electrik", "Vol", "Sol", "Roche", "Psy"} # sert pour l'exception type inconnu 
            

def multiplicateur(type_attaque, type_defenseur):
    """Renvoie x2, x0.5, x0 ou x1 pour un type d'attaque contre UN type."""
    return dict_efficacité[type_attaque].get(type_defenseur, 1)
 
 
class Attaque:
    categorie = None  # défini dans Physique / Speciale / Statut
 
    def __init__(self, nom, type, puissance, precision, pp, effet=None, priorite=0):
        if type not in TYPES:
            raise ValueError(f"Type inconnu pour {nom} : '{type}'. Types valides : {sorted(TYPES)}")
        self.nom = nom
        self.type = type
        self.__puissance_base = puissance
        self.precision = precision
        self.pp = pp
        self.pp_max = pp
        self.effet = effet
        self.priorite = priorite  # 0 = normal, 1 = Vive-Attaque, etc.
 
    def get_puissance(self):
        return self.__puissance_base
 
    def set_puissance(self, valeur):
        self.__puissance_base = valeur
 
    def calculer_efficacite(self, defenseur):
        """Gère les doubles types : les multiplicateurs se cumulent."""
        resultat = 1
        for type_defenseur in defenseur.types:
            resultat *= multiplicateur(self.type, type_defenseur)
        return resultat
 
    def peut_etre_utilisee(self):
        return self.pp > 0
 
    def utiliser(self):
        """Retire 1 PP. À appeler à chaque fois que l'attaque est lancée."""
        if self.pp <= 0:
            raise ValueError(f"{self.nom} n'a plus de PP !")
        self.pp -= 1
 
    def restaurer_pp(self):
        self.pp = self.pp_max
 
    def __str__(self):
        puissance = self.get_puissance() or "—"
        return (f"{self.nom:<15} {self.type:<9} {self.categorie:<9} "
                f"Puiss. {puissance:<4} Préc. {self.precision}%  PP {self.pp}/{self.pp_max}")
 
 
class Physique(Attaque):
    categorie = "Physique"
 
 
class Speciale(Attaque):
    categorie = "Spéciale"
 
 
class Statut(Attaque):
    categorie = "Statut"
 
    def __init__(self, nom, type, precision, pp, effet=None, priorite=0):
        # Une attaque de statut ne fait pas de dégâts : puissance = 0 par defaut
        super().__init__(nom, type, 0, precision, pp, effet, priorite)

#exemple sur les attaques de ho-ho :
attaque_Ho_oh = {
"rapace" : Attaque("Rapace", "Vol", 120, 100, 15, "recul"),
"feu_sacre" : Speciale("Feu Sacré", "Feu", 100, 95, 5, "brulure"), # <= implique la creation d'un dossier effets pour les attaques qui ont des effets speciaux
"seisme" : Attaque("Séisme", "Sol", 100, 100, 10, None),
"soin" : Statut("Soin", "Normal", 0, 100, 5, "soin") }

#============ test =============#
"""
if __name__ == "__main__":
    class FauxPokemon:          # juste pour tester, sans avoir besoin de Pokemon.py
        def __init__(self, types):
            self.types = types

    seisme = Attaque("Séisme", "Sol", 100, 100, 2, None)
    print(seisme.calculer_efficacite(FauxPokemon(["Roche", "Sol"])))  # doit afficher 2
    print(seisme.calculer_efficacite(FauxPokemon(["Eau", "Vol"])))    # doit afficher 0

    seisme.utiliser()
    seisme.utiliser()
    print(seisme.pp)            # doit afficher 0
    seisme.utiliser()           # doit afficher TON message d'erreur
"""