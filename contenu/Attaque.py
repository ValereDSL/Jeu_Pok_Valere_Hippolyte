import unicodedata
from Attaque import Physique, Speciale, Statut
from Effets import (Recul, Soin, InfligerStatut, Brulure, Paralysie, Apeurer,
                    ModifierNiveau, Sacrifice, DeuxTours, Protection)


dict_efficacité = {"Normal" :     {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrik" : 1, "Vol" : 1, "Sol" : 1, "Psy" : 1, "Roche" : 0.5},
                   "Feu" :        {"Normal" : 1, "Feu" : 0.5, "Eau" : 0.5, "Plante" : 2, "Electrik" : 1, "Vol" : 1, "Sol" : 1, "Psy" : 1, "Roche" : 0.5},
                   "Eau" :        {"Normal" : 1, "Feu" : 2, "Eau" : 0.5, "Plante" : 0.5, "Electrik" : 1, "Vol" : 1, "Sol" : 2, "Psy" : 1, "Roche" : 2},
                   "Plante" :     {"Normal" : 1, "Feu" : 0.5, "Eau" : 2, "Plante" : 0.5, "Electrik" : 1, "Vol" : 0.5, "Sol" : 2, "Psy" : 1, "Roche" : 2},
                   "Electrik" : {"Normal" : 1, "Feu" : 1, "Eau" : 2, "Plante" : 0.5, "Electrik" : 0.5, "Vol" : 2, "Sol" : 0, "Psy" : 1, "Roche" : 1},
                   "Vol" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 2, "Electrik" : 0.5, "Vol" : 1, "Sol" : 1, "Psy" : 1, "Roche" : 0.5},
                   "Sol" :        {"Normal" : 1, "Feu" : 2, "Eau" : 1, "Plante" : 0.5, "Electrik" : 2, "Vol" : 0, "Sol" : 1, "Psy" : 1, "Roche" : 2},
                   "Psy" :        {"Normal" : 1, "Feu" : 1, "Eau" : 1, "Plante" : 1, "Electrik" : 1, "Vol" : 1, "Sol" : 1, "Psy" : 0.5, "Roche" : 1},
                   "Roche" :      {"Normal" : 1, "Feu" : 2, "Eau" : 1, "Plante" : 1, "Electrik" : 1, "Vol" : 2, "Sol" : 0.5, "Psy" : 1, "Roche" : 1},
                  }

