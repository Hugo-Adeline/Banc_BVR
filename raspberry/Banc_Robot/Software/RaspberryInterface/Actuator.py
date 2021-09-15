# -*- coding: utf-8 -*-

from time import time, sleep

class Actuator():
    def __init__(self, category, subCategory, pin, interface):

        # Définition de l'actionneur
        self.category = category
        self.subCategory = subCategory
        self.pinType = pin[0]
        self.pin = pin [1]
        self.interface = interface
        self.position = 0


    def GetdBValues(self, numberOfGear= 2):

        # Création des valeurs associées aux actionneurs
        return {'Time': None}


    def GetOverrideData(self):

        # Gestion du texte et de la position des boutons associés aux actionneurs du menu ManualDiagnosisWindow
        if '+' in self.subCategory:
            column = 5
            text ='▶'
        elif '-' in self.subCategory:
            column = 3
            text ='◀'
        elif self.category == 'Electro_pompe':
            column = 3
            text ='▲'
        else:
            return None

        return column, text


    def Set(self, time= 0.5, state= None, actuatorType= None):

        # On active l'actionneur en fontion de son type ou en fonction du status passé en argument
        # Si l'argument "state" n'est pas vide, il prend la priorité sur le contrôle de l'actionneur
        if state != None:
            return self.interface.Set(self.pin, state)

        # En fonction du type d'actionneur, sa gestion dans le menu de DiagManuel peut nécessiter qu'il soit maintenu en position
        # La position est sauvegardée dans une variable pour simuler un effet toggle
        if actuatorType == 'S-Cam':
            if self.position == 0:
                self.position = 1
                return self.interface.Set(self.pin, 1)
            elif self.position == 1:
                self.position = 0
                return self.interface.Set(self.pin, 0)

        # Dans le cas d'une sélection simple, il faut aller modifier la position de l'actionneur opposé si il est activé pour revenir en position centrale
        elif self.subCategory == 'Sélection +':
            if self.interface.actuatorClass[self.category]['Sélection -'].position == 1:
                self.interface.actuatorClass[self.category]['Sélection -'].position = 0
                return self.interface.Set(self.interface.actuatorClass[self.category]['Sélection -'].pin, 0)
            elif self.position == 0:
                self.position = 1
                return self.interface.Set(self.pin, 1)
            else:
                return
        elif self.subCategory == 'Sélection -':
            if self.interface.actuatorClass[self.category]['Sélection +'].position == 1:
                self.interface.actuatorClass[self.category]['Sélection +'].position = 0
                return self.interface.Set(self.interface.actuatorClass[self.category]['Sélection +'].pin, 0)
            elif self.position == 0:
                self.position = 1
                return self.interface.Set(self.pin, 1)
            else:
                return

        # Pour le reste de actionneurs, on utilise un temps d'activation défini
        else:
            return self.interface.SetTime(self.pin, time)


    def GetTime(self, robotAttributes):

        # Aquisition du temps de monté en pression nominal
        # Vérification que l'actionneur est l'électro-pompe
        if self.category != "Electro_pompe":
            return None

        # Récupération des données nécessaires
        pressureSensor = self.interface.sensorClass['Pression']['Robot']
        target = robotAttributes['Sensors']['Pression']['Robot']['Max']

        # Démarrage du test
        t0 = time()                             #Sauvegarde du temps initial
        self.Set(state= 1)                      #Démarrage de la pompe
        sleep(1)
        while pressureSensor.Poll() < target:   #Boucle de régulation
            None
        t1 = time()                             #Sauvegarde du temps final
        self.Set(state= 0)                      #Arrêt de la pompe
        return round(t1 - t0, 1)                #Retour de la valeur trouvé avec un décimal
