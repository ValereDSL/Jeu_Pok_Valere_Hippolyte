
class PokemonKOError(Exception):
    """Levée si on tente de faire agir ou attaquer un Pokémon déjà K.O."""
    if self._pv <= 0:
        raise PokemonKOError("Le Pokémon est K.O. et ne peut pas agir.")
 
 
class ObjetIndisponibleError(Exception):
    """Levée si un Dresseur tente d'utiliser un objet qu'il n'a pas ou plus."""
    if not self.objet_disponible:
        raise ObjetIndisponibleError("L'objet n'est pas disponible pour le Dresseur.")
 
 
class PVInvalideError(Exception):
    """Levée si tentative d'affectation incohérente des PV."""
    if self._pv < 0 or self._pv > self._pv_max: 
        raise PVInvalideError("Les PV doivent être compris entre 0 et le maximum de PV du Pokémon.")