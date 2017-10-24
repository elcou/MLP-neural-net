# TXT_FILE.py
#
# Ce module fait le tri des donnees contenues dans les fichiers mfc.
# Il y a trois methodes distinctes pour faire le tri et choisir le nombre approprie de donnees.
# La methode a fait le tri des donnees par l'energie statique
# La methode b fait le tri des donnees par l'energie dynamique
# La methode c fait le trie des donnees par la moyenne des deux energies.
# Par la suite, des fichiers texte des 40,50,60 valeurs les plus hautes sont crees.
#
# Auteurs: Elodie Couturier
#          Carl   Martin
#          Radu   Vacarciuc
#
# Date de creation: 10 juin 2017
# ######################################################################################################################

import os
import operator
import numpy as np


class TxtFile:

    def __init__(self, name):

        self.error_flag = False

        self.lines_of_data = []
        try:
            with open(name) as txt_file:
                col = 0
                for line in txt_file:
                    self.lines_of_data.append([])
                    for data in line.split():
                        self.lines_of_data[col].append(float(data))
                    col += 1

            txt_file.close()

        except FileNotFoundError:
            self.error_flag = True

        self.name = name
        self.value13 = []
        self.valueA = []
        self.value26 = []
        self.valueB = []
        self.valueC = []

    # Methode qui fait le tri avec l'energie statique
    def method_a(self):

        index = 0
        for line in self.lines_of_data:
            self.value13.append([line[12]])
            self.value13[index].append(index)
            index += 1
        self.valueA = sorted(self.value13, key=operator.itemgetter(0), reverse=True)

        self.write_file(self.valueA, 40, 'A')
        self.write_file(self.valueA, 50, 'A')
        self.write_file(self.valueA, 60, 'A')

    # Methode qui fait le tri avec l'energie dynamique
    def method_b(self):

        index = 0
        for line in self.lines_of_data:
            self.value26.append([line[25]])
            self.value26[index].append(index)
            index += 1
        self.valueB = sorted(self.value26, key=operator.itemgetter(0), reverse=True)

        self.write_file(self.valueB, 40, 'B')
        self.write_file(self.valueB, 50, 'B')
        self.write_file(self.valueB, 60, 'B')

    # Methode qui fait le tri avec la moyenne des deux energies
    def method_c(self):

        value_moy = []
        for line in range(0, len(self.value13)):
            value_moy.append([(self.value13[line][0] + self.value26[line][0])/2])
            value_moy[self.value13[line][1]].append(self.value13[line][1])
        self.valueC = sorted(value_moy, key=operator.itemgetter(0), reverse=True)

        self.write_file(self.valueC, 40, 'C')
        self.write_file(self.valueC, 50, 'C')
        self.write_file(self.valueC, 60, 'C')

    # Methode qui cre des nouveaux fichiers mfc avec les donnees gardees selon la methode utilisee.
    def write_file(self, sorted_values, nb_of_lines, method):

        file_name, file_extension = os.path.splitext(self.name)

        f = open(file_name + '_method' + method + '_' + str(nb_of_lines) + '.txt', 'w+')

        line = 0
        try:
            while line < nb_of_lines:
                for col in range(0, 26):
                    f.write(str(self.lines_of_data[sorted_values[line][1]][col]))
                    f.write(' ')
                f.write('\n')

                line += 1

            f.close()

        except IndexError:

            # Pour effacer ce qui avait ete ecrit avant d'intercepter l'erreur
            f.close()
            f = open(file_name + '_method' + method + '_' + str(nb_of_lines) + '.txt', 'w+')

            nb_lines_add = nb_of_lines - len(self.lines_of_data)

            # Copie lignes initiales (en ordre selon sorted_values)
            new_lines = []
            for line in sorted_values:
                new_lines.append(self.lines_of_data[line[1]])

            # xp: index des lignes a utiliser pour l'interpolation
            # x: index des lignes a creer
            xp = [1, nb_lines_add+2]
            x = []
            for i in range(2, nb_lines_add+2):
                x.append(i)

            line = 0
            lines_add = []
            while line < nb_lines_add:
                lines_add.append([])
                line += 1

            # yp: valeurs a utiliser pour l'interpolation
            for col in range(0, 26):
                yp = [new_lines[0][col], new_lines[1][col]]
                interpol = np.interp(x, xp, yp)
                for line in range(0, nb_lines_add):
                    lines_add[line].append(float(interpol[line]))

            for line in range(0, nb_lines_add):
                new_lines.insert(line+1, lines_add[line])

            for line in new_lines:
                for data in line:
                    f.write(str(data))
                    f.write(' ')
                f.write('\n')

            f.close()
