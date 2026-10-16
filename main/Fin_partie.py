
# --- Règles du score : changez ces nombres pour changer le calcul --- #
POINTS_PAR_DRESSEUR_BATTU = 1000
POINTS_PAR_POKEMON_DEBOUT = 200     # Pokémon encore debout à la fin de la partie
POINTS_PAR_PV_RESTANT = 1           # chaque PV restant dans l'équipe rapporte 1 point
MALUS_PAR_OBJET_UTILISE = 50
MALUS_PAR_TOUR = 10                 # récompense les combats rapides
 
 
def calculer_score(joueur, resultats):
    """Renvoie (score total, détail du calcul sous forme de lignes de texte)."""
    victoires = len([r for r in resultats if r[1] == "victoire"])
    debout = len(joueur.pokemon_encore_en_vie())
    pv_restants = sum(pokemon.pv for pokemon in joueur.equipe)
    objets = sum(bilan["objets"] for _, _, bilan in resultats)
    tours = sum(bilan["tours"] for _, _, bilan in resultats)
 
    lignes = [
        (f"{victoires} dresseur(s) battu(s) x {POINTS_PAR_DRESSEUR_BATTU}", victoires * POINTS_PAR_DRESSEUR_BATTU),
        (f"{debout} Pokémon debout x {POINTS_PAR_POKEMON_DEBOUT}", debout * POINTS_PAR_POKEMON_DEBOUT),
        (f"{pv_restants} PV restants x {POINTS_PAR_PV_RESTANT}", pv_restants * POINTS_PAR_PV_RESTANT),
        (f"{objets} objet(s) utilisé(s) x -{MALUS_PAR_OBJET_UTILISE}", -objets * MALUS_PAR_OBJET_UTILISE),
        (f"{tours} tour(s) x -{MALUS_PAR_TOUR}", -tours * MALUS_PAR_TOUR),
    ]
    total = max(0, sum(points for _, points in lignes))
    return total, lignes
 
 
def fin_partie(joueur, resultats):
    """Affiche le bilan de la partie. resultats = [(adversaire, résultat, bilan), ...].
    Renvoie True si le joueur veut rejouer."""
    nb_dresseurs = 3
    victoires = len([r for r in resultats if r[1] == "victoire"])
    dernier_resultat = resultats[-1][1]
 
    print("\n" + "=" * 60)
    if victoires == nb_dresseurs:
        print("         ★ ★ ★  TU AS BATTU LES 3 DRESSEURS !  ★ ★ ★")
    elif dernier_resultat == "abandon":
        print("                   ABANDON")
    else:
        print("                    DÉFAITE")
    print("=" * 60)
 
    # --- Combat par combat ---
    print("\n  Combat par combat :")
    for numero, (adversaire, resultat, bilan) in enumerate(resultats, start=1):
        ko = len([p for p in adversaire.equipe if p.est_ko])
        print(f"    {numero}) {adversaire.nom:<12} {resultat.upper():<9} "
              f"{bilan['tours']:>2} tours | dégâts infligés {bilan['degats_infliges']:>4}, "
              f"reçus {bilan['degats_recus']:>4} | K.O. {ko}/{len(adversaire.equipe)}")
    if len(resultats) < nb_dresseurs:
        print(f"    ... {nb_dresseurs - len(resultats)} dresseur(s) jamais affronté(s)")
 
    # --- État de l'équipe ---
    print("\n  État de ton équipe :")
    for pokemon in joueur.equipe:
        etat = "K.O." if pokemon.est_ko else f"{pokemon.pv}/{pokemon.pv_max} PV"
        print(f"    - {pokemon.nom:<11} {etat}")
 
    # --- Score ---
    total, lignes = calculer_score(joueur, resultats)
    print("\n  Score :")
    for texte, points in lignes:
        print(f"    {texte:<38} {points:>+6}")
    print(f"    {'TOTAL':<38} {total:>6}")
 
    while True:
        reponse = input("\nRejouer ? (o/n) : ").strip().lower()
        if reponse == "o":
            return True
        if reponse == "n":
            return False
        print("Réponds par o ou n.")