# REPO_MANIP.py
#
# Module servant au parcours d'un repertoire pour lister le chemin de tous les fichiers mfc qui y sont contenus et
# genere de nouveaux fichiers triees selon des methodes differentes.
#
# Ce module supprime aussi tous les fichiers generes anterieurement.
#
# Auteurs: Elodie Couturier
#          Carl   Martin
#          Radu   Vacarciuc
#
# Date de creation: 10 juin 2017
# ######################################################################################################################

from os import walk
import settings
from txt_file import *


class RepoManip:

    def __init__(self):
        self.path = []

        self.repo_tree()

    # Methode qui construit la liste de repertoire a partir de l'arborescence des fichiers mfc
    def repo_tree(self):

        self.path = []

        repo1 = []
        for (dirpath, dirnames, filenames) in walk(settings.mainpath):
            repo1.extend(dirnames)
            break

        for dirnames1 in repo1:
            repo2 = []
            for (dirpath, dirnames, filenames) in walk(settings.mainpath + dirnames1):
                repo2.extend(dirnames)
                break

            for dirnames2 in repo2:
                repo3 = []
                for (dirpath, dirnames, filenames) in walk(settings.mainpath + dirnames1 + '/' + dirnames2):
                    repo3.extend(dirnames)
                    break

                for dirnames3 in repo3:
                    repo4 = []
                    for (dirpath, dirnames, filenames) in walk(settings.mainpath + dirnames1 + '/' + dirnames2 +
                                                               '/' + dirnames3):
                        repo4.extend(filenames)
                        break

                    for dirnames4 in repo4:
                        file_name, file_extension = os.path.splitext(dirnames4)
                        if file_extension == '.txt' and file_name[:4] != 'info':
                            self.path.append(os.path.join(settings.mainpath, dirnames1, dirnames2, dirnames3, dirnames4))

    # Methode qui supprime les fichiers generes anterieurement par le script pour recommencer a zero
    def delete_files(self):

        for i in range(0, len(self.path)):
            file_name, file_extension = os.path.splitext(self.path[i])

            if file_extension == '.txt' and \
                    (file_name[-2:] == '40' or file_name[-2:] == '50' or file_name[-2:] == '60'):
                os.remove(self.path[i])

    # Methode generant de nouveaux fichiers triees selon des methodes differentes
    def create_new_files(self):

        # Supprime tous les fichiers autres que les fichiers texte initiaux
        self.delete_files()

        # Reconstruit la liste de toutes les adresses des fichiers texte contenus dans le repertoire
        self.repo_tree()

        # Traite tous les fichiers texte de la liste
        for file in self.path:
            # Initialise le fichier courant comme etant un objet TxtFile.
            # TxtFile enregistre les donnees contenues dans le fichier texte.
            current_file = TxtFile(file)

            if ~current_file.error_flag:
                # Cree 9 nouveaux fichiers texte a partir du fichier courant.
                current_file.method_a()  # Methode A 40, 50, 60 lignes.
                current_file.method_b()  # Methode B 40, 50, 60 lignes.
                current_file.method_c()  # Methode C 40, 50, 60 lignes.


