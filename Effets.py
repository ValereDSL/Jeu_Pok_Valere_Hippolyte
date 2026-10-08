

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