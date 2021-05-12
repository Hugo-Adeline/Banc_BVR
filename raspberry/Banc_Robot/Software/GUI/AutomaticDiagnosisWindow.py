# -*- coding: utf-8 -*-

import tkinter as tk
from GUI.GUI_utils import SwitchWindow, Popup
from time import sleep
from Thread import Thread
from numpy import mean
from GUI.AutoDiag_utils import LowerPressure

class AutomaticDiagnosisWindow():
    def __init__(self, root):

        # Définition de la fenêtre Parent
        self.root = root

        # Création de la frame qui contient la page
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)

        # Création des cadres
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)
        self.centerSubFrame = tk.Frame(self.masterFrame, relief= 'groove', bd= 1, bg= 'white')

        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerSubFrame.pack(side= 'top', expand = True)

        # Définition des variables
        self.robotSelected = tk.StringVar()
        self.labelChoix = tk.StringVar()
        self.robotAttributes = None
        self.sensorErrDict = {}
        self.actuatorErrDict = {}
        self.errCount = 0


    def Setup(self):

        # Récupération de la robot sélectionnée pour le diagnostique
        self.robotSelected = self.root.mainMenuWindow.robotSelected

        # Création des boutons et labels fixes
        self.label = tk.Label(self.titleFrame, text="Diagnostique automatique", bg= self.root.defaultbg)
        self.label.config(font = self.root.fontTitle)
        self.label.pack(pady = self.root.titlePadY)

        self.diagConsole = tk.Listbox(self.centerSubFrame, bg= 'white', width= 75, height= 25)
        self.diagConsole.pack()

        self.buttonRetour = tk.Button(self.masterFrame, text= "Retour", command= self.root.mainMenuWindow.Open)
        self.buttonRetour.config(font = self.root.fontButton)
        self.buttonRetour.place(relx= self.root.retourRelX, rely= self.root.retourRelY)

        self.buttonRelancer = tk.Button(self.masterFrame, text= "Relancer", command= self.Open)
        self.buttonRelancer.config(font = self.root.fontButton)
        self.buttonRelancer.place(relx= self.root.validerRelX, rely= self.root.retourRelY)


    def Open(self):
        self.robotSelected = self.root.mainMenuWindow.robotSelected
        if self.root.activeFrame == self.root.mainMenuWindow.masterFrame:
            retour = Popup(self, 2, texte= "Démarrer le diagnostique du robot " + str(self.robotSelected.get()) + " ?", valider= "Oui", fermer= "Non")
            if retour == False:
                return
        SwitchWindow(self.masterFrame,self.root)
        self.Refresh()
        self.autoDiagThread = Thread('autoDiagThread', self.AutoDiag, loop= False)
        self.autoDiagThread.start()

    def Refresh(self):
        self.robotAttributes = self.root.dB.GetRobotAttributes(self.robotSelected.get())
        return


    def AutoDiag(self):
        self.buttonRetour.config(state= 'disabled')
        self.buttonRelancer.config(state= 'disabled')

        self.diagConsole.insert('end', "[AutoDiag] : Initialisation du diagnostique automatique pour le robot: " + self.robotAttributes['Name'] + '...')
        self.errCount = 0

        # Création du dictionnaire des erreurs
        for category in self.robotAttributes['Sensors']:
            for subCategory in self.robotAttributes['Sensors'][category]:
                try:
                    self.sensorErrDict[category]
                except:
                    self.sensorErrDict[category] = {}
                self.sensorErrDict[category][subCategory] = []
        for category in self.robotAttributes['Actuators']:
            for subCategory in self.robotAttributes['Actuators'][category]:
                try:
                    self.actuatorErrDict[category]
                except:
                    self.actuatorErrDict[category] = {}
                self.actuatorErrDict[category][subCategory] = []

        # Test du branchement des capteurs
        self.diagConsole.insert('end', "[AutoDiag] : Test du branchement des capteurs en cours...")

        sensorValues = {}
        for category in self.sensorErrDict:
            sensorValues[category] = {}
            for subCategory in self.sensorErrDict[category]:
                    sensorValues[category][subCategory] = []
        for i in range(1000):
            for category in sensorValues:
                    for subCategory in sensorValues[category]:
                            sensorValues[category][subCategory].append(self.root.interface.sensorClass[category][subCategory].Poll())
        for category in sensorValues:
                    for subCategory in sensorValues[category]:
                            avgVal = mean(sensorValues[category][subCategory])
                            variance = 0
                            for i in sensorValues[category][subCategory]:
                                variance += (i - avgVal)**2
                            variance = variance / len(sensorValues[category][subCategory])
                            std_dev = variance**(0.5)

                            sensorValues[category][subCategory] = std_dev
                            if std_dev >= 2*self.robotAttributes['Sensors'][category][subCategory]['Deviation']:
                                    self.diagConsole.insert('end', "[Erreur] : Le capteur "  + category + ' ' + subCategory +  " est débranché.")
                                    self.diagConsole.itemconfig('end', fg= 'red')
                                    self.sensorErrDict[category][subCategory].append('Capteur débranché')
                                    self.errCount += 1

        if self.errCount == 0:
            self.diagConsole.insert('end', "[AutoDiag] : Tous les capteurs sont branchés.")
            self.diagConsole.itemconfig('end', fg= 'green')
        elif 'Capteur débranché' in self.sensorErrDict['Pression']['Robot']:
            self.diagConsole.insert('end', "[AutoDiag] : Impossible de continuer le diagnostique.")
            self.Stop()
            return

        # Test de la partie pression
        if self.robotAttributes['Type'] != 'Electrique':
            self.diagConsole.insert('end', "[AutoDiag] : Test du système de pression...")

            pressureSensor = self.root.interface.sensorClass['Pression']['Robot']
            pressureActuator = self.root.interface.actuatorClass['Electro_pompe']['Robot']

            self.diagConsole.insert('end', "[AutoDiag] : Abaissement de la pression au minimum...")
            # La fonction d'abaissement de pression permet de vérifier la pression minimale
            validation = LowerPressure(self)
            if validation == False:
                self.diagConsole.insert('end', "[Erreur] : Impossible de baisser la pression via les actionneurs.")
                self.diagConsole.itemconfig('end', fg= 'red')
                self.sensorErrDict['Pression']['Robot'].append('Capteur défaillant')
                self.diagConsole.insert('end', "[AutoDiag] : Impossible de continuer le diagnostique.")

                self.Stop()
                return

            # On utilise la variable Time + 1sec pour tester si la pompe atteint le max
            initPressure = pressureSensor.Poll()
            print(initPressure)
            self.diagConsole.insert('end', "[AutoDiag] : Test de la pompe...")
            pressureActuator.Set(state = 1)
            sleep(self.robotAttributes['Actuators']['Electro_pompe']['Robot']['Time'] + 1)
            pressureActuator.Set(state = 0)
            finalPressure = pressureSensor.Poll()
            print(finalPressure)
            dev = self.robotAttributes['Sensors']['Pression']['Robot']['Deviation']
            target = self.robotAttributes['Sensors']['Pression']['Robot']['Max']

            if finalPressure >= target - self.root.interface.margin * dev :
                self.diagConsole.insert('end', "[AutoDiag] : Le système de pression fonctionne.")
                self.diagConsole.itemconfig('end', fg= 'green')
            else:
                # Emplacement du test pour vérifier si la pompe fonctionne mais pas le capteur
                self.diagConsole.insert('end', "[Erreur] : Le capteur de pression ou la pompe est défaillant(e).")
                self.diagConsole.itemconfig('end', fg= 'red')
                self.sensorErrDict['Pression']['Robot'].append('Capteur défaillant')
                self.actuatorErrDict['Electro_pompe']['Robot'].append('Actionneur défaillant')
                self.errCount +=1

                self.diagConsole.insert('end', "[AutoDiag] : Impossible de continuer le diagnostique.")

                self.Stop()
                return


        # Test des capteurs et actionneurs
        self.diagConsole.insert('end', "[AutoDiag] : Début du test des capteurs de position...")
        for subCategory in self.robotAttributes['Sensors']['Position']:
            if self.sensorErrDict['Position'][subCategory] != []:
                continue
            pressureActuator.Set(state= 1)
            while self.robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(5):
                sleep(0.1)
            pressureActuator.Set(state= 0)
            minSensorMes, maxSensorMes = self.root.interface.sensorClass['Position'][subCategory].GetMinMax(self.robotAttributes)
            minSensor, maxSensor = self.robotAttributes['Sensors']['Position'][subCategory]['Min'],  self.robotAttributes['Sensors']['Position'][subCategory]['Max']
            dev = self.robotAttributes['Sensors']['Position'][subCategory]['Deviation']
            print(subCategory, "minmes = ", minSensorMes, " ;min = ", minSensor, " ;maxSensorMes = ", maxSensorMes, " ;max = ", maxSensor)
            error = False
            if minSensorMes > minSensor + self.root.interface.margin*dev or minSensorMes < minSensor - self.root.interface.margin*dev:
                error = True
            if maxSensorMes > maxSensor + self.root.interface.margin*dev or maxSensorMes < maxSensor - self.root.interface.margin*dev:
                error = True
            if error:
                self.diagConsole.insert('end', "[Erreur] : Le capteur de Position " + subCategory + " ou l'actionneur de " + subCategory.rstrip(' 0123456789') + " est défaillant.")
                self.diagConsole.itemconfig('end', fg= 'red')
                self.errCount +=1
        self.diagConsole.insert('end', "[AutoDiag] : Fin du test des capteurs de position.")

        self.Stop()
        return

    def Stop(self):

        # Affichage du nombre d'erreur avec un code couleur approrié
        self.diagConsole.insert('end', "[AutoDiag] : Le diagnostique a trouvé " + str(self.errCount) + " erreurs.")
        if self.errCount == 0:
            self.diagConsole.itemconfig('end', fg= 'green')
        elif self.errCount == 1:
            self.diagConsole.itemconfig('end', fg= 'orange')
        elif self.errCount > 1:
            self.diagConsole.itemconfig('end', fg= 'red')

        self.diagConsole.insert('end', "[AutoDiag] : Le diagnostique est terminé.")

        self.diagConsole.insert('end', "[AutoDiag] : Création du résumé du diagnostique...")

        for category in self.sensorErrDict:
            for subCategory in self.sensorErrDict[category]:
                errors = self.sensorErrDict[category][subCategory]
                if errors != []:
                    for error in errors:
                        self.diagConsole.insert('end', "[Conclusion] (" + category + ' ' + subCategory + ") : " + error)
                        print('[Conclusion] (' + category + ' ' + subCategory + ') : ' + error)
        for category in self.actuatorErrDict:
            for subCategory in self.actuatorErrDict[category]:
                errors = self.actuatorErrDict[category][subCategory]
                if errors != []:
                    for error in errors:
                        self.diagConsole.insert('end', "[Conclusion] (" + category + ' ' + subCategory + ") : " + error)
                        print('[Conclusion] (' + category + ' ' + subCategory + ') : ' + error)

        self.buttonRelancer.config(state= 'normal')
        self.buttonRetour.config(state= 'normal')
        return
