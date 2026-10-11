from math import *

import random


class Effet:
    def __init__(self, nom, dercription, duree):
        self.nom = nom
        self.description = dercription
        self.duree = duree

    def __str__(self):
        return f"{self.nom} : {self.description} (durée : {self.duree})"
"""
    def appliquer(self, cible):
        pass
"""

class Brulure(Effet):
    def __init__(self):
        super().__init__(
            "Brûlure",
            "Inflige des dégâts à chaque tour",
            5
        )

    def appliquer(self, cible):
        # logique de la brûlure
        pass


class Soin(Effet):
    def __init__(self):
        super().__init__(
            "Soin",
            "Restaure 50% des PV max",
            0
        )

    def appliquer(self, cible):
        # logique du soin
        pass

#_______________________Talents___________________________#

class Talent:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description

    def __str__(self):
        return f"{self.nom} : {self.description}"


class Engrais(Talent): # Talent de Torterra
    def __init__(self):
        super().__init__(
            "Engrais",
            "Augmente la puissance des attaques de type Plante de 50%, quand le pokemon est à moins d'un tiers de ses PV max"
        )

    def appliquer(self, attaquant, attaque):
        if attaque.type == "Plante" and attaquant.pv <= attaquant.pv_max / 3:
            attaque.set_puissance(attaque.get_puissance() * 1.5)


class Intimidation(Talent):  # Talent de Léviator
    def __init__(self):
        super().__init__(
            "Intimidation",
            "Baisse l'Attaque de l'adversaire à l'entrée en combat"
        )

    def appliquer(self):
       pass


class RegardVif(Talent):  # Talent de Roucarnage
    def __init__(self):
        super().__init__(
            "Regard Vif",
            "Empêche la précision de baisser"
        )

    def appliquer(self, possesseur):
        pass


class Statik(Talent):  # Talent de Wattouat
    def __init__(self):
        super().__init__(
            "Statik",
            "30% de chances de paralyser l'adversaire qui touche avec une attaque physique"
        )

    def appliquer(self, possesseur, attaquant, attaque):
        if attaque.categorie == "Physique" and random.randint(1, 3) == 1:
            attaquant.infliger_statut("Paralysé")


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
        pass

class Torrent(Talent):  # Talent de Staross, Akwakwak et Tortank
    def __init__(self):
        super().__init__(
            "Torrent",
            "Augmente la puissance des attaques de type Eau de 50% quand les PV sont en dessous d'un tiers"
        )

    def appliquer(self, attaquant, attaque):
        if attaque.type == "Eau" and attaquant.pv <= attaquant.pv_max / 3:
            attaque.set_puissance(attaque.get_puissance() * 1.5)


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