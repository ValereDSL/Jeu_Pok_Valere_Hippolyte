from main.Nouvelle_partie import nouvelle_partie


def main():
    print("=" * 60)
    print(" BIENVENUE DANS LE MAGNIFIQUE POKEMON DE HIPPO ET VALERE")
    print("=" * 60)

    while True:
        print("\n----- MENU -----")
        print("  1) Nouvelle partie ")
        print("  2) Informations sur le jeu ") # Ici on pourrais avoir des infos sur les pokemons comme un pokedex ou des infos sur les attaques et les objets
        print("  0) Quitter")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            nouvelle_partie()
        elif choix == "2": # ce menu info pourrait ressemble a un wiki ou le joueur recherche un pokemon ou une attaque et obtient des infos sur celui ci
            # Comme il faut rechercher les pokemons cela force le joueur a d'abord avoir combattu contre des pokemons pour les rechercher (ne spoil pas les pokjemons adverse )
            print("\n----- INFORMATIONS SUR LE JEU -----")
            print("\nCe jeu est un projet de terminal Pokémon développé par Hippolyte et Valère.")
            print("Vous pouvez créer votre équipe de Pokémon, utiliser des objets et combattre d'autres Dresseurs.")
            print("Amusez-vous bien !")
        elif choix == "0":
            print("À bientôt !")
            break
        else:
            print("Choix invalide, réessayez.")


if __name__ == "__main__":
    main()
