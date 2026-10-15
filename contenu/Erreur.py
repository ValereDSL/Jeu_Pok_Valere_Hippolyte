class PokemonKOError(Exception):
    """Levée si on tente de faire agir ou attaquer un Pokémon déjà K.O."""
    pass


class ObjetIndisponibleError(Exception):
    """Levée si un Dresseur tente d'utiliser un objet qu'il n'a pas ou plus."""
    pass


class PVInvalideError(Exception):
    """Levée si tentative d'affectation incohérente des PV."""
    pass