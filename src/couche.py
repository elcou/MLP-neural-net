# COUCHE.py
#
# Definition de la classe couche. La classe couche contient tous les omegas, les delta omegas, les objets neurones,
# les 'a' de la couche precedente et le niveau de la couche active.
#
# La classe couche a deux initialisations differentes. __init__ est utilise pour la premiere initialisation et init2
# est utilise pour les initialisations subsequentes.
#
# Les methodes de calcul pour 'i', 'a', delta, delta omega et pour la mise a jour des omegas sont aussi definies dans
# couche.py.
#
# Date de creation: 21 juin 2017
# Derniere modification: 20 juillet 2017
# Auteurs: Carl Martin, Radu Vacarciuc, Elodie Couturier
# ######################################################################################################################

from neurone import *
import random
import math
import settings
import numpy


# Classe definissant les differents elements de chaque couche
class Couche:

    # Initialisation des parametres
    def __init__(self, n_in, n_out, niveau):
        i, j = n_in, n_out
        self.omegas = [[random.uniform((-0.01), 0.01) for x in range(j)] for y in range(i)]
        self.delta_omegas = [[0 for x in range(j)] for y in range(i)]
        self.neurones = list()
        self.niveau = niveau
        for i in range(0, n_out):
            self.neurones.append(Neurone())
        self.amoins1 = list()

    # Methode permettant d'ecraser les 'i' et les 'a', mais de conserver les poids
    def init2(self, niveau):
        self.niveau = niveau
        self.neurones = list()
        for i in range(0, settings.nb_neurones[niveau]):
            self.neurones.append(Neurone())
        self.amoins1 = list()


# Methode calculant les valeurs de 'i' pour une couche
def calcul_i(couche):

    for j in range(0, settings.nb_neurones[couche.niveau]):
        for i in range(0, len(couche.amoins1)):
            couche.neurones[j].i = couche.neurones[j].i + couche.omegas[i][j] * couche.amoins1[i]
        couche.neurones[j].i = couche.neurones[j].i + couche.neurones[j].theta


# Methode calculant les valeurs de 'a' avec differentes fonctions d'activation pour une couche
def calcul_a(couche):

    if settings.fonction == "sigmoide":
        for neurone in couche.neurones:
            # Si 'i' est trop grand, lui attribuer la valeur maximale (709)
            # pour eviter un Overflow lors de l'utilisation de exp()
            if neurone.i > settings.valueMax:
                neurone.i = settings.valueMax
            elif neurone.i < -settings.valueMax:
                neurone.i = -settings.valueMax

            neurone.a = 1 / (1 + math.e ** (-neurone.i))

    elif settings.fonction == "tangente":
        for neurone in couche.neurones:
            neurone.a = math.tan(neurone.i)

    elif settings.fonction == "tangente hyperbolique":
        for neurone in couche.neurones:
            neurone.a = math.tanh(neurone.i)


# Methode calculant les signaux d'erreur lors de la retropropagation pour une couche
def calcul_delta(couche, coucheplus1):

    if settings.fonction == "sigmoide":

        # Si la couche evaluee est la couche de sorties
        if couche.niveau == len(settings.nb_neurones) - 1:
            for j in range(0, settings.nb_sorties):
                couche.neurones[j].delta = (settings.sortie_d[j] - couche.neurones[j].a) * couche.neurones[j].a * (1 - couche.neurones[j].a)

        else:   # Pour toutes les autres couches
            for i in range(0, len(couche.neurones)):
                for j in range(0, len(coucheplus1.neurones)):
                    couche.neurones[i].delta = couche.neurones[i].delta + coucheplus1.neurones[j].delta * coucheplus1.omegas[i][j]
                couche.neurones[i].delta = couche.neurones[i].delta * couche.neurones[i].a * (1 - couche.neurones[i].a)

    elif settings.fonction == "tangente":

        # Si la couche evaluee est la couche de sorties
        if couche.niveau == len(settings.nb_neurones) - 1:
            for j in range(0, settings.nb_sorties):
                # Si 'i' est trop grand, lui attribuer la valeur maximale (709)
                # pour eviter un Overflow lors de l'utilisation de exp()
                if couche.neurones[j].i > settings.valueMax:
                    couche.neurones[j].i = settings.valueMax
                elif couche.neurones[j].i < -settings.valueMax:
                    couche.neurones[j].i = -settings.valueMax
                couche.neurones[j].delta = (settings.sortie_d[j] - couche.neurones[j].a) * (1/(numpy.cos(couche.neurones[j].i)**2))

        else:   # Pour toutes les autres couches
            for i in range(0, len(couche.neurones)):
                # Si 'i' est trop grand, lui attribuer la valeur maximale (709)
                # pour eviter un Overflow lors de l'utilisation de exp()
                if couche.neurones[i].i > settings.valueMax:
                    couche.neurones[i].i = settings.valueMax
                elif couche.neurones[i].i < -settings.valueMax:
                    couche.neurones[i].i = -settings.valueMax
                for j in range(0, len(coucheplus1.neurones)):
                    couche.neurones[i].delta = couche.neurones[i].delta + coucheplus1.neurones[j].delta * coucheplus1.omegas[i][j]
                couche.neurones[i].delta = couche.neurones[i].delta * (1/(numpy.cos(couche.neurones[i].i)**2))

    elif settings.fonction == "tangente hyperbolique":

        # Si la couche evaluee est la couche de sorties
        if couche.niveau == len(settings.nb_neurones) - 1:
            for j in range(0, settings.nb_sorties):
                # Si 'i' est trop grand, lui attribuer la valeur maximale (709)
                # pour eviter un Overflow lors de l'utilisation de exp()
                if couche.neurones[j].i > settings.valueMax:
                    couche.neurones[j].i = settings.valueMax
                elif couche.neurones[j].i < -settings.valueMax:
                    couche.neurones[j].i = -settings.valueMax
                couche.neurones[j].delta = (settings.sortie_d[j] - couche.neurones[j].a) * (1/(numpy.cosh(couche.neurones[j].i) ** 2))

        else:   # Pour toutes les autres couches
            for i in range(0, len(couche.neurones)):
                # Si 'i' est trop grand, lui attribuer la valeur maximale (709)
                # pour eviter un Overflow lors de l'utilisation de exp()
                if couche.neurones[i].i > settings.valueMax:
                    couche.neurones[i].i = settings.valueMax
                elif couche.neurones[i].i < -settings.valueMax:
                    couche.neurones[i].i = -settings.valueMax
                for j in range(0, len(coucheplus1.neurones)):
                    couche.neurones[i].delta = couche.neurones[i].delta + coucheplus1.neurones[j].delta * coucheplus1.omegas[i][j]
                couche.neurones[i].delta = couche.neurones[i].delta * (1/(numpy.cosh(couche.neurones[i].i) ** 2))


# Methode calculant les corrections de poids pour une couche
def calcul_delta_omega(couche):

    for i in range(0, len(couche.omegas)):
        for j in range(0, len(couche.omegas[i])):
            couche.delta_omegas[i][j] = settings.eta * couche.amoins1[i] * couche.neurones[j].delta


# Methode effectuant la mise a jour des poids d'une couche
def update_omegas(couche):
    for i in range(0, len(couche.omegas)):
        for j in range(0, len(couche.omegas[i])):
            couche.omegas[i][j] = couche.omegas[i][j] + couche.delta_omegas[i][j]