# APPRENTISSAGE.py
#
# Script principal pour l'apprentissage d'un reseau de neurones perceptron multi-couches.
# L'apprentissage se fait a l'aide des fichiers mfc contenus dans le fichier info_train.txt.
# Une validation croisee est ensuite effectuee a l'aide des fichiers mfc contenus dans le fichier info_vc.txt
# L'apprentissage et la validation sont effectue en boucle, c'est-a-dire qu'on recommencera un nouvel apprentissage
# tant que la validation ne nous confirmera pas un taux de succes superieur a 85% ou apres 15 epoques.
#
# Les parametres du reseau sont enregistres dans un fichier texte afin de pouvoir les recuperer pour ameliorer notre
# apprentissage.
#
# Date de creation: 21 juin 2017
# Derniere modification: 20 juillet 2017
# Auteurs: Carl Martin, Radu Vacarciuc, Elodie Couturier
# ######################################################################################################################

import settings
import console_utilisateur
from reseau import *
from repo_manip import *
import pickle

# Permet de lister tous les fichiers mfc contenus dans le repertoire txt_dist et de creer les nouveaux fichiers avec
# les differentes methodes de tri.
files_manipulation = RepoManip()
files_manipulation.create_new_files()
files_manipulation.repo_tree()
taux_succes = 0
k = 0

# Verifie si un fichier contenant les parametres d'un reseau existe
# (dans le cas ou le reseau a deja ete entraine et nous voudrions l'ameliorer)
if os.path.isfile("reseau.txt"):
    with open("reseau.txt", "rb") as reseau_file:
        reseau = pickle.load(reseau_file)
else:
    # Sinon nous creons un nouveau reseau
    reseau = Reseau()

# Effectue l'apprentissage et la validation croisee jusqu'a l'obtention d'un taux de succes de 85% ou apres 15 epoques
while taux_succes < 0.85 and k < 15:
    k = k + 1

    # --------------------------------------------------- TRAINING -----------------------------------------------------
    with open(settings.mainpath + 'info_train.txt') as info_train_file:

        for line in info_train_file:
            # Garder juste les noms de fichiers
            l = line.split('txt_dist')
            file_name, file_extension = os.path.splitext(l[1])
            x = list()

            # Trouver tous les fichiers correspondant avec "_method"
            for path in files_manipulation.path:
                if path.find(str(file_name) + '_method' + settings.method + '_' + str(settings.nb_entrees)) != -1:
                    try:
                        # Extraire la valeur de la sortie dans le nom de fichier
                        settings.sortie_d = list()
                        for i in range(0, settings.nb_sorties):
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
                        for i in range(1, settings.nb_sorties):
                            settings.sortie_d.append(0)
                        file_name, file_extension = os.path.splitext(path)
                        nb_in = int(file_name[-2:])

                    # Ouvrir le fichier et extraire les donnees
                    with open(path) as file:
                        for line_data in file:
                            data = line_data.split()
                            for i in range(0, 12):
                                x.append(float(data[i]))

                    file.close()

                    # Permet d'initialiser tous les parametres du reseau, mais sans ecraser les valeurs de
                    # omegas apprises
                    reseau.init2()

                    reseau.x = x

                    reseau.Phase1()
                    reseau.Phase2()
                    reseau.Phase3()
                    reseau.Phase4()

    # Enregistre les parametres du reseau dans un fichier texte
    # Utilise le module pickle pour recuperer l'objet reseau (mais impossible de lire le fichier texte)
    with open("reseau.txt", "wb") as reseau_file:
        pickle.dump(reseau, reseau_file, protocol=pickle.HIGHEST_PROTOCOL)
    reseau_file.close()

    info_train_file.close()

    # Enregistre les parametres du reseau dans un fichier texte pour permettre de lire tous les parametres
    with open('log_neurones.txt', 'w+') as log_file:
        i = 0
        j = 0
        for couche in reseau.couches:
            log_file.write('\nCouche: ' + str(i) + '\n')
            j = 0
            for neurone in couche.neurones:
                log_file.write('\n    Neurone: ' + str(j) + '\n')
                log_file.write('        Theta: ' + str(neurone.theta) + '\n')
                log_file.write('        i    : ' + str(neurone.i) + '\n')
                log_file.write('        a    : ' + str(neurone.a) + '\n')
                log_file.write('        delta: ' + str(neurone.delta) + '\n')
                j = j + 1
            log_file.write('\nOmegas:\n' + str(couche.omegas) + '\n')
            log_file.write('\nDelta Omegas:\n' + str(couche.delta_omegas) + '\n')
            log_file.write('\nAmoins1:\n' + str(couche.amoins1) + '\n')
            i = i + 1
    log_file.close()

    # --------------------------------------------- VALIDATION CROISEE -------------------------------------------------
    with open("reseau.txt", "rb") as reseau_file:
        reseau = pickle.load(reseau_file)

    reseau.init2()

    # Variables pour le calcul du taux de succes
    true = int()
    essais = int()

    # Ouvrir le fichier texte contenant la liste des paths des fichiers a  utiliser pour la validation croisee
    with open(settings.mainpath + 'info_vc.txt') as info_vc_file:
        for line in info_vc_file:
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
                        for i in range(0, settings.nb_sorties):
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
                        for i in range(1, settings.nb_sorties):
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

                    # Faire seulement la phase 1 pour la validation croisee
                    reseau.Phase1()

                    # Recuperer toutes les valeurs des 'a' de la derniere couche
                    # La position de la valeur maximale dans cette liste correspondra au resultat obtenu
                    sortie_a = list()
                    for i in range(0, len(reseau.couches[-1].neurones)):
                        sortie_a.append(reseau.couches[-1].neurones[i].a)
                    max = -1000
                    index = 0
                    for i in range(0, settings.nb_sorties):
                        if sortie_a[i] > max:
                            max = sortie_a[i]
                            index = i

                    # Verifier sur notre resultat correspond a la veritable sortie
                    if settings.sortie_d[index]:
                        true = true + 1
                    essais = essais + 1

    taux_succes = float(true)/float(essais)
    print('Training: ' + str(k) + ' Taux de succes: ' + str(taux_succes))

    info_vc_file.close()


