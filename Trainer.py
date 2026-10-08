class Trainer:
    """Un Dresseur : nom, liste de Pokémon et objets."""
    
    def __init__(self, nom, pokemons=None, objets=None):
        self.nom = nom
        self.pokemons = pokemons if pokemons is not None else []
        self.objets = objets if objets is not None else []

    def __str__(self):
        return f"Vous avez créé le Dresseur {self.nom} avec {len(self.pokemons)} Pokémon(s) et {len(self.objets)} objet(s)."
    