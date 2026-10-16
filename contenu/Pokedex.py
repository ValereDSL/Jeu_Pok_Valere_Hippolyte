"""Toutes les données du jeu : les 15 Pokémon, ceux que le joueur peut choisir, et les 3 dresseurs.

Pour ajouter un Pokémon : une ligne dans POKEDEX + ses attaques dans Attaque.py (attaques_<nom>).
"""
from contenu.Attaque import Attaque
from contenu.Pokemon import Pokemon
from contenu.Effets import (Engrais, Intimidation, RegardVif, Statik, EpaisGras,
                            Attention, Torrent, Agitation, Robustesse)


# nom : (types, PV, Attaque, Défense, Attaque Spé, Défense Spé, Vitesse, talent)
# Le talent est une CLASSE (sans parenthèses) : chaque Pokémon créé reçoit son propre talent.
POKEDEX = {
    "Ho-Oh":      (["Feu", "Vol"],      106, 130,  90, 110, 154,  90, None),  # Pression : à coder !
    "Torterra":   (["Plante", "Sol"],    95, 109, 105,  75,  85,  56, Engrais),
    "Léviator":   (["Eau", "Vol"],       95, 125,  79,  60, 100,  81, Intimidation),
    "Roucarnage": (["Normal", "Vol"],    83,  80,  75,  70,  70, 101, RegardVif),
    "Wattouat":   (["Electrik"],         55,  40,  40,  65,  45,  35, Statik),
    "Écrémeuh":   (["Normal"],           95,  80, 105,  40,  70, 100, EpaisGras),
    "Regigigas":  (["Normal"],          110, 160, 110,  80, 110, 100, None),
    "Canarticho": (["Normal", "Vol"],    52,  90,  55,  58,  62,  60, Attention),
    "Raichu":     (["Electrik"],         60,  90,  55,  90,  80, 110, Statik),
    "Akwakwak":   (["Eau"],              80,  82,  78,  95,  80,  85, Torrent),
    "Jungko":     (["Plante"],           70,  85,  65, 105,  85, 120, Engrais),
    "Triopikeur": (["Sol"],              35, 100,  50,  50,  70, 120, Agitation),
    "Staross":    (["Eau", "Psy"],       60,  75,  85, 100,  85, 115, Torrent),
    "Tortank":    (["Eau"],              79,  83, 100,  85, 105,  78, Torrent),
    "Grolem":     (["Roche", "Sol"],     80, 120, 130,  55,  65,  45, Robustesse),
}

# Les 9 Pokémon que le joueur peut choisir (ceux qui ne sont pas chez les dresseurs)
POKEMONS_DISPONIBLES = ["Ho-Oh", "Torterra", "Roucarnage", "Écrémeuh", "Raichu",
                        "Jungko", "Staross", "Tortank", "Grolem"]

# Les 3 dresseurs, du plus facile au plus difficile : (nom, [Pokémon], niveau)
DRESSEURS = [
    ("Le Novice",   ["Canarticho", "Wattouat"],  50),
    ("La Stratège", ["Triopikeur", "Akwakwak"],  50),
    ("Le Champion", ["Léviator", "Regigigas"],   50),
]


def creer_pokemon(nom, niveau):
    """Crée un Pokémon NEUF (PV pleins, PP pleins) à partir de son nom."""
    types, pv, att, defense, att_spe, def_spe, vit, classe_talent = POKEDEX[nom]
    talent = classe_talent() if classe_talent is not None else None
    return Pokemon(nom, niveau, types, pv, att, defense, att_spe, def_spe, vit,
                   talent, Attaque.attaques_de(nom))


def description_courte(nom):
    """Une ligne pour le menu de choix : 'Torterra    Plante/Sol   PV 95  Att 109 ...'."""
    types, pv, att, defense, att_spe, def_spe, vit, classe_talent = POKEDEX[nom]
    talent = classe_talent().nom if classe_talent is not None else "—"
    return (f"{nom:<11} {'/'.join(types):<12} PV {pv:<4} Att {att:<4} Déf {defense:<4} "
            f"AttSp {att_spe:<4} DéfSp {def_spe:<4} Vit {vit:<4} Talent : {talent}")


# --- test : python -m contenu.Pokedex --- #
if __name__ == "__main__":
    for nom in POKEDEX:
        pokemon = creer_pokemon(nom, 50)
        print(pokemon, "|", ", ".join(a.nom for a in pokemon.attaques))
