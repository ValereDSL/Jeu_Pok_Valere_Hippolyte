"""Classe Pokemon."""
import random
from Erreur import PVInvalideError, PokemonKOError
from Effets import *


class Pokemon:
    """Un Pokémon : nom, niveau, types, statistiques, talent, attaques et PV."""

    def __init__(self, nom, lvl, types, pv, attaque, defense, attaque_spe,
                 defense_spe, vitesse, talent=None, attaques=None):
        self.nom = nom
        self.lvl = lvl
        self.types = list(types)
        self.talent = talent
        self.attaques = list(attaques) if attaques else []
        self.statut = None          # "brulure", "paralysie"... géré par tes effets
        self.iv = random.randint(0, 31)

        # Statistiques réelles calculées à partir des stats de base
        self._pv_max = self._calcul_pv(pv)
        self._pv = self._pv_max     # un Pokémon commence avec tous ses PV
        self.attaque = self._calcul_stat(attaque)
        self.defense = self._calcul_stat(defense)
        self.attaque_spe = self._calcul_stat(attaque_spe)
        self.defense_spe = self._calcul_stat(defense_spe)
        self.vitesse = self._calcul_stat(vitesse)

    # --- Formules officielles (sans les EV) ---
    def _calcul_pv(self, base):
        return ((2 * base + self.iv) * self.lvl) // 100 + self.lvl + 10

    def _calcul_stat(self, base):
        return ((2 * base + self.iv) * self.lvl) // 100 + 5

    # --- PV ---
    @property
    def pv(self):
        return self._pv

    @pv.setter
    def pv(self, valeur):
        if not isinstance(valeur, (int, float)):   # on vérifie le type AVANT de comparer
            raise TypeError("Les PV doivent être un nombre.")
        if valeur < 0 or valeur > self._pv_max:
            raise PVInvalideError(f"Les PV doivent être compris entre 0 et {self._pv_max}.")
        self._pv = valeur

    @property
    def pv_max(self):
        return self._pv_max

    @property
    def est_ko(self):
        return self._pv <= 0

    def en_vie(self):
        if self.est_ko:
            raise PokemonKOError(f"{self.nom} est K.O. et ne peut pas agir.")

    def degats(self, damage_amount):
        """Inflige des dégâts. Renvoie les dégâts réellement subis."""
        self.en_vie()
        if damage_amount < 0:
            raise ValueError("Les dégâts doivent être un nombre positif.")
        reels = min(int(damage_amount), self._pv)  # on ne descend jamais sous 0
        self.pv = self._pv - reels # OUT OF RANGE !!!
        return reels

    def soigner(self, heal_amount):
        """Soigne le Pokémon. Renvoie les PV réellement rendus."""
        self.en_vie()
        if heal_amount < 0:
            raise ValueError("Le soin doit être un nombre positif.")
        avant = self._pv
        self.pv = min(self._pv + int(heal_amount), self._pv_max)
        return self._pv - avant

    # --- Affichage --- #
    def __str__(self):
        types = "/".join(self.types)
        return f"{self.nom} (N.{self.lvl}, {types}) — PV {self._pv}/{self._pv_max}"

# --- test --- #
if __name__ == "__main__":
    torterra = Pokemon("Torterra", 50, ["Plante", "Sol"], 95, 109, 105, 75, 85, 56, None)
    print(torterra)
    print(155 <= torterra.pv_max <= 170)   # doit afficher True (ça dépend de l'IV tiré au hasard)
    print(torterra.pv == torterra.pv_max)  # True : il commence en pleine forme

    print(torterra.degats(50))             # 50
    print(torterra.soigner(999))           # 50 : il ne rend que ce qui manquait
    print(torterra.degats(9999))           # ses PV max : pas de plantage !
    print(torterra.est_ko)                 # True