from ProjetPokemon.pokemon import *
from ProjetPokemon.Effets import *
from ProjetPokemon.Attaque import *

class Trainer:
    """Un Dresseur : nom, liste de Pokémon et objets."""
    Taille_equipe = 3    
    
    def __init__(self, nom, list, sac=None): # peut-etre est-ce que le joueuer peut renomer son dresseur ? - Hippo
        if len(list) is None or len(list)!= self.taille_equipe:
            raise ValueError("Un dresseur ne peut pas avoir plus de 3 Pokémon.")
        self.nom = nom
        self._equipe = list
        self.sac = sac if sac is not None else []
        self._pokemon_actif = self._equipe[0]  #On prend le premier pokemon de l'equipe comme pokemon actif par défaut

    def __str__(self):
        return f"Vous avez créé le Dresseur {self.nom} avec {len(self.equipe)} Pokémon(s) et {len(self.sac)} objet(s)."

    @property
    def equipe(self):
        return tuple(self._equipe) #comme ça on ne peut pas le modifier

    @property
    def pokemoon_actif(self):
        return self._pokemon_actif

    @property
    def perdu(self):
        return (pokemon.est_ko for pokemon in self._equipe)

    def attaquer(self, attaque, cible):
        if self._pokemon_actif.est_ko:
            raise ValueError(f"{self._pokemon_actif.nom} est K.O. et ne peut pas attaquer.")
        if attaque.pp <= 0:
            raise ValueError(f"{attaque.nom} n'a plus de PP et ne peut pas être utilisé.")
        attaque.pp -= 1
        multiplicateur = Attaque.calculer_efficacite(attaque, cible)
        degats = attaque.get_puissance() * multiplicateur
        Pokemon.cible.degats(degats)                  