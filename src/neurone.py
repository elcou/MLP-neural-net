# NEURONE.py
#
# Definition de la classe Neurone. La classe Neurone contient les valeurs i, a, theta et delta du neurone actif
#
# Date de creation: 21 juin 2017
# Derniere modification: 20 juillet 2017
# Auteurs: Carl Martin, Radu Vacarciuc, Elodie Couturier
# ######################################################################################################################


class Neurone:
    def __init__(self):
        self.theta = 0
        self.i = float()
        self.a = float()
        self.delta = float()
