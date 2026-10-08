from ProjetPokemon.Exception import PVInvalideError
class Pokemon:
    """Un Pokémon : nom, types, statistiques, attaques et PV (encapsulés)."""
 
    def __init__(self, nom, types, pv_max, attaque, defense, attaque_spe, defense_spe, vitesse, talent, attaques=None):
        self.nom = nom
        self.types = list(types)        
        self._pv_max = pv_max           
        self._pv = pv_max               
        self.talent = talent

        self.attaque = attaque
        self.defense = defense
        self.attaque_spe = attaque_spe
        self.defense_spe = defense_spe
        self.vitesse = vitesse

    @property
    def pv(self):
        return self._pv

    @pv.setter
    def pv(self, valeur):
        if valeur < 0 or valeur > self._pv_max:
            raise PVInvalideError(f"Les PV doivent être compris entre 0 et {self._pv_max}.")
        if not isinstance(valeur, (int, float)):
            raise TypeError("Les PV doivent être un nombre.")
        self._pv = valeur

    @property
    def pv_max(self):
        return self._pv_max

    @property
    def is_ko(self):
        """Vérifie si le Pokémon est K.O. (PV <= 0)."""
        return self._pv <= 0