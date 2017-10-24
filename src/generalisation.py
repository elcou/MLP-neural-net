# GENERALISATION.py
#
# Script principal pour le test d'un reseau de neurones perceptron multi-couches.
# La generalisation se fait a l'aide des fichiers mfc contenus dans le fichier info_test.txt.
# Elle utilise les parametres du reseau contenu dans le fichier texte reseau.txt qui a ete precedemment cree lors
# de l'apprentissage du reseau.
#
# Date de creation: 21 juin 2017
# Derniere modification: 20 juillet 2017
# Auteurs: Carl Martin, Radu Vacarciuc, Elodie Couturier
# ######################################################################################################################

import settings
from reseau import *
from repo_manip import *
import pickle
import os

# Recupere le reseau entraine
with open("reseau.txt", "rb") as reseau_file:
    reseau = pickle.load(reseau_file)

# Recupere les configurations de base utilisees pour l'apprentissage
settings.nb_entrees = reseau.nb_entrees
settings.method = reseau.method
settings.eta = reseau.eta
settings.fonction = reseau.fonction
settings.mainpath = reseau.mainpath
settings.nb_neurones = reseau.nb_neurones

# Permet de lister tous les fichiers mfc contenus dans le repertoire txt_dist
files_manipulation = RepoManip()

# Re-initialise le reseau sans ecraser les poids et theta
reseau.init2()

true = int()
essais = int()

# Ouvrir le fichier text contenant la liste des paths des fichiers a utiliser pour la generalisation
with open(settings.mainpath + 'info_test.txt') as info_test_file:
    for line in info_test_file:
        # Garder juste les noms de fichiers
        l = line.split('txt_dist')
        file_name, file_extension = os.path.splitext(l[1])

        # Trouver tous les fichiers correspondant avec "_method"
        for path in files_manipulation.path:
            # Liste de tous les path des fichiers pour la validation croisee (avec "_method")
            x = list()
            if path.find(str(file_name) + '_method' + settings.method + '_' + str(settings.nb_entrees)) != -1:

                try:
                    # Extraire la valeur de la sortie dans le nom de fichier
                    settings.sortie_d = list()
                    for i in range(0, 10):
                        if i == int(file_name[-2:-1]):
                            settings.sortie_d.append(1)
                        else:
                            settings.sortie_d.append(0)
                    file_name, file_extension = os.path.splitext(path)
                    # Extraire le nombre d'entrees dans le nom de fichier
                    nb_in = int(file_name[-2:])

                # Dans le cas ou nous evaluons un mfc de sortie '0'
                # (dois gerer le fait que c'est ecrit 'o' plutot que '0')
                except ValueError:
                    settings.sortie_d = list()
                    settings.sortie_d.append(1)
                    for i in range(1, 10):
                        settings.sortie_d.append(0)
                    file_name, file_extension = os.path.splitext(path)
                    nb_in = int(file_name[-2:])

                # Ouvrir le fichier et extraire les donnees
                with open(path) as file:
                    for line_data in file:
                        data = line_data.split()
                        for i in range(0, 12):
                            x.append(float(data[i]))

                reseau.x = x
                reseau.Phase1()

                # Recuperer toutes les valeurs des 'a' de la derniere couche
                # La position de la valeur maximale dans cette liste correspondra au resultat obtenu
                sortie_a = list()
                for i in range(0, len(reseau.couches[-1].neurones)):
                    sortie_a.append(reseau.couches[-1].neurones[i].a)
                max = -1000
                index = 0
                for i in range(0, 10):
                    if sortie_a[i] > max:
                        max = sortie_a[i]
                        index = i

                # Verifier sur notre resultat correspond a la veritable sortie
                if settings.sortie_d[index]:
                    true = true + 1
                essais = essais + 1

print('Taux de succes: ' + str(float(true)/float(essais)))

info_test_file.close()
