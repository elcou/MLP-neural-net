# RESEAU.py
#
# Represente les differentes couches dans un reseau MLP.
# Cette classe contient 4 methodes effectuant chaque phase de calculde l'apprentissage du reseau.
#
# Date de creation: 21 juin 2017
# Derniere modification: 20 juillet 2017
# Auteurs: Carl Martin, Radu Vacarciuc, Elodie Couturier
# ######################################################################################################################

import couche
import settings


class Reseau:

    # Methode pour initialiser le reseau lors de sa creation
    def __init__(self):
        self.x = list()
        self.couches = list()
        self.couches.append(couche.Couche(settings.nb_entrees * 12, settings.nb_neurones[0], 0))
        for i in range(1, len(settings.nb_neurones)):
            self.couches.append(couche.Couche(settings.nb_neurones[i-1], settings.nb_neurones[i], i))

        # Enregistrement des variables globales dans le reseau pour permettre de les enregistrer dans reseau.txt
        # et ainsi les recuperer lors de la generalisation
        self.nb_entrees = settings.nb_entrees
        self.method = settings.method
        self.eta = settings.eta
        self.fonction = settings.fonction
        self.mainpath = settings.mainpath
        self.nb_neurones = settings.nb_neurones

    # Methode permettant d'initialiser les couches sans ecraser les poids apres avoir fait un premier entrainement
    def init2(self):
        self.x = list()
        self.couches[0].init2(0)
        for i in range(1, len(settings.nb_neurones)):
            self.couches[i].init2(i)

    # Methode effectuant la phase 1 qui consiste a calculer les 'a' et 'i' du reseau
    # ainsi que d'enregistrer les 'a' appartenant a la couche precedente
    def Phase1(self):

        # Le 'a moins 1' de la premiere couche est en fait l'entree x
        self.couches[0].amoins1 = self.x

        # On passe a travers chaque couche et on calcule chaque 'a' et 'i'
        for i in range(0, len(self.couches)):
            couche.calcul_i(self.couches[i])
            couche.calcul_a(self.couches[i])

            # Enregistrement des 'a' de la couche courante comme etant les 'a moins 1' de la couche suivante
            if self.couches[i].niveau < len(settings.nb_neurones)-1:
                self.couches[i+1].amoins1 = list()
                for j in range(0, len(self.couches[i].neurones)):
                    self.couches[i+1].amoins1.append(self.couches[i].neurones[j].a)

    # Methode effectuant la phase 2 qui permet de calculer le delta
    def Phase2(self):

        # On commence avec la couche la plus elevee et on descent de facon decroissante
        # pour calculer chaque delta de chaque couche.
        for i in range(len(self.couches), 0, -1):
            if i == len(self.couches):
                couche.calcul_delta(self.couches[i-1], None)
            else:
                couche.calcul_delta(self.couches[i-1], self.couches[i])

    # Methode effectuant la phase 3 qui calcule les delta omegas de chaque couche
    def Phase3(self):
        couche.calcul_delta_omega(self.couches[0])
        for i in range(1, len(self.couches)):
            couche.calcul_delta_omega(self.couches[i])

    # Methode effectuant la phase 4 qui met a jour les omegas
    def Phase4(self):
        for i in range(0, len(self.couches)):
            couche.update_omegas(self.couches[i])
