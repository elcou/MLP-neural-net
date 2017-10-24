# SETTINGS.py
#
# settings.py contient toutes les variables utilisees globalement par tous les modules du programmes.
#
# Date de creation: 21 juin 2017
# Derniere modification: 20 juillet 2017
# Auteurs: Carl Martin, Radu Vacarciuc, Elodie Couturier
# ######################################################################################################################


def init():
    global nb_entrees
    global method
    global nb_neurones
    global sortie_d
    global eta
    global fonction
    global valueMax
    global mainpath
    global nb_sorties

    sortie_d = list()       # Valeur de la sortie reelle du fichier entraine
    valueMax = 709          # Valeur maximale pour eviter un Overflow lors de l'utilisation de exp()
    nb_sorties = 10

    nb_entrees = int()       # Nombre de lignes de valeurs gardees dans les fichiers
    method = str()           # Methode utilisee
    nb_neurones = list()     # Nombre de neurones par couche cachee
    eta = float()            # Taux d'apprentissage
    mainpath = str()         # Chemin vers les fichiers mfc
    fonction = str()         # Fonction d'activation

init()



