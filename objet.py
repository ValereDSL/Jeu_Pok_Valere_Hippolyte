class Objet :

    def __init__(self, nom, effet):
        self.nom = nom
        self.effet = effet

    def utiliser(self, cible):
        """Applique l'effet de l'objet sur la cible."""
        self.effet(cible)

class Potion(Objet):
    def __init__(self, nom="Potion", soin = 20):
        super().__init__(nom)
        self.soin = soin

    def soigner(self, cible):
        """Soigne le Pokémon cible de 20 PV."""
        if cible.est_ko:
            raise ValueError(f"{cible.nom} est K.O. et ne peut pas être soigné.")
        avant_soin = cible.pv
        cible.soigner(self.soin)
        if cible.pv + self.soin > cible.pv_max:
            cible.pv = cible.pv_max
        return f"{cible.nom} a été soigné de {cible.pv - self.soin} PV !"