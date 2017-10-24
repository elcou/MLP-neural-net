# CONSOLE_UTILISATEUR.py
#
# Module demandant a l'utilisateur d'entrer les parametres qu'il souhaite utiliser pour l'apprentissage du reseau
#
# Date de creation: 21 juin 2017
# Derniere modification: 20 juillet 2017
# Auteurs: Carl Martin, Radu Vacarciuc, Elodie Couturier
# ######################################################################################################################

import settings


def init():

    print('\nChemin vers vos fichiers mfc a evaluer:')
    settings.mainpath = input()

    settings.nb_entrees = 0
    while (settings.nb_entrees != 40) and (settings.nb_entrees != 50) and (settings.nb_entrees != 60):
        print('\nTaille de la base de donnees: \n(Entrez 40, 50 ou 60)')
        settings.nb_entrees = int(input())

    settings.method = 'D'
    while (settings.method != 'A') and (settings.method != 'B') and (settings.method != 'C'):
        print("\nMethode a utiliser: \n(Entrez 'A', 'B' ou 'C')")
        print("(A: Donnees triees par valeurs croissantes d'energie statique")
        print(" B: Donnees triees par valeurs croissantes d'energie dynamique")
        print(" C: Donnees triees par la valeur moyenne de l'energie statique et dynamique)")
        print('(Veuillez respecter la case)')
        settings.method = input()

    print('\nNombre de couches cachees:')
    settings.nb_couches = int(input())

    settings.nb_neurones = list()
    for i in range(0, settings.nb_couches):
        print('\nNombre de neurones dans la couche cachee ' + str(i+1) + ':')
        settings.nb_neurones.append(int(input()))
    settings.nb_neurones.append(settings.nb_sorties)

    settings.eta = 2
    while (settings.eta <= 0) or (settings.eta >= 1):
        print("\nTaux d'apprentissage:\n(Entrez une valeur d'eta entre 0 et 1)")
        settings.eta = float(input())

    settings.fonction = "None"
    while (settings.fonction != "sigmoide") and (settings.fonction != "tangente"):
        print("\nFonction d'activation:\n" + '(Entrez "sigmoide" ou "tangente")')
        print('(Veuillez respecter la case)')
        settings.fonction = input()

    print('\n\n')

init()
