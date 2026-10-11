from random import random


def nouvelle_partie():
    print("\n--- NOUVELLE PARTIE ---")
    print("1) Choisir mon équipe")
    print("2) Équipe aléatoire")

    choix = input("Votre choix : ").strip()

    if choix == "1":
        equipe = choisir_equipe()
    elif choix == "2":
        equipe = equipe_aleatoire()
    else:
        print("Choix invalide.")
        return

    # La suite de la création de partie viendra ici

def equipe_aleatoire(pokemons_disponibles):
    return random.sample(pokemons_disponibles, 5) # il faut donc créer une liste de pokemons_disponibles dans le main.py ou ailleurs pour que ça fonctionne