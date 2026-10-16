import random
 
from contenu.Pokedex import POKEMONS_DISPONIBLES, DRESSEURS, creer_pokemon, description_courte
from contenu.Trainer import Trainer
from contenu.Objet import Potion, SuperPotion, Rappel, Antidote
from main.Lancer_combat import lancer_combat, demander_nombre
from main.Fin_partie import fin_partie
 
TAILLE_EQUIPE = 5
NIVEAU_JOUEUR = 50
SOIN_ENTRE_LES_COMBATS = False   # True : l'équipe est entièrement soignée avant chaque dresseur
 
 
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
        afficher_equipe(joueur)
        input("\nAppuie sur Entrée pour défier le premier dresseur...")
 
        resultats = jouer_les_combats(joueur)
        rejouer = fin_partie(joueur, resultats)
 
 
def jouer_les_combats(joueur):
    """Le joueur affronte les dresseurs un par un, jusqu'à la première défaite (ou abandon).
    Renvoie la liste des résultats : [(adversaire, "victoire"/"defaite"/"abandon", bilan), ...]"""
    resultats = []
    for numero in range(len(DRESSEURS)):
        adversaire = creer_dresseur(numero)
 
        print("\n" + "#" * 60)
        print(f"   COMBAT {numero + 1} SUR {len(DRESSEURS)} : {adversaire.nom.upper()}")
        print("#" * 60)
 
        resultat, bilan = lancer_combat(joueur, adversaire)
        resultats.append((adversaire, resultat, bilan))
 
        if resultat != "victoire":
            break                                   # défaite ou abandon : la partie s'arrête
        if numero < len(DRESSEURS) - 1:             # il reste au moins un dresseur
            preparer_combat_suivant(joueur)
 
    return resultats
 
 
def preparer_combat_suivant(joueur):
    """Entre deux combats : on remet le premier Pokémon en forme devant, et on montre l'équipe."""
    if SOIN_ENTRE_LES_COMBATS:
        for pokemon in joueur.equipe:          # même les K.O. sont soignés
            pokemon.pv = pokemon.pv_max
            pokemon.statut = None
            for attaque in pokemon.attaques:
                attaque.restaurer_pp()
        print("\nTon équipe a été entièrement soignée !")
 
    # Le Pokémon au combat doit être debout : on envoie le premier qui n'est pas K.O.
    premier_debout = joueur.pokemon_encore_en_vie()[0]
    index = joueur.equipe.index(premier_debout)
    if index != joueur.index_actif:
        joueur.changer_de_pokemon(index)
    else:
        joueur.pokemon_actif.quitter_terrain()      # on efface les bonus/malus du combat précédent
 
    afficher_equipe(joueur)
    input("\nAppuie sur Entrée pour défier le dresseur suivant...")
 
 
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
            deja_pris = "  ✔ déjà dans l'équipe" if nom in noms_choisis else ""
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
 
 
def creer_sac_dresseur(numero):
    """Plus le dresseur est fort, plus son sac est rempli."""
    if numero == 0:
        return [Potion()]
    if numero == 1:
        return [Potion(), Potion()]
    return [SuperPotion(), SuperPotion()]
 
 
def creer_dresseur(numero):
    """Crée le dresseur n° numero de la liste DRESSEURS, avec des Pokémon neufs."""
    nom, noms_pokemon, niveau = DRESSEURS[numero]
    equipe = [creer_pokemon(nom_pokemon, niveau) for nom_pokemon in noms_pokemon]
    return Trainer(nom, equipe, creer_sac_dresseur(numero), est_ordinateur=True)
 
 
def afficher_equipe(joueur):
    print(f"\n--- L'ÉQUIPE DE {joueur.nom.upper()} ---")
    for i, pokemon in enumerate(joueur.equipe, start=1):
        etat = "K.O." if pokemon.est_ko else f"PV {pokemon.pv}/{pokemon.pv_max}"
        statut = f" [{pokemon.statut.abreviation}]" if pokemon.statut else ""
        talent = pokemon.talent.nom if pokemon.talent else "—"
        print(f"  {i}) {pokemon.nom:<11} N.{pokemon.lvl}  {'/'.join(pokemon.types):<12} {etat}{statut}  |  Talent : {talent}")
    print("  Sac : " + (", ".join(objet.nom for objet in joueur.sac) or "vide"))