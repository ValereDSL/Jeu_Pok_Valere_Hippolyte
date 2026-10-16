import random

# Règle commune à TOUS les effets :
#   appliquer(lanceur, cible, degats) renvoie TOUJOURS une liste de messages (même vide).
#   C'est le combat qui affiche les messages.
# Les probabilités sont en POURCENTAGE (30 = 30 %), comme dans Attaque.py.


class Effet:
    def __init__(self, nom, description, duree):
        self.nom = nom
        self.description = description
        self.duree = duree

    def __str__(self):
        return f"{self.nom} : {self.description} (durée : {self.duree})"

    def appliquer(self, lanceur, cible, degats):
        l = []
        return l


class Soin(Effet):  # Soin, Repos, Synthèse, Lait à Boire
    def __init__(self, pourcentage=0.5):
        super().__init__(
            "Soin",
            f"Restaure {int(pourcentage * 100)} % des PV max",
            0
        )
        self.pourcentage = pourcentage

    def appliquer(self, lanceur, cible, degats):
        soin = lanceur.soigner(lanceur.pv_max * self.pourcentage)
        if soin == 0:
            return [f"Les PV de {lanceur.nom} sont déjà au maximum !"]
        return [f"{lanceur.nom} récupère {soin} PV !"]


class Recul(Effet):  # Rapace, Éclair Fou
    def __init__(self, fraction):
        super().__init__(
            "Recul",
            "Le lanceur subit une partie des dégâts qu'il a infligés",
            0
        )
        self.fraction = fraction

    def appliquer(self, lanceur, cible, degats):
        if degats == 0 or lanceur.est_ko:   # l'attaque a raté : pas de contrecoup
            return []
        perte = max(1, int(degats * self.fraction))
        perte = lanceur.degats(perte)   # degats() renvoie ce qui a vraiment été perdu
        return [f"{lanceur.nom} subit le contrecoup ! (-{perte} PV)"]


class Sacrifice(Effet):  # Explosion de Regigigas et Grolem
    def __init__(self):
        super().__init__("Sacrifice", "Le lanceur est mis K.O.", 0)

    def appliquer(self, lanceur, cible, degats):
        if lanceur.est_ko:
            return []
        lanceur.degats(lanceur.pv)
        return [f"{lanceur.nom} est mis K.O. par sa propre explosion !"]


class Apeurer(Effet):  # Coup d'Boule, Morsure, Écrasement, Cascade, Éboulement
    def __init__(self, pourcentage):
        super().__init__("Peur", f"{pourcentage} % de chances que l'adversaire n'attaque pas ce tour", 0)
        self.pourcentage = pourcentage

    def appliquer(self, lanceur, cible, degats):
        # Ne marche que si la cible n'a pas encore joué ce tour (apeure est remis à False en fin de tour)
        if not cible.est_ko and random.randint(1, 100) <= self.pourcentage:
            cible.apeure = True
        return []   # le message s'affichera quand la cible essaiera d'attaquer


class ModifierNiveau(Effet):  # Danse-Lames, Aqua-Brèche, Psyko, Éco-Sphère, Queue de Fer
    def __init__(self, stat, delta, pourcentage=100, sur_lanceur=False):
        super().__init__("Modif. stat", f"{stat} {delta:+d}", 0)
        self.stat = stat                # "attaque", "defense", "attaque_spe", "defense_spe", "vitesse"
        self.delta = delta              # +2 pour Danse-Lames, -1 pour Aqua-Brèche
        self.pourcentage = pourcentage
        self.sur_lanceur = sur_lanceur  # True : le lanceur se booste lui-même

    def appliquer(self, lanceur, cible, degats):
        pokemon = lanceur if self.sur_lanceur else cible
        if pokemon.est_ko or random.randint(1, 100) > self.pourcentage:
            return []
        return pokemon.modifier_niveau(self.stat, self.delta)


class DeuxTours(Effet):  # Tunnel, Lance-Soleil : on charge au tour 1, on frappe au tour 2
    def __init__(self, message, invulnerable=False):
        super().__init__("Deux tours", "L'attaque se charge pendant un tour", 0)
        self.message = message            # ex : "{nom} s'enfouit dans le sol !"
        self.invulnerable = invulnerable  # True pour Tunnel : on ne peut pas le toucher pendant la charge
        # Toute la logique est dans Lancer_combat.attaquer(), car elle dépend du tour de jeu


class Protection(Effet):  # Abri
    def __init__(self):
        super().__init__("Protection", "Protège de toutes les attaques adverses pendant ce tour", 0)

    def appliquer(self, lanceur, cible, degats):
        lanceur.protege = True       # remis à False à la fin du tour
        return [f"{lanceur.nom} se protège !"]


#=============================== Statuts ==============================#
# Un statut RESTE sur le Pokémon (pokemon.statut) pendant plusieurs tours.

class Statut(Effet):
    abreviation = "???"

    def peut_agir(self, pokemon):
        """Appelé avant que le Pokémon attaque. Renvoie (True ou False, messages)."""
        return True, []

    def fin_de_tour(self, pokemon):
        """Appelé à la fin de chaque tour. Le statut s'en va quand la durée tombe à 0."""
        self.duree -= 1
        if self.duree <= 0:
            pokemon.statut = None
            return [f"{pokemon.nom} n'est plus {self.nom.lower()} !"]
        return []


class Brulure(Statut):
    abreviation = "BRU"

    def __init__(self):
        super().__init__("Brûlé", "Perd 1/16 de ses PV max à chaque tour, Attaque divisée par 2", 5)

    def fin_de_tour(self, pokemon):
        if pokemon.est_ko:
            return []
        perte = pokemon.degats(max(1, pokemon.pv_max // 16))
        messages = [f"{pokemon.nom} souffre de sa brûlure ! (-{perte} PV)"]
        if not pokemon.est_ko:
            messages += super().fin_de_tour(pokemon)   # on garde le décompte de la classe Statut
        return messages


class Paralysie(Statut):
    abreviation = "PAR"

    def __init__(self):
        super().__init__("Paralysé", "25 % de chances de ne pas attaquer, Vitesse divisée par 2", 5)

    def peut_agir(self, pokemon):
        if random.random() < 0.25:
            return False, [f"{pokemon.nom} est paralysé ! Il ne peut pas attaquer !"]
        return True, []


class InfligerStatut(Effet):  # Feu Sacré, Tonnerre, Végé-Attaque, Plaquage, Cage-Éclair...
    def __init__(self, classe_statut, pourcentage):
        super().__init__("Statut", f"{pourcentage} % de chances d'infliger un statut", 0)
        self.classe_statut = classe_statut   # la CLASSE (Brulure ou Paralysie), sans parenthèses
        self.pourcentage = pourcentage

    def appliquer(self, lanceur, cible, degats):
        if cible.est_ko:
            return []
        if cible.statut is not None:
            if self.pourcentage == 100:      # Cage-Éclair : on explique pourquoi ça rate
                return [f"Mais {cible.nom} est déjà {cible.statut.nom.lower()} !"]
            return []
        if random.randint(1, 100) > self.pourcentage:
            return []
        # On crée un statut NEUF : chaque Pokémon a son propre compteur de durée
        return cible.infliger_statut(self.classe_statut())


#_______________________Talents___________________________#

class Talent:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description

    def __str__(self):
        return f"{self.nom} : {self.description}"


class Engrais(Talent):  # Talent de Torterra et Jungko
    def __init__(self):
        super().__init__(
            "Engrais",
            "Augmente la puissance des attaques de type Plante de 50%, quand le pokemon est à moins d'un tiers de ses PV max"
        )

    def appliquer(self, attaquant, attaque, puissance):
        # On RENVOIE la puissance au lieu de faire attaque.set_puissance() :
        # sinon le bonus restait collé à l'attaque pour toujours et se cumulait.
        if attaque.type == "Plante" and attaquant.pv <= attaquant.pv_max / 3:
            return puissance * 1.5
        return puissance


class Intimidation(Talent):  # Talent de Léviator
    def __init__(self):
        super().__init__(
            "Intimidation",
            "Baisse l'Attaque de l'adversaire à l'entrée en combat"
        )

    def appliquer(self, possesseur, adversaire):
        return [f"L'Intimidation de {possesseur.nom} fait effet !"] + adversaire.modifier_niveau("attaque", -1)


class RegardVif(Talent):  # Talent de Roucarnage
    def __init__(self):
        super().__init__(
            "Regard Vif",
            "Empêche la précision de baisser"
        )

    def appliquer(self, possesseur):
        # Aucune attaque du jeu ne baisse la précision pour l'instant :
        # on renvoie juste True pour dire "je protège la précision".
        return True


class Statik(Talent):  # Talent de Wattouat et Raichu
    def __init__(self):
        super().__init__(
            "Statik",
            "30% de chances de paralyser l'adversaire qui touche avec une attaque physique"
        )

    def appliquer(self, possesseur, attaquant, attaque):
        if attaque.categorie == "Physique" and not attaquant.est_ko and random.randint(1, 100) <= 30:
            if attaquant.statut is None:
                return [f"Le Statik de {possesseur.nom} fait effet !"] + attaquant.infliger_statut(Paralysie())
        return []


class EpaisGras(Talent):  # Talent d'Écrémeuh
    def __init__(self):
        super().__init__(
            "Épais Gras",
            "Réduit de moitié les dégâts des attaques de type Feu reçues"
        )

    def appliquer(self, possesseur, attaque, degats):
        if attaque.type == "Feu":
            return degats * 0.5
        return degats


class Attention(Talent):  # Talent de Canarticho
    def __init__(self):
        super().__init__(
            "Attention",
            "Empêche la précision de baisser"
        )

    def appliquer(self, possesseur):
        return True


class Torrent(Talent):  # Talent de Staross, Akwakwak et Tortank
    def __init__(self):
        super().__init__(
            "Torrent",
            "Augmente la puissance des attaques de type Eau de 50% quand les PV sont en dessous d'un tiers"
        )

    def appliquer(self, attaquant, attaque, puissance):
        if attaque.type == "Eau" and attaquant.pv <= attaquant.pv_max / 3:
            return puissance * 1.5
        return puissance


class Agitation(Talent):  # Talent de Triopikeur
    def __init__(self):
        super().__init__(
            "Agitation",
            "Augmente les chances de coup critique"
        )

    def get_bonus_critique(self):
        return 1  # à additionner au taux de critique du moteur


class Robustesse(Talent):  # Talent de Grolem
    def __init__(self):
        super().__init__(
            "Robustesse",
            "Empêche d'être mis K.O. en un seul coup si les PV sont au maximum"
        )

    def sur_degats_recus(self, possesseur, attaque, degats):
        if possesseur.pv == possesseur.pv_max and degats >= possesseur.pv:
            return possesseur.pv - 1  # survit avec 1 PV
        return degats
