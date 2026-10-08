def main():
    print("=" * 60)
    print(" BIENVENUE DANS LE MAGNIFIQUE POKEMON DE HIPPO ET VALERE")
    print("=" * 60)

    while True:
        print("\n----- MENU -----")
        print("  1) Nouvelle partie ")
        print("  2) Informations sur le jeu ")
        print("  0) Quitter")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            pass
        elif choix == "2":
            pass
        elif choix == "0":
            print("À bientôt !")
            break
        else:
            print("Choix invalide, réessayez.")


if __name__ == "__main__":
    main()