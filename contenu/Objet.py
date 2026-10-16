class Objet :

    def __init__(self, nom):
        self.nom = nom

    def peut_utiliser(self, cible):
        """Renvoie True si l'objet aurait un effet sur la cible. Vérifié AVANT de consommer l'objet."""
        return True

    def utiliser(self, cible):
        """A redefinir dans les classes filles pour appliquer l'effet de l'objet sur le Pokémon cible.""" #il y avait un bug si je mettais un def utiliser pour tout les ovjets
        raise NotImplementedError("Cet objet n'a pas d'effet défini.")

    def __str__(self):
        return self.nom


class Potion(Objet):
    def __init__(self, nom="Potion", soin = 20):
        super().__init__(nom)
        self.soin = soin

    def peut_utiliser(self, cible):
        return not cible.est_ko and cible.pv < cible.pv_max

    def utiliser(self, cible):
        """Soigne le Pokémon cible de 20 PV."""
        if cible.est_ko:
            raise ValueError(f"{cible.nom} est K.O. et ne peut pas être soigné.")
        pv_rendus = cible.soigner(self.soin)   # soigner() ne dépasse jamais les PV max
        return f"{cible.nom} a été soigné de {pv_rendus} PV !"


class SuperPotion(Potion):
    """Soigne le Pokémon cible de 50 PV."""
    def __init__(self, nom="Super Potion", soin = 50):
        super().__init__(nom, soin)


class Rappel(Potion):
    """Restaure tous les PV du Pokémon cible."""
    def __init__(self, nom="Rappel"):
        super().__init__(nom, soin=0)

    def peut_utiliser(self, cible):
        return cible.est_ko

    def utiliser(self, cible):
        if not cible.est_ko:
            raise ValueError(f"{cible.nom} n'est pas K.O. et ne peut pas être rappelé.")
        cible.pv = cible.pv_max
        cible.statut = None
        return f"{cible.nom} a été rappelé et ses PV sont restaurés à {cible.pv_max} !"


class Antidote(Objet):
    """Soigne le Pokémon cible de son statut (brûlure, paralysie)."""
    def __init__(self, nom="Antidote"):
        super().__init__(nom)

    def peut_utiliser(self, cible):
        return not cible.est_ko and cible.statut is not None

    def utiliser(self, cible):
        if cible.est_ko:
            raise ValueError(f"{cible.nom} est K.O.")
        if cible.statut is None:
            raise ValueError(f"{cible.nom} n'a aucun problème de statut.")
        ancien = cible.statut
        cible.statut = None
        return f"{cible.nom} n'est plus {ancien.nom.lower()} !"
