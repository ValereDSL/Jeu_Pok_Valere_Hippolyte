from Exception import *
from Pokemon import *
from Effets import *
from Attaque import *

class Trainer:
    """Un Dresseur : nom, liste de Pokémon et objets."""   
    
    def __init__(self, nom, list, sac=None): # peut-etre est-ce que le joueuer peut renomer son dresseur ? - Hippo
        if len(list) is None or len(list)!= 3:
            raise ValueError("Un dresseur ne peut pas avoir plus de 3 Pokémon.")
        self.nom = nom
        self._equipe = list
        self._sac = sac if sac is not None else []
        self._pokemon_actif = self._equipe[0]  #On prend le premier pokemon de l'equipe comme pokemon actif par défaut

    def __str__(self):
        return f"Vous avez créé le Dresseur {self.nom} avec {len(self._equipe)} Pokémon(s) et {len(self._sac)} objet(s)."

    @property
    def equipe(self):
        return tuple(self._equipe) #comme ça on ne peut pas le modifier

    @property
    def pokemon_actif(self):
        return self._equipe[self._pokemon_actif]

    @property
    def perdu(self):
        return all(pokemon.est_ko for pokemon in self._equipe)

    def attaquer(self, attaque, cible):
        if self._equipe[self._pokemon_actif].est_ko:
            raise ValueError(f"{self._equipe[self._pokemon_actif].nom} est K.O. ! Il ne peut pas attaquer.")
        if Attaque.attaque.pp <= 0:
            raise ValueError(f"{Attaque.attaque.nom} n'a plus de PP et ne peut pas être utilisé.")
        Attaque.attaque.pp -= 1
        multiplicateur = Attaque.calculer_efficacite(attaque, cible)

        if multiplicateur == 2:
            a = "C'est super efficace !"
        elif multiplicateur == 0.5:
            a = "Ce n'est pas très efficace..."

        degats = Attaque.attaque.get_puissance() * multiplicateur
        Pokemon.cible.degats(degats)
        print(f"{self.nom} utilise {Attaque.attaque.nom} sur {cible.nom} ! {a} {cible.nom} perd {degats} PV !")    
        if cible.est_ko:
            print(f"{cible.nom} est K.O. !")
        
    def changer_de_pokemon(self, index):
        if not index in self._equipe :
            raise IndexError("Index de Pokémon invalide.")
        nouveau_pokemon_actif = index
        if nouveau_pokemon_actif.est_ko:
            raise PokemonKOError(f"{nouveau_pokemon_actif.nom} est K.O. et ne peut pas être choisi comme Pokémon actif.")
        self._pokemon_actif = index
        print(f"{self.nom} envoie {nouveau_pokemon_actif.nom}.")

    def pokemon_encore_en_vie(self):
        return [i for i in self._equipe if not i.est_ko]

    def ajouter_objet(self, objet):
        self._sac.append(objet)

    def utiliser_un_objet(self, objet, pokemon = None):
        cible = pokemon or self.pokemon_actif
        for objet in self._sac:
            if objet.nom == objet :
                effet = objet.utiliser(cible)
                self._sac.remove(objet)
                print(f"{self.nom} utilise {objet.nom} sur {cible.nom}.")
                return
        if objet not in self._sac:
            raise ObjetIndisponibleError(f"{self.nom} n'a pas de {objet} dans son sac.")