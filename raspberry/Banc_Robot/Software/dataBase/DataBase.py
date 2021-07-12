# -*- coding: utf-8 -*-

import pandas as pd
import os
import subprocess
from ast import literal_eval


class DataBase():
    def __init__(self, path):
        self.path = path
        self.backupPath = None
        disk = os.popen("ls /media/pi").read()
        if disk != '':
                disk = disk[:-1]
                self.backupPath = '/media/pi/' + disk + '/raspberry/Banc_Robot/Software/dataBase/'

        # Création de l'entête
        self.header = ['Dictionnary']

        # Vérification de l'existence de la base de données
        if os.path.isfile(path):
            self.Backup()
            return

        # Création de la base de donnée si non existente
        else:
            df = pd.DataFrame([[{'Name': "Exemple",
                                 'Gears': 6,
                                 'Type': 'Hydraulique',
                                 'Sensors': {'Position': {'Sélection 1': {'Min': 1.56,
                                                                          'Max': 3.3,
                                                                          'Deviation': 0,
                                                                          'DeviationErr': 0,
                                                                          'ActuatorType': 'Toggle'},
                                                          'Engagement 1': {'Min': 0.82,
                                                                           'Max': 3.3,
                                                                           'Deviation': 0,
                                                                           'DeviationErr': 0,
                                                                           'ActuatorType': 'Linéaire'},
                                                          'Embrayage 1': {'Min': 1.14,
                                                                          'Max': 3.3,
                                                                          'Deviation': 0,
                                                                          'DeviationErr': 0,
                                                                          'ActuatorType': 'Bouton'}},
                                             'Pression': {'Robot': {'Min': 0.5,
                                                                    'Max': 2.5,
                                                                    'Deviation': 0,
                                                                    'DeviationErr': 0,
                                                                    'ActuatorType': 'Pompe'}},
                                             'Vitesse': {'Boîte de vitesses': {'Min': 0.5,
                                                                               'Max': 2.5,
                                                                               'Deviation': 0,
                                                                               'DeviationErr': 0,
                                                                               'ActuatorType': None}}},
                                 'Actuators': {'Electrovanne': {'Sélection +': {'Time': None},
                                                                'Sélection -': {'Time': None},
                                                                'Engagement +': {'Time': None},
                                                                'Engagement -': {'Time': None},
                                                                'Embrayage +': {'Time': None}},
                                               'Electro_pompe': {'Robot': {'Time': 6.5}}}}]],
                               columns= self.header)
            df.to_csv(self.path, index= False)
            self.Backup()

    def AddRobot(self, name, gears, Type, sensors, actuators):
        """
        Ajoute un robot à la base de données.

        Parameters
        ----------
        name : str
            Nom du robot.
        gears : int
            Nombre de rapports du robot.
        sensors : list
            Liste des capteurs avec leurs données.
        actuators : list
            Liste des actionneurs avec leurs données.

        Returns
        -------
        bool
            True: L'opération à été effectuée.
            False: Erreur dans le processus.
        """

        # Vérification que le nom n'est pas vide sinon
        if name == '' or name == None or name == 'null':
            return False

        # Ouverture de la base de données
        df = pd.read_csv(self.path)
        row_count, _ = df.shape

        # Vérification que le nom n'est pas déjà utilisé
        for i in range (row_count):
            if (literal_eval(df.values[i][0])['Name']==name):
                return False

        # Ajout de l'élément à la base de données
        df = pd.DataFrame([[{'Name': name,
                             'Gears': gears,
                             'Type': Type,
                             'Sensors': sensors,
                             'Actuators': actuators}]],
                          columns= self.header)
        df.to_csv(self.path, mode= 'a', index= False, header= None)
        self.Backup()

        # On retourne True lorsque l'élément a été ajouté
        return True

    def DeleteRobot(self, name):
        """
        Suppression d'un entrée de la base de données.

        Parameters
        ----------
        name : str
            Nom du robot.

        Returns
        -------
        bool
            True: L'opération à été effectuée.
            False: Erreur dans le processus.

        """
        # Ouverture de la base de données
        df = pd.read_csv(self.path)
        row_count, _ = df.shape

        # Vérification que la base de données a au moins 2 entrées
        if row_count < 2:
            return False

        # Recherche et suppression de l'élément
        for i in range (row_count):
            if (literal_eval(df.values[i][0])['Name']==name):
                df.drop(df.index[i], inplace=True)
                df.to_csv(self.path, index=False)
                self.Backup()
                return True

        # On retourne False si on a pas trouvé l'élément
        return False


    def GetRobotAttributes(self, name):
        """
        Retourne la liste des données associées au robot

        Parameters
        ----------
        name : str
            Nom du robot.

        Returns
        -------
        Robot : list
            Données du robot [Type, SubType, [Sensors], [Actuators]].

        """
        # Ouverture de la base de données
        df = pd.read_csv(self.path)
        row_count, _ = df.shape

        # Recherche de l'élément à retourner
        for i in range (row_count):
            robot = literal_eval(df.values[i][0])
            if (robot['Name']==name):
                return robot

        # On retourne None si rien n'a été trouvé
        return None


    def GetRobotNameList(self):
        """
        Retourne une liste contenant le nom des robots présent dans la base de données.

        Returns
        -------
        RobotNameList : list
            Liste des noms des robots.

        """

        # Création de la variable de stockage
        robotNameList = []

        # Ouverture de la base de données
        df = pd.read_csv(self.path)
        row_count, _ = df.shape

        # Ajout des noms de robots
        for i in range (row_count):
            robot = literal_eval(df.values[i][0])
            robotNameList.append(robot['Name'])
        robotNameList.sort()

        # Retour de la liste des robots
        return robotNameList


    def ModifyRobot(self, oldName, name, gears, Type, sensors, actuators):
        """
        Modifie l'entrée de la base de donnée avec les nouvelles données spécifées.

        Parameters
        ----------
        oldName : str
            Ancien nom du robot.
        name : str
            Nouveau nom du robot.
        gears : int
            Nombre de rapports du robot.
        sensors : list
            Liste des capteurs avec leurs données.
        actuators : list
            Liste des actionneurs avec leurs données.

        Returns
        -------
        bool
            True: L'opération à été effectuée.
            False: Erreur dans le processus.
        """

        # Ouverture de la base de données
        df = pd.read_csv(self.path)
        row_count, _ = df.shape

        # Recherche et suppression de l'ancienne entrée
        for i in range (row_count):
            if (literal_eval(df.values[i][0])['Name']==oldName):
                df.drop(df.index[i], inplace=True)
                df.to_csv(self.path, index=False)
                break

        # Création et ajout de la nouvelle entrée
        df = pd.DataFrame([[{'Name': name,
                             'Gears': gears,
                             'Type': Type,
                             'Sensors': sensors,
                             'Actuators': actuators}]],
                          columns= self.header)
        df.to_csv(self.path, mode= 'a', index= False, header= None)
        self.Backup()

        # On retourne True si l'opération a été effectuée
        return True

    def Backup(self):
        if self.backupPath == None:
            return
        command = 'cp ' + self.path + ' ' + self.backupPath
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        process.communicate()[0]
        return
