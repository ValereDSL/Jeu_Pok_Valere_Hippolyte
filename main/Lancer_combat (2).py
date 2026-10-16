"""Un combat tour par tour entre le joueur et un dresseur ordinateur.

Une "action" est un petit tuple :
    ("attaque", attaque)            -> lancer une attaque
    ("objet", objet, pokemon)       -> utiliser un objet du sac sur un Pokémon
    ("changer", index)              -> envoyer un autre Pokémon
    ("quitter",)                    -> abandonner le combat
"""
import random

from contenu.Attaque import Physique
from contenu.Effets import Recul
from contenu.Effets import (DeuxTours, InfligerStatut, Sacrifice, Engrais, Torrent, Intimidation,
                            Statik, EpaisGras, Agitation, Robustesse)


# ======================================================================
#  OUTILS : affichage et saisie
# ======================================================================

def afficher(messages):
    """Affiche une liste de messages renvoyée par un effet."""
    for message in messages:
        print("   » " + message)


def demander_nombre(question, minimum, maximum):
    """Repose la question tant que la réponse n'est pas un nombre entre minimum et maximum."""
    while True:
        reponse = input(question).strip()
        if reponse.isdigit() and minimum <= int(reponse) <= maximum:
            return int(reponse)
        print(f"   Tape un nombre entre {minimum} et {maximum}.")


def barre_pv(pokemon):
    """Une barre de 20 cases : ██████████░░░░░░░░░░"""
    pleines = round(20 * pokemon.pv / pokemon.pv_max)
    if pokemon.pv > 0:
        pleines = max(1, pleines)
    return "█" * pleines + "░" * (20 - pleines)


def ligne_pokemon(pokemon):
    statut = f" [{pokemon.statut.abreviation}]" if pokemon.statut else ""
    ko = " K.O." if pokemon.est_ko else ""
    return f"{pokemon.nom:<11} N.{pokemon.lvl}  {barre_pv(pokemon)} {pokemon.pv:>3}/{pokemon.pv_max:<3}{statut}{ko}"


def boules(dresseur):
    """● pour un Pokémon en forme, ○ pour un Pokémon K.O."""
    return " ".join("○" if p.est_ko else "●" for p in dresseur.equipe)


def afficher_etat(joueur, adversaire, tour):
    print("\n" + "-" * 60)
    print(f"  TOUR {tour}")
    print("-" * 60)
    print(f"  {adversaire.nom}  {boules(adversaire)}")
    print("     " + ligne_pokemon(adversaire.pokemon_actif))
    print()
    print("     " + ligne_pokemon(joueur.pokemon_actif))
    print(f"  {joueur.nom}  {boules(joueur)}")


def creer_lutte():
    """L'attaque de secours quand un Pokémon n'a plus AUCUN PP (comme dans les vrais jeux)."""
    return Physique("Lutte", "Normal", 50, 100, 1, Recul(1 / 4))


def plus_aucun_pp(pokemon):
    return all(not attaque.peut_etre_utilisee() for attaque in pokemon.attaques)


# ======================================================================
#  LE JOUEUR CHOISIT SON ACTION (menu à 4 options)
# ======================================================================

def choisir_action_joueur(joueur):
    pokemon = joueur.pokemon_actif

    # Tunnel / Lance-Soleil : au 2e tour, l'attaque part toute seule
    if pokemon.charge is not None:
        print(f"\n   {pokemon.nom} termine son attaque {pokemon.charge.nom} !")
        return ("attaque", pokemon.charge)

    while True:
        print(f"\n  Que doit faire {pokemon.nom} ?")
        print("    1) Attaquer")
        print("    2) Objets")
        print("    3) Pokémon")
        print("    4) Quitter")
        choix = demander_nombre("  Votre choix : ", 1, 4)

        if choix == 1:
            action = menu_attaques(pokemon)
        elif choix == 2:
            action = menu_objets(joueur)
        elif choix == 3:
            action = menu_changer(joueur)
        else:
            confirmation = input("  Abandonner le combat ? (o/n) : ").strip().lower()
            action = ("quitter",) if confirmation == "o" else None

        if action is not None:      # None veut dire "Retour" : on réaffiche le menu
            return action


def menu_attaques(pokemon):
    if plus_aucun_pp(pokemon):
        print(f"   {pokemon.nom} n'a plus de PP ! Il utilise Lutte.")
        return ("attaque", creer_lutte())
    print()
    for i, attaque in enumerate(pokemon.attaques, start=1):
        print(f"    {i}) {attaque}")
    print("    0) Retour")
    while True:
        choix = demander_nombre("  Quelle attaque ? ", 0, len(pokemon.attaques))
        if choix == 0:
            return None
        attaque = pokemon.attaques[choix - 1]
        if attaque.peut_etre_utilisee():
            return ("attaque", attaque)
        print("   Cette attaque n'a plus de PP !")


def menu_objets(joueur):
    if len(joueur.sac) == 0:
        print("   Votre sac est vide !")
        return None
    print()
    for i, objet in enumerate(joueur.sac, start=1):
        print(f"    {i}) {objet.nom}")
    print("    0) Retour")
    choix = demander_nombre("  Quel objet ? ", 0, len(joueur.sac))
    if choix == 0:
        return None
    objet = joueur.sac[choix - 1]

    print(f"\n  Sur quel Pokémon utiliser {objet.nom} ?")
    for i, pokemon in enumerate(joueur.equipe, start=1):
        print(f"    {i}) {ligne_pokemon(pokemon)}")
    print("    0) Retour")
    choix = demander_nombre("  Votre choix : ", 0, len(joueur.equipe))
    if choix == 0:
        return None
    pokemon = joueur.equipe[choix - 1]
    if not objet.peut_utiliser(pokemon):
        print("   Ça n'aurait aucun effet !")
        return None
    return ("objet", objet, pokemon)


def menu_changer(joueur, oblige=False):
    """Choisir un Pokémon à envoyer. oblige=True quand le Pokémon actif vient d'être mis K.O."""
    print()
    for i, pokemon in enumerate(joueur.equipe, start=1):
        au_combat = "  (au combat)" if i - 1 == joueur.index_actif else ""
        print(f"    {i}) {ligne_pokemon(pokemon)}{au_combat}")
    if not oblige:
        print("    0) Retour")
    while True:
        choix = demander_nombre("  Quel Pokémon envoyer ? ", 1 if oblige else 0, len(joueur.equipe))
        if choix == 0:
            return None
        index = choix - 1
        if joueur.equipe[index].est_ko:
            print("   Ce Pokémon est K.O. !")
        elif index == joueur.index_actif:
            print("   Ce Pokémon est déjà au combat !")
        else:
            return ("changer", index)


# ======================================================================
#  L'ORDINATEUR CHOISIT SON ACTION
# ======================================================================

def choisir_action_ia(dresseur, adversaire):
    pokemon = dresseur.pokemon_actif
    cible = adversaire.pokemon_actif

    if pokemon.charge is not None:
        return ("attaque", pokemon.charge)

    # 1) PV bas : une chance sur deux d'utiliser un objet
    if pokemon.pv < pokemon.pv_max * 0.3 and random.randint(1, 2) == 1:
        for objet in dresseur.sac:
            if objet.peut_utiliser(pokemon):
                return ("objet", objet, pokemon)

    # 2) Sinon on donne une note à chaque attaque et on prend la meilleure
    meilleure_attaque = None
    meilleure_note = -1
    for attaque in pokemon.attaques:
        if not attaque.peut_etre_utilisee():
            continue
        note = noter_attaque(pokemon, cible, attaque) * random.uniform(0.85, 1.15)  # un peu de hasard
        if note > meilleure_note:
            meilleure_note = note
            meilleure_attaque = attaque

    if meilleure_attaque is None:     # plus aucun PP : Lutte
        return ("attaque", creer_lutte())
    return ("attaque", meilleure_attaque)


def noter_attaque(pokemon, cible, attaque):
    """Plus la note est haute, plus l'ordinateur a envie d'utiliser l'attaque."""
    nom_effet = type(attaque.effet).__name__     # "Soin", "InfligerStatut", ...
    if attaque.categorie == "Statut":
        if nom_effet == "Soin":
            return 150 if pokemon.pv < pokemon.pv_max / 2 else 0
        if nom_effet == "InfligerStatut":
            return 0 if cible.statut is not None else 60
        if nom_effet == "ModifierNiveau":
            return 50 if pokemon.pv > pokemon.pv_max * 0.7 else 10
        return 20                                  # Abri
    if nom_effet == "Sacrifice":                   # Explosion : seulement en dernier recours
        return 400 if pokemon.pv < pokemon.pv_max / 4 else 5
    bonus_type = 1.5 if attaque.type in pokemon.types else 1
    return attaque.get_puissance() * attaque.calculer_efficacite(cible) * bonus_type * attaque.precision / 100


# ======================================================================
#  ORDRE DES ACTIONS
# ======================================================================

def priorite_action(dresseur, action):
    """Changer de Pokémon et utiliser un objet passent toujours en premier."""
    if action[0] in ("changer", "objet"):
        return 10
    return action[1].priorite


def ordonner(joueur, action_joueur, adversaire, action_adverse):
    """Renvoie la liste [(dresseur, action), ...] dans l'ordre où elles se jouent."""
    p_joueur = priorite_action(joueur, action_joueur)
    p_adverse = priorite_action(adversaire, action_adverse)
    v_joueur = joueur.pokemon_actif.stat("vitesse")
    v_adverse = adversaire.pokemon_actif.stat("vitesse")

    if p_joueur != p_adverse:
        joueur_en_premier = p_joueur > p_adverse
    elif v_joueur != v_adverse:
        joueur_en_premier = v_joueur > v_adverse
    else:
        joueur_en_premier = random.randint(1, 2) == 1     # égalité : pile ou face

    if joueur_en_premier:
        return [(joueur, action_joueur), (adversaire, action_adverse)]
    return [(adversaire, action_adverse), (joueur, action_joueur)]


# ======================================================================
#  EXÉCUTION DES ACTIONS
# ======================================================================

def executer(dresseur, action, autre, bilan, joueur):
    print()
    if action[0] == "changer":
        envoyer_pokemon(dresseur, action[1], autre)
    elif action[0] == "objet":
        objet, pokemon = action[1], action[2]
        print(f"  {dresseur.nom} utilise {objet.nom} sur {pokemon.nom} !")
        print("   » " + dresseur.utiliser_un_objet(objet, pokemon))
        if dresseur is joueur:
            bilan["objets"] += 1
    else:
        degats = attaquer(dresseur.pokemon_actif, autre.pokemon_actif, action[1])
        if dresseur is joueur:
            bilan["degats_infliges"] += degats
        else:
            bilan["degats_recus"] += degats


def envoyer_pokemon(dresseur, index, autre):
    ancien = dresseur.pokemon_actif
    if not ancien.est_ko:
        print(f"  {dresseur.nom} rappelle {ancien.nom} !")
    dresseur.changer_de_pokemon(index)
    nouveau = dresseur.pokemon_actif
    print(f"  {dresseur.nom} envoie {nouveau.nom} !")
    if isinstance(nouveau.talent, Intimidation) and not autre.pokemon_actif.est_ko:
        afficher(nouveau.talent.appliquer(nouveau, autre.pokemon_actif))


def attaquer(lanceur, cible, attaque):
    """Le lanceur utilise une attaque sur la cible. Renvoie les dégâts infligés."""
    if lanceur.est_ko:                       # mis K.O. avant d'avoir pu jouer
        return 0
    if lanceur.apeure:
        print(f"  {lanceur.nom} a peur ! Il ne peut pas attaquer !")
        lanceur.charge = None
        return 0
    if lanceur.statut is not None:
        peut_agir, messages = lanceur.statut.peut_agir(lanceur)
        afficher(messages)
        if not peut_agir:
            lanceur.charge = None
            return 0

    # --- Attaques en deux tours (Tunnel, Lance-Soleil) ---
    deuxieme_tour = lanceur.charge is attaque
    if not deuxieme_tour:
        attaque.utiliser()                   # on retire 1 PP (une seule fois pour les deux tours)
    print(f"  {lanceur.nom} utilise {attaque.nom} !")
    if isinstance(attaque.effet, DeuxTours) and not deuxieme_tour:
        lanceur.charge = attaque
        print("   » " + attaque.effet.message.format(nom=lanceur.nom))
        return 0
    lanceur.charge = None

    # --- Est-ce que l'attaque touche ? ---
    vise_l_adversaire = attaque.categorie != "Statut" or isinstance(attaque.effet, InfligerStatut)
    if vise_l_adversaire:
        if cible.est_ko:
            print("   » Mais il n'y a pas de cible...")
            return 0
        if cible.protege:
            print(f"   » {cible.nom} se protège !")
            return 0
        if cible.charge is not None and cible.charge.effet.invulnerable:
            print(f"   » {cible.nom} est sous terre ! L'attaque échoue !")
            return 0
        if random.randint(1, 100) > attaque.precision:
            print(f"   » {cible.nom} évite l'attaque !")
            return 0

    # --- Attaque de statut : pas de dégâts, seulement l'effet ---
    if attaque.categorie == "Statut":
        if attaque.effet is not None:
            afficher(attaque.effet.appliquer(lanceur, cible, 0))
        return 0

    # --- Attaque qui fait des dégâts ---
    degats, messages = calculer_degats(lanceur, cible, attaque)
    if degats == 0:
        afficher(messages)
        return 0
    if isinstance(cible.talent, EpaisGras):
        degats = cible.talent.appliquer(cible, attaque, degats)
    if isinstance(cible.talent, Robustesse):
        avant = degats
        degats = cible.talent.sur_degats_recus(cible, attaque, degats)
        if degats < avant:
            messages.append(f"{cible.nom} tient bon grâce à Robustesse !")

    reels = cible.degats(max(1, int(degats)))
    print(f"   » {cible.nom} perd {reels} PV.")
    afficher(messages)

    if isinstance(cible.talent, Statik):
        afficher(cible.talent.appliquer(cible, lanceur, attaque))
    if attaque.effet is not None:
        afficher(attaque.effet.appliquer(lanceur, cible, reels))

    if cible.est_ko:
        print(f"   » {cible.nom} est K.O. !")
    if lanceur.est_ko and not isinstance(attaque.effet, Sacrifice):   # Explosion a déjà son message
        print(f"   » {lanceur.nom} est K.O. !")
    return reels


def calculer_degats(lanceur, cible, attaque):
    """Formule officielle simplifiée. Renvoie (dégâts, messages)."""
    efficacite = attaque.calculer_efficacite(cible)
    if efficacite == 0:
        return 0, [f"Ça n'affecte pas {cible.nom}..."]

    # Physique : Attaque contre Défense / Spéciale : Attaque Spé contre Défense Spé
    if attaque.categorie == "Physique":
        att = lanceur.stat("attaque")
        defense = cible.stat("defense")
        if lanceur.statut is not None and lanceur.statut.nom == "Brûlé":
            att = att / 2
    else:
        att = lanceur.stat("attaque_spe")
        defense = cible.stat("defense_spe")

    puissance = attaque.get_puissance()
    if isinstance(lanceur.talent, (Engrais, Torrent)):
        puissance = lanceur.talent.appliquer(lanceur, attaque, puissance)

    base = ((2 * lanceur.lvl / 5 + 2) * puissance * att / defense) / 50 + 2

    bonus_type = 1.5 if attaque.type in lanceur.types else 1     # même type que le Pokémon
    chance_critique = 1 / 16
    if isinstance(lanceur.talent, Agitation):
        chance_critique = 1 / 8
    critique = random.random() < chance_critique
    hasard = random.uniform(0.85, 1.0)

    degats = base * bonus_type * efficacite * hasard
    messages = []
    if critique:
        degats = degats * 1.5
        messages.append("Coup critique !")
    if efficacite > 1:
        messages.append("C'est super efficace !")
    elif efficacite < 1:
        messages.append("Ce n'est pas très efficace...")
    return degats, messages


# ======================================================================
#  FIN DE TOUR ET REMPLACEMENT DES K.O.
# ======================================================================

def fin_de_tour(joueur, adversaire):
    for dresseur in (joueur, adversaire):
        pokemon = dresseur.pokemon_actif
        pokemon.apeure = False
        pokemon.protege = False
        if pokemon.statut is not None and not pokemon.est_ko:
            afficher(pokemon.statut.fin_de_tour(pokemon))
            if pokemon.est_ko:
                print(f"   » {pokemon.nom} est K.O. !")


def remplacer_les_ko(joueur, adversaire):
    if joueur.pokemon_actif.est_ko:
        print(f"\n  {joueur.pokemon_actif.nom} est K.O. ! Quel Pokémon envoyer ?")
        action = menu_changer(joueur, oblige=True)
        envoyer_pokemon(joueur, action[1], adversaire)
    if adversaire.pokemon_actif.est_ko:
        suivant = adversaire.pokemon_encore_en_vie()[0]
        print()
        envoyer_pokemon(adversaire, adversaire.equipe.index(suivant), joueur)


# ======================================================================
#  LE COMBAT COMPLET
# ======================================================================

def lancer_combat(joueur, adversaire):
    """Joue un combat jusqu'au bout. Renvoie (résultat, bilan).
    résultat vaut "victoire", "defaite" ou "abandon"."""
    bilan = {"tours": 0, "degats_infliges": 0, "degats_recus": 0, "objets": 0}

    print("\n" + "=" * 60)
    print(f"  {adversaire.nom} veut se battre !")
    print("=" * 60)
    print(f"  {adversaire.nom} envoie {adversaire.pokemon_actif.nom} !")
    print(f"  {joueur.nom} envoie {joueur.pokemon_actif.nom} !")
    for dresseur, autre in ((joueur, adversaire), (adversaire, joueur)):
        if isinstance(dresseur.pokemon_actif.talent, Intimidation):
            afficher(dresseur.pokemon_actif.talent.appliquer(dresseur.pokemon_actif, autre.pokemon_actif))

    while True:
        bilan["tours"] += 1
        afficher_etat(joueur, adversaire, bilan["tours"])

        action_adverse = choisir_action_ia(adversaire, joueur)
        action_joueur = choisir_action_joueur(joueur)
        if action_joueur[0] == "quitter":
            print(f"\n  {joueur.nom} prend la fuite...")
            return "abandon", bilan

        for dresseur, action in ordonner(joueur, action_joueur, adversaire, action_adverse):
            autre = adversaire if dresseur is joueur else joueur
            executer(dresseur, action, autre, bilan, joueur)

        fin_de_tour(joueur, adversaire)

        if joueur.perdu:
            print(f"\n  Tous vos Pokémon sont K.O... {adversaire.nom} a gagné.")
            return "defaite", bilan
        if adversaire.perdu:
            print(f"\n  ★ Vous avez battu {adversaire.nom} ! ★")
            return "victoire", bilan

        remplacer_les_ko(joueur, adversaire)
