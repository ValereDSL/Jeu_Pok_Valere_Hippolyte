
class Pokemon:
    """Un Pokémon : nom, types, statistiques, attaques et PV (encapsulés)."""
 
    def __init__(self, nom, types, pv_max, attaque, defense, attaque_spe, defense_spe, vitesse, attaques=None):
        self.nom = nom
        self.types = list(types)        
        self._pv_max = pv_max           
        self._pv = pv_max               
 
        self.attaque = attaque
        self.defense = defense
        self.attaque_spe = attaque_spe
        self.defense_spe = defense_spe
        self.vitesse = vitesse