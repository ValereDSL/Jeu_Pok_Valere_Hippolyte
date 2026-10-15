import random


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


class Brulure(Effet):
    def __init__(self):
        super().__init__(
            "Brûlure",
            "Inflige des dégâts à chaque tour",
            5
        )

    def appliquer(self, cible):
        """À appeler à la fin de CHAQUE tour tant que la cible est brûlée."""
        messages = []

        # 1) Les dégâts : 1/16 des PV max, au moins 1
        perte = max(1, cible.pv_max // 16)
        perte = cible.degats(perte)            # degats() renvoie les PV vraiment perdus
        messages.append(f"{cible.nom} souffre de sa brûlure ! (-{perte} PV)")

        # 2) Le compte à rebours : un tour de moins
        self.duree -= 1
        if self.duree <= 0:
            cible.statut = None                # la brûlure disparaît
            messages.append(f"{cible.nom} n'est plus brûlé !")

        return messages


class Soin(Effet):
    def __init__(self):
        super().__init__(
            "Soin",
            "Restaure 50% des PV max",
            0
        )

    def appliquer(self, lanceur, cible, degats):
        soin = lanceur.soigner(lanceur.pv_max * self.pourcentage)
        if soin == 0:
            return [f"Les PV de {lanceur.nom} sont déjà au maximum !"]
        return [f"{lanceur.nom} récupère {soin} PV !"]



class Recul(Effet):
    def __init__(self, fraction):
        super().__init__(
            "Recul",
            "Le lanceur subit une partie des dégâts qu'il a infligés",
            0
        )
        self.fraction = fraction

    def appliquer(self, lanceur, cible, degats):
        if degats == 0:          # l'attaque a raté : pas de contrecoup
            return []
        perte = max(1, int(degats * self.fraction))
        perte = lanceur.degats(perte)   # degats() renvoie ce qui a vraiment été perdu
        return [f"{lanceur.nom} subit le contrecoup ! (-{perte} PV)"]



class Explosion(Effet):  # Explosion de Regigigas
    def __init__(self):
        super().__init__("Explosion", "Le lanceur est mis K.O.", 0)

 
    def appliquer(self, lanceur, cible, degats):
        if lanceur.est_ko:
            return []
        lanceur.degats(lanceur.pv)
        return [f"{lanceur.nom} est mis K.O. par sa propre explosion !"]
 
 

class Peur(Effet):  # Coup d'Boule, Morsure, Écrasement, Cascade
    def __init__(self, probabilite):
        super().__init__("Peur", f"{int(probabilite * 100)} % de chances que l'adversaire n'attaque pas ce tour", 0)
        self.probabilite = probabilite

 
    def appliquer(self, lanceur, cible, degats):
        # Ne marche que si la cible n'a pas encore joué ce tour : c'est le combat qui gérera ça
        if not cible.est_ko and random.random() < self.probabilite:
            cible.apeure = True
        return []   # le message s'affichera quand la cible essaiera d'attaquer
 
 

class ModifStat(Effet):  # Danse-Lames, Aqua-Brèche
    def __init__(self, stat, delta, probabilite=1.0, sur_lanceur=False):
        super().__init__("Modif. stat", f"{stat} {delta:+d}", 0)
        self.stat = stat                # "attaque", "defense", "attaque_spe", "defense_spe", "vitesse"
        self.delta = delta              # +2 pour Danse-Lames, -1 pour Aqua-Brèche
        self.probabilite = probabilite
        self.sur_lanceur = sur_lanceur  # True : le lanceur se booste lui-même

 
    def appliquer(self, lanceur, cible, degats):
        pokemon = lanceur if self.sur_lanceur else cible
        if pokemon.est_ko or random.random() >= self.probabilite:
            return []
        return pokemon.modifier_niveau(self.stat, self.delta)

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