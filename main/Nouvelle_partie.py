import random

from contenu.Pokedex import POKEMONS_DISPONIBLES, DRESSEURS, creer_pokemon, description_courte
from contenu.Trainer import Trainer
from contenu.Objet import Potion, SuperPotion, Rappel, Antidote
from Lancer_combat import lancer_combat, demander_nombre
from Fin_partie import fin_partie

TAILLE_EQUIPE = 5
NIVEAU_JOUEUR = 50


def nouvelle_partie():
    """Une partie complète. On recommence tant que le joueur veut rejouer."""
    nom = input("\nComment t'appelles-tu, dresseur ? ").strip()
    if nom == "":
        nom = "Joueur"

    rejouer = True
    while rejouer:
        equipe = choisir_ou_tirer_equipe()
        if equipe is None:          # le joueur a choisi "Retour"
            return

        joueur = Trainer(nom, equipe, creer_sac_joueur())
        adversaire = creer_dresseur(0)          # 0 = Le Novice (le premier de la liste DRESSEURS)

        afficher_equipe(joueur)
        input("\nAppuie sur Entrée pour lancer le combat...")

        resultat, bilan = lancer_combat(joueur, adversaire)
        rejouer = fin_partie(joueur, adversaire, resultat, bilan)


def choisir_ou_tirer_equipe():
    while True:
        print("\n--- NOUVELLE PARTIE ---")
        print("1) Choisir mon équipe")
        print("2) Équipe aléatoire")
        print("0) Retour au menu")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            return choisir_equipe()
        elif choix == "2":
            return equipe_aleatoire(POKEMONS_DISPONIBLES)
        elif choix == "0":
            return None
        else:
            print("Choix invalide.")


def choisir_equipe():
    """Le joueur choisit TAILLE_EQUIPE Pokémon parmi les disponibles, un par un."""
    noms_choisis = []
    while len(noms_choisis) < TAILLE_EQUIPE:
        print(f"\n--- CHOIX DU POKÉMON n°{len(noms_choisis) + 1} sur {TAILLE_EQUIPE} ---")
        for i, nom in enumerate(POKEMONS_DISPONIBLES, start=1):
            deja_pris = "  déjà dans l'équipe" if nom in noms_choisis else ""
            print(f"  {i}) {description_courte(nom)}{deja_pris}")

        choix = demander_nombre("Votre choix : ", 1, len(POKEMONS_DISPONIBLES))
        nom = POKEMONS_DISPONIBLES[choix - 1]
        if nom in noms_choisis:
            print(f"{nom} est déjà dans ton équipe !")
        else:
            noms_choisis.append(nom)
            print(f"{nom} rejoint ton équipe !")

    return [creer_pokemon(nom, NIVEAU_JOUEUR) for nom in noms_choisis]


def equipe_aleatoire(pokemons_disponibles):
    noms = random.sample(pokemons_disponibles, TAILLE_EQUIPE)
    return [creer_pokemon(nom, NIVEAU_JOUEUR) for nom in noms]


def creer_sac_joueur():
    return [Potion(), Potion(), SuperPotion(), Rappel(), Antidote()]


def creer_dresseur(numero):
    """Crée le dresseur n° numero de la liste DRESSEURS, avec des Pokémon neufs."""
    nom, noms_pokemon, niveau = DRESSEURS[numero]
    equipe = [creer_pokemon(nom_pokemon, niveau) for nom_pokemon in noms_pokemon]
    return Trainer(nom, equipe, [Potion()], est_ordinateur=True)


def afficher_equipe(joueur):
    print(f"\n--- L'ÉQUIPE DE {joueur.nom.upper()} ---")
    for i, pokemon in enumerate(joueur.equipe, start=1):
        print(f"  {i}) {pokemon}  |  Talent : {pokemon.talent.nom if pokemon.talent else '—'}")
    print("  Sac : " + ", ".join(objet.nom for objet in joueur.sac))
