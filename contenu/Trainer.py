from contenu.Erreur import PokemonKOError, ObjetIndisponibleError


class Trainer:
    """Un Dresseur : nom, liste de Pokémon et objets."""

    def __init__(self, nom, equipe, sac=None, est_ordinateur=False): # peut-etre est-ce que le joueuer peut renomer son dresseur ? - Hippo
        if len(equipe) == 0 or len(equipe) > 6:
            raise ValueError("Un dresseur doit avoir entre 1 et 6 Pokémon.")
        self.nom = nom
        self._equipe = list(equipe)
        self._sac = list(sac) if sac is not None else []
        self._pokemon_actif = 0  #On prend le premier pokemon de l'equipe comme pokemon actif par défaut
        self.est_ordinateur = est_ordinateur   # True : c'est l'IA qui choisit les actions

    def __str__(self):
        return f"Vous avez créé le Dresseur {self.nom} avec {len(self._equipe)} Pokémon(s) et {len(self._sac)} objet(s)."

    @property
    def equipe(self):
        return tuple(self._equipe) #comme ça on ne peut pas le modifier

    @property
    def sac(self):
        return tuple(self._sac)

    @property
    def pokemon_actif(self):
        return self._equipe[self._pokemon_actif]

    @property
    def index_actif(self):
        return self._pokemon_actif

    @property
    def perdu(self):
        return all(pokemon.est_ko for pokemon in self._equipe)

    def changer_de_pokemon(self, index):
        """Met au combat le Pokémon numéro index (0 = le premier de l'équipe)."""
        if index < 0 or index >= len(self._equipe):
            raise IndexError("Index de Pokémon invalide.")
        nouveau_pokemon_actif = self._equipe[index]
        if nouveau_pokemon_actif.est_ko:
            raise PokemonKOError(f"{nouveau_pokemon_actif.nom} est K.O. et ne peut pas être choisi comme Pokémon actif.")
        self.pokemon_actif.quitter_terrain()   # l'ancien perd ses bonus/malus
        self._pokemon_actif = index

    def pokemon_encore_en_vie(self):
        return [i for i in self._equipe if not i.est_ko]

    def ajouter_objet(self, objet):
        self._sac.append(objet)

    def utiliser_un_objet(self, objet, pokemon=None):
        """Utilise un objet du sac sur un Pokémon (le Pokémon actif par défaut). Renvoie le message."""
        cible = pokemon or self.pokemon_actif
        if objet not in self._sac:
            raise ObjetIndisponibleError(f"{self.nom} n'a pas de {objet.nom} dans son sac.")
        message = objet.utiliser(cible)
        self._sac.remove(objet)
        return message