TYPES = {"Normal", "Feu", "Eau", "Plante", "Electrik", "Vol",("Sol",),("Psy",),("Roche",)} # sert pour l'exception type inconnu 
            

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

    # ---------------- Les 4 attaques de chaque Pokémon ---------------- #
    @classmethod
    def attaques_ho_oh(cls):
        return [cls.rapace(), cls.feu_sacre(), cls.seisme(), cls.soin()]
 
    @classmethod
    def attaques_pikachu(cls):
        return [cls.tonnerre(), cls.vive_attaque(), cls.cage_eclair(), cls.eclair_fou()]
 
    @classmethod
    def attaques_psychokwak(cls):
        return [cls.hydrocanon(), cls.pistolet_a_o(), cls.coup_d_boule(), cls.aqua_breche()]
 
    @classmethod
    def attaques_canarticho(cls):
        return [cls.picpic(), cls.coupe(), cls.danse_lames(), cls.coup_d_boue()]
 
    @classmethod
    def attaques_regigigas(cls):
        return [cls.ecrasement(), cls.seisme(), cls.explosion(), cls.repos()]
 
    @classmethod
    def attaques_torterra(cls):
        return [cls.vege_attaque(), cls.seisme(), cls.synthese(), cls.morsure()]
 
    @classmethod
    def attaques_leviator(cls):
        return [cls.hydrocanon(), cls.cascade(), cls.seisme(), cls.repos()]
 
    @classmethod
    def attaques_roucarnage(cls):
        return [cls.rapace(), cls.cru_ailes(), cls.vive_attaque(), cls.soin()]
 
    @classmethod
    def attaques_wattouat(cls):
        return [cls.eclair(), cls.fatal_foudre(), cls.cage_eclair(), cls.boul_gomme()]
 
    @classmethod
    def attaques_ecremeuh(cls):
        return [cls.plaquage(), cls.ecrasement(), cls.lait_a_boire(), cls.vive_attaque()]
 
    @classmethod
    def attaques_raichu(cls):
        return [cls.fatal_foudre(), cls.cage_eclair(), cls.vive_attaque(), cls.queue_de_fer()]
 
    @classmethod
    def attaques_akwakwak(cls):
        return [cls.hydrocanon(), cls.surf(), cls.cru_ailes(), cls.soin()]
 
    @classmethod
    def attaques_jungko(cls):
        return [cls.lance_soleil(), cls.eco_sphere(), cls.cru_ailes(), cls.abri()]
 
    @classmethod
    def attaques_triopikeur(cls):
        return [cls.seisme(), cls.tunnel(), cls.coup_d_boule(), cls.vive_attaque()]
 
    @classmethod
    def attaques_staross(cls):
        return [cls.surf(), cls.psyko(), cls.rapide_eclair(), cls.soin()]
 
    @classmethod
    def attaques_tortank(cls):
        return [cls.hydrocanon(), cls.surf(), cls.seisme(), cls.repos()]
 
    @classmethod
    def attaques_grolem(cls):
        return [cls.seisme(), cls.eboulement(), cls.explosion(), cls.repos()]
 
    @staticmethod
    def _cle(nom):
        """'Léviator' -> 'leviator', 'Ho-Oh' -> 'ho_oh'."""
        sans_accents = unicodedata.normalize("NFD", nom)
        propre = "".join(c for c in sans_accents if not unicodedata.combining(c)).lower()
        return propre.replace("-", "_").replace(" ", "_")
 
    @classmethod
    def attaques_de(cls, nom_pokemon):
        """Renvoie les 4 attaques (neuves) d'un Pokémon à partir de son nom."""
        methode = getattr(cls, "attaques_" + cls._cle(nom_pokemon), None)
        if methode is None:
            raise KeyError(f"Aucune fiche d'attaques pour '{nom_pokemon}'.")
        return methode()
 
    # ------------------------------ Vol ------------------------------ #
    @staticmethod
    def rapace():
        return Physique("Rapace", "Vol", 120, 100, 15, Recul(1 / 3))
 
    @staticmethod
    def picpic():
        return Physique("Picpic", "Vol", 35, 100, 35)
 
    @staticmethod
    def cru_ailes():
        return Physique("Cru-Ailes", "Vol", 60, 100, 35)
 
    # ------------------------------ Feu ------------------------------ #
    @staticmethod
    def feu_sacre():
        return Physique("Feu Sacré", "Feu", 100, 95, 5, InfligerStatut(Brulure, 50))
 
    # ------------------------------ Sol ------------------------------ #
    @staticmethod
    def seisme():
        return Physique("Séisme", "Sol", 100, 100, 10)
 
    @staticmethod
    def coup_d_boue():
        return Physique("Coup d'Boue", "Sol", 20, 100, 10)
 
    @staticmethod
    def eboulement():
        return Physique("Éboulement", "Sol", 75, 90, 10, Apeurer(30))
 
    @staticmethod
    def tunnel():
        return Physique("Tunnel", "Sol", 80, 100, 10,
                        DeuxTours("{nom} s'enfouit dans le sol !", invulnerable=True))
 
    # ---------------------------- Électrik ---------------------------- #
    @staticmethod
    def tonnerre():
        return Speciale("Tonnerre", "Electrik", 90, 100, 15, InfligerStatut(Paralysie, 10))
 
    @staticmethod
    def eclair():
        return Speciale("Éclair", "Electrik", 40, 100, 30)
 
    @staticmethod
    def fatal_foudre():
        return Speciale("Fatal-Foudre", "Electrik", 110, 70, 5, InfligerStatut(Paralysie, 30))
 
    @staticmethod
    def rapide_eclair():
        return Speciale("Rapide-Éclair", "Electrik", 55, 100, 30)
 
    @staticmethod
    def eclair_fou():
        return Physique("Éclair Fou", "Electrik", 90, 100, 15, Recul(1 / 3))
 
    @staticmethod
    def cage_eclair():
        return Statut("Cage-Éclair", "Electrik", 90, 20, InfligerStatut(Paralysie, 100))
 
    # ------------------------------ Eau ------------------------------ #
    @staticmethod
    def hydrocanon():
        return Speciale("Hydrocanon", "Eau", 110, 80, 5)
 
    @staticmethod
    def surf():
        return Speciale("Surf", "Eau", 90, 100, 15)
 
    @staticmethod
    def pistolet_a_o():
        return Speciale("Pistolet à O", "Eau", 40, 100, 25)
 
    @staticmethod
    def cascade():
        return Physique("Cascade", "Eau", 80, 100, 15, Apeurer(20))
 
    @staticmethod
    def aqua_breche():
        return Physique("Aqua-brèche", "Eau", 85, 100, 10, ModifierNiveau("defense", -1, 20))
 
    @staticmethod
    def psyko():
        # La fiche indique le type Eau (type officiel : Psy). Pour passer en Psy : "Psy".
        return Speciale("Psyko", "Eau", 90, 100, 10, ModifierNiveau("defense_spe", -1, 10))
 
    # ----------------------------- Plante ----------------------------- #
    @staticmethod
    def vege_attaque():
        return Physique("Végé-Attaque", "Plante", 100, 95, 10, InfligerStatut(Paralysie, 30))
 
    @staticmethod
    def lance_soleil():
        return Speciale("Lance-Soleil", "Plante", 120, 100, 10,
                        DeuxTours("{nom} absorbe la lumière !"))
 
    @staticmethod
    def eco_sphere():
        return Speciale("Éco-Sphère", "Plante", 90, 100, 10, ModifierNiveau("defense_spe", -1, 10))
 
    @staticmethod
    def synthese():
        return Statut("Synthèse", "Plante", 100, 5, Soin(0.5))
 
    # ----------------------------- Normal ----------------------------- #
    @staticmethod
    def vive_attaque():
        return Physique("Vive-Attaque", "Normal", 40, 100, 30, priorite=1)
 
    @staticmethod
    def coupe():
        return Physique("Coupe", "Normal", 50, 95, 30)
 
    @staticmethod
    def boul_gomme():
        return Physique("Boul'Gomme", "Normal", 40, 100, 40)
 
    @staticmethod
    def coup_d_boule():
        return Physique("Coup d'Boule", "Normal", 70, 100, 15, Apeurer(30))
 
    @staticmethod
    def ecrasement():
        return Physique("Écrasement", "Normal", 65, 100, 20, Apeurer(30))
 
    @staticmethod
    def morsure():
        return Physique("Morsure", "Normal", 60, 100, 25, Apeurer(30))
 
    @staticmethod
    def plaquage():
        return Physique("Plaquage", "Normal", 85, 100, 15, InfligerStatut(Paralysie, 30))
 
    @staticmethod
    def queue_de_fer():
        return Physique("Queue de Fer", "Normal", 100, 75, 15, ModifierNiveau("defense", -1, 30))
 
    @staticmethod
    def explosion():
        return Physique("Explosion", "Normal", 250, 100, 5, Sacrifice())
 
    # ------------- Attaques de statut (Normal) : précision "—" = 100 ------------- #
    @staticmethod
    def soin():
        return Statut("Soin", "Normal", 100, 5, Soin(0.5))
 
    @staticmethod
    def repos():
        return Statut("Repos", "Normal", 100, 10, Soin(0.5))
 
    @staticmethod
    def lait_a_boire():
        return Statut("Lait à Boire", "Normal", 100, 5, Soin(0.5))
 
    @staticmethod
    def danse_lames():
        return Statut("Danse-Lames", "Normal", 100, 20,
                      ModifierNiveau("attaque", 2, sur_lanceur=True))
 
    @staticmethod
    def abri():
        return Statut("Abri", "Normal", 100, 10, Protection())
 
class Physique(Attaque):
    categorie = "Physique"
 
 
class Speciale(Attaque):
    categorie = "Spéciale"
 
 
class Statut(Attaque):
    categorie = "Statut"
 
    def __init__(self, nom, type, precision, pp, effet=None, priorite=0):
        # Une attaque de statut ne fait pas de dégâts : puissance = 0 par defaut
        super().__init__(nom, type, 0, precision, pp, effet, priorite)


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