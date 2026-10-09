from JEU_POK_VALERE_HIPPOLYTE.Exception import PVInvalideError, PokemonKOError
class Pokemon:
    """Un Pokémon : nom, types, statistiques, attaques, vitesse, talent et PV."""
 
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
    def est_ko(self):
        """Vérifie si le Pokémon est K.O."""
        return self._pv <= 0

    def en_vie(self):
        """Vérifie si le Pokémon est en vie."""
        if self.est_ko:
            raise PokemonKOError(f"{self.nom} est K.O. et ne peut pas agir.")

    def degats(self, damage_amount):
        """Inflige des dégâts au Pokémon."""
        self.check_if_alive()
        if damage_amount < 0:
            raise ValueError("Les dégâts doivent être un nombre positif.")
        self.pv = self._pv - damage_amount

    def soigner(self, heal_amount):
        """Soigne le Pokémon."""
        self.check_if_alive()
        if heal_amount < 0:
            raise ValueError("Le soin doit être un nombre positif.")
        self.pv = min(self._pv + heal_amount, self._pv_max)