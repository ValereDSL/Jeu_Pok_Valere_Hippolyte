def fin_partie(joueur, adversaire, resultat, bilan):
    """Affiche le bilan du combat. Renvoie True si le joueur veut rejouer."""
    print("\n" + "=" * 60)
    if resultat == "victoire":
        print("                 ★  VICTOIRE  ★")
    elif resultat == "defaite":
        print("                    DÉFAITE")
    else:
        print("                   ABANDON")
    print("=" * 60)

    ko_infliges = len([p for p in adversaire.equipe if p.est_ko])
    ko_subis = len([p for p in joueur.equipe if p.est_ko])

    print(f"\n  Adversaire            : {adversaire.nom}")
    print(f"  Nombre de tours       : {bilan['tours']}")
    print(f"  Dégâts infligés       : {bilan['degats_infliges']}")
    print(f"  Dégâts reçus          : {bilan['degats_recus']}")
    print(f"  Pokémon adverses K.O. : {ko_infliges} / {len(adversaire.equipe)}")
    print(f"  Tes Pokémon K.O.      : {ko_subis} / {len(joueur.equipe)}")
    print(f"  Objets utilisés       : {bilan['objets']}")

    print("\n  État de ton équipe :")
    for pokemon in joueur.equipe:
        etat = "K.O." if pokemon.est_ko else f"{pokemon.pv}/{pokemon.pv_max} PV"
        print(f"    - {pokemon.nom:<11} {etat}")

    while True:
        reponse = input("\nRejouer ? (o/n) : ").strip().lower()
        if reponse == "o":
            return True
        if reponse == "n":
            return False
        print("Réponds par o ou n.")
