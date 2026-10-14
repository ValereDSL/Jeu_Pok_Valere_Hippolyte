class Objet :

    def __init__(self, nom, effet):
        self.nom = nom
        self.effet = effet

    def utiliser(self, cible):
        """A redefinir dans les classes filles pour appliquer l'effet de l'objet sur le Pokémon cible.""" #il y avait un bug si je mettais un def utiliser pour tout les ovjets
        raise NotImplementedError("Cet objet n'a pas d'effet défini.")

class Potion(Objet):
    def __init__(self, nom="Potion", soin = 20):
        super().__init__(nom)
        self.soin = soin

    def utiliser(self, cible):
        """Soigne le Pokémon cible de 20 PV."""
        if cible.est_ko:
            raise ValueError(f"{cible.nom} est K.O. et ne peut pas être soigné.")
        avant_soin = cible.pv
        cible.soigner(self.soin)
        if cible.pv + self.soin > cible.pv_max:
            cible.pv = cible.pv_max
        return f"{cible.nom} a été soigné de {cible.pv - self.soin} PV !"


class SuperPotion(Potion):
    """Soigne le Pokémon cible de 50 PV."""
    def __init__(self, nom="Super Potion", soin = 50):
        super().__init__(nom, soin)


class Rappel(Potion):
    """Restaure tous les PV du Pokémon cible."""
    def __init__(self, nom="Rappel"):
        super().__init__(nom, soin=0)

    def utiliser(self, cible):
        if not cible.est_ko:
            raise ValueError(f"{cible.nom} n'est pas K.O. et ne peut pas être rappelé.")
        cible.pv = cible.pv_max
        return f"{cible.nom} a été rappelé et ses PV sont restaurés à {cible.pv_max} !"

class Antidote(Objet):
    """Soigne le Pokémon cible de l'empoisonnement."""
    def __init__(self, nom="Antidote"):
        super().__init__(nom)

    def utiliser(self, cible):
        if cible.est_ko:
            raise ValueError(f"{cible.nom} est K.O.")
        if cible.statut is None:
            raise ValueError(f"{cible.nom} n'a aucun problème de statut.")
        ancien = cible.statut
        cible.statut = None
        return f"{cible.nom} n'est plus affecté par {ancien} !"