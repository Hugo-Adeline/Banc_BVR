# -*- coding: utf-8 -*-

import tkinter as tk
from GUI.GUI_utils import SwitchWindow, Popup
from time import sleep
from Thread import Thread
from numpy import mean
from GUI.AutoDiag_utils import LowerPressure
from PDF.PDF import PDF

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

        # Récupération de la robot sélectionnée pour le diagnostic
        self.robotSelected = self.root.mainMenuWindow.robotSelected

        # Création des boutons et labels fixes
        self.label = tk.Label(self.titleFrame, text="Diagnostic automatique", bg= self.root.defaultbg)
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
            retour = Popup(self, 2, texte= "Démarrer le diagnostic du robot " + str(self.robotSelected.get()) + " ?", valider= "Oui", fermer= "Non")
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

        self.diagConsole.insert('end', "[AutoDiag] : Initialisation du diagnostic automatique pour le robot: " + self.robotAttributes['Name'] + '...')
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

        # Récupération de l'écart-type du bruit des capteurs
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
                            # Le capteur est-il branché ?
                            if std_dev >= 2*self.robotAttributes['Sensors'][category][subCategory]['Deviation']:
                                    self.diagConsole.insert('end', "[Erreur] : (0) Le capteur "  + category + ' ' + subCategory +  " est débranché.")
                                    self.diagConsole.itemconfig('end', fg= 'red')
                                    self.sensorErrDict[category][subCategory].append('Erreur 0: Capteur débranché')
                                    self.errCount += 1

        if self.errCount == 0:
            self.diagConsole.insert('end', "[AutoDiag] : Tous les capteurs sont branchés.")
            self.diagConsole.itemconfig('end', fg= 'green')
        # Le capteur de pression est-il branché ?
        elif 'Erreur 0: Capteur débranché' in self.sensorErrDict['Pression']['Robot']:
            self.diagConsole.insert('end', "[AutoDiag] : Impossible de continuer le diagnostic sans le capteur de pression.")
            self.Stop()
            return

        # Test de la partie pression
        if self.robotAttributes['Type'] != 'Electrique':
            self.diagConsole.insert('end', "[AutoDiag] : Test du système de pression...")

            pressureSensor = self.root.interface.sensorClass['Pression']['Robot']
            pressureActuator = self.root.interface.actuatorClass['Electro_pompe']['Robot']

            self.diagConsole.insert('end', "[AutoDiag] : Abaissement de la pression au minimum...")
            # Abaissement de la pression via l'activation des actionneurs de manière répétée
            LowerPressure(self)
            margin = self.root.interface.margin
            dev = self.robotAttributes['Sensors']['Pression']['Robot']['Deviation']
            target = self.robotAttributes['Sensors']['Pression']['Robot']['Min']
            pressure = pressureSensor.Poll(10)
            # La pression a-t-elle atteint Pmin ?
            if (pressure > target + margin*dev) or (pressure < target - margin*dev):
                self.diagConsole.insert('end', "[Erreur] : Valeur du capteur de pression non conforme.")
                self.diagConsole.itemconfig('end', fg= 'red')
                self.sensorErrDict['Pression']['Robot'].append('Erreur 1: Pression min érronée')
                self.diagConsole.insert('end', "[AutoDiag] : Impossible de continuer le diagnostic.")
                self.Stop()
                return
            else:
                self.diagConsole.insert('end', "[AutoDiag] : La pression minimale a bien été atteinte.")
                self.diagConsole.itemconfig('end', fg= 'green')
            # On utilise la variable Time + 1sec pour tester si la pompe atteint le max
            initPressure = pressureSensor.Poll(10)
            print(initPressure)
            self.diagConsole.insert('end', "[AutoDiag] : Test de la pompe...")
            pressureActuator.Set(state = 1)
            sleep(self.robotAttributes['Actuators']['Electro_pompe']['Robot']['Time'] + 1)
            pressureActuator.Set(state = 0)
            finalPressure = pressureSensor.Poll(10)
            print(finalPressure)
            margin = self.root.interface.margin
            dev = self.robotAttributes['Sensors']['Pression']['Robot']['Deviation']
            target = self.robotAttributes['Sensors']['Pression']['Robot']['Max']
            # La pression a-t-elle atteint Pmax ?
            if finalPressure >= target - margin * dev:
                self.diagConsole.insert('end', "[AutoDiag] : La pression maximale a bien été atteinte.")
                self.diagConsole.itemconfig('end', fg= 'green')
            else:
                # Acquisition des valeurs max d'un actionneur
                verif = 0
                for subCategory in self.robotAttributes['Sensors']['Position']:
                    if self.sensorErrDict['Position'][subCategory] != []:
                        continue
                    minSensorMes, maxSensorMes = self.root.interface.sensorClass['Position'][subCategory].GetMinMax(self.robotAttributes)
                    minSensor, maxSensor = self.robotAttributes['Sensors']['Position'][subCategory]['Min'],  self.robotAttributes['Sensors']['Position'][subCategory]['Max']
                    dev = self.robotAttributes['Sensors']['Position'][subCategory]['Deviation']
                    print(subCategory, "minmes = ", minSensorMes, " ;min = ", minSensor, " ;maxSensorMes = ", maxSensorMes, " ;max = ", maxSensor)
                    error = False
                    if minSensorMes > minSensor + self.root.interface.margin*dev or minSensorMes < minSensor - self.root.interface.margin*dev:
                        error = True
                    if maxSensorMes > maxSensor + self.root.interface.margin*dev or maxSensorMes < maxSensor - self.root.interface.margin*dev:
                        error = True
                    verif = 1
                    if error == False:
                        break
                # Y'a-t-il un actionneur à tester
                if verif == 0 :
                    self.diagConsole.insert('end', "[Erreur] : Impossible d'activer un actionneur hydraulique.")
                    self.diagConsole.itemconfig('end', fg= 'red')
                    self.diagConsole.insert('end', "[Erreur] : Le capteur de pression et/ou la pompe est défaillant(e).")
                    self.diagConsole.itemconfig('end', fg= 'red')
                    self.sensorErrDict['Pression']['Robot'].append('Erreur 3: Valeur capteur érronée')
                    self.actuatorErrDict['Electro_pompe']['Robot'].append('Erreur 4: Défaut actionneur')
                    self.errCount +=1
                else:
                    # Les valeurs sont-elles égales à celles en mémoire ?
                    if error == True:
                        self.diagConsole.insert('end', "[Erreur] : La pompe est défaillante.")
                        self.diagConsole.itemconfig('end', fg= 'red')
                        self.actuatorErrDict['Electro_pompe']['Robot'].append('Erreur 4: Défaut actionneur')
                    else:
                        self.diagConsole.insert('end', "[Erreur] : Le capteur de pression est défaillant.")
                        self.diagConsole.itemconfig('end', fg= 'red')
                        self.sensorErrDict['Pression']['Robot'].append('Erreur 3: Valeur capteur érronée')
                self.errCount +=1
                self.diagConsole.insert('end', "[AutoDiag] : Impossible de continuer le diagnostic.")
                self.Stop()
                return
            # Attente 1 minute et sauvegarde de la pression
            self.diagConsole.insert('end', "[AutoDiag] : Début du test de maintient de la pression pendant 1 minute...")
            sleep(60)
            pressure = pressureSensor.Poll(10)
            self.diagConsole.insert('end', "[AutoDiag] : Fin du test.")
            # La perte pression est-elle trop élevée ?
            print("Pinit = ", finalPressure, "; Pfinal = ", pressure)
            if pressure < finalPressure - 0.5:
                self.actuatorErrDict['Electro_pompe']['Robot'].append('Erreur 2: Perte de pression')
                self.diagConsole.insert('end', "[Erreur] : Le robot ne tient pas la pression.")
                self.diagConsole.itemconfig('end', fg= 'red')
                self.errCount +=1
                self.diagConsole.insert('end', "[AutoDiag] : Impossible de continuer le diagnostic.")
                self.Stop(pressureSensorTest= True)
                return
            self.diagConsole.insert('end', "[AutoDiag] : Le robot maintient la pression.")
            self.diagConsole.itemconfig('end', fg= 'green')
            self.diagConsole.insert('end', "[AutoDiag] : Le système de pression fonctionne.")
            self.diagConsole.itemconfig('end', fg= 'green')
        # Test des capteurs et actionneurs
        self.diagConsole.insert('end', "[AutoDiag] : Début du test des capteurs de position...")
        for subCategory in self.robotAttributes['Sensors']['Position']:
            # Le capteur est-il branché
            if self.sensorErrDict['Position'][subCategory] != []:
                continue
            # Activation de la pompe jusqu'à Pmax
            pressureActuator.Set(state= 1)
            while self.robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(10):
                sleep(0.1)
            pressureActuator.Set(state= 0)
            # Vérification des valeurs min/max du capteur
            minSensorMes, maxSensorMes = self.root.interface.sensorClass['Position'][subCategory].GetMinMax(self.robotAttributes)
            minSensor, maxSensor = self.robotAttributes['Sensors']['Position'][subCategory]['Min'],  self.robotAttributes['Sensors']['Position'][subCategory]['Max']
            dev = self.robotAttributes['Sensors']['Position'][subCategory]['Deviation']
            print(subCategory, "minmes = ", minSensorMes, " ;min = ", minSensor, " ;maxSensorMes = ", maxSensorMes, " ;max = ", maxSensor)
            error = False
            errMin = False
            errMax = False
            if minSensorMes > minSensor + self.root.interface.margin*dev or minSensorMes < minSensor - self.root.interface.margin*dev:
                error = True
                errMin = True
            if maxSensorMes > maxSensor + self.root.interface.margin*dev or maxSensorMes < maxSensor - self.root.interface.margin*dev:
                error = True
                errMax = True
            if error:
                if self.robotAttributes['Sensors']['Position'][subCategory]['ActuatorType'] == 'S-Shaft':
                    self.diagConsole.insert('end', "[Erreur] : Défaillance sur le système S-Cam, impossible de déterminer le défaut.")
                    self.diagConsole.itemconfig('end', fg= 'red')
                    self.diagConsole.insert('end', "[Erreur] : Le capteur de Position " + subCategory + " est à tester.")
                    self.diagConsole.itemconfig('end', fg= 'red')
                    self.sensorErrDict['Position'][subCategory].append('Erreur 3: Valeur capteur érronée')
                    self.errCount +=1
                    self.diagConsole.insert('end', "[Erreur] : L'actionneur de " + subCategory.rstrip(' 0123456789') + " + est à tester.")
                    self.diagConsole.itemconfig('end', fg= 'red')
                    self.actuatorErrDict['Electrovanne'][subCategory.rstrip('0123456789') + '+'].append('Erreur 4: Défaut actionneur')
                    self.errCount +=1
                    continue
                # Activation de la pompe jusqu'à Pmax
                pressureActuator.Set(state= 1)
                while self.robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(10):
                    sleep(0.1)
                pressureActuator.Set(state= 0)
                # Récupération et sauvegarde de la valeur de pression initiale
                initPressure = pressureSensor.Poll(10)
                # Activation de l'actionneur plusieurs fois (on utilise la fonction GetMinMax)
                for i in range(3):
                    self.root.interface.sensorClass['Position'][subCategory].GetMinMax(self.robotAttributes)
                # Récupération et sauvegarde de la valeur de pression finale
                finalPressure = pressureSensor.Poll(10)
                # Les valeurs de pression sont-elles égales ?
                dev = self.robotAttributes['Sensors']['Pression']['Robot']['Deviation']
                margin = self.root.interface.margin
                if finalPressure <= initPressure - margin * dev:
                    self.diagConsole.insert('end', "[Erreur] : Le capteur de Position " + subCategory + " est défaillant.")
                    self.diagConsole.itemconfig('end', fg= 'red')
                    self.sensorErrDict['Position'][subCategory].append('Erreur 3: Valeur capteur érronée')
                    self.errCount +=1
                else:
                    if errMax and errMin:
                        self.diagConsole.insert('end', "[Erreur] : Les actionneurs de " + subCategory.rstrip(' 0123456789') + " sont défaillants.")
                        self.diagConsole.itemconfig('end', fg= 'red')
                        self.actuatorErrDict['Electrovanne'][subCategory.rstrip('0123456789') + '+'].append('Erreur 4: Défaut actionneur')
                        self.errCount +=1
                        try:
                            self.actuatorErrDict['Electrovanne'][subCategory.rstrip('0123456789') + '-'].append('Erreur 4: Défaut actionneur')
                            self.errCount +=1
                        except:
                            None
                    elif errMax:
                        self.diagConsole.insert('end', "[Erreur] : L'actionneur de " + subCategory.rstrip(' 0123456789') + " + est défaillant.")
                        self.diagConsole.itemconfig('end', fg= 'red')
                        self.actuatorErrDict['Electrovanne'][subCategory.rstrip('0123456789') + '+'].append('Erreur 4: Défaut actionneur')
                        self.errCount +=1
                    elif errMin:
                        try:
                            self.actuatorErrDict['Electrovanne'][subCategory.rstrip('0123456789') + '-'].append('Erreur 4: Défaut actionneur')
                            self.diagConsole.insert('end', "[Erreur] : L'actionneur de " + subCategory.rstrip(' 0123456789') + " - est défaillant.")
                            self.diagConsole.itemconfig('end', fg= 'red')
                            self.errCount +=1
                        except:
                            self.diagConsole.insert('end', "[Erreur] : L'actionneur de " + subCategory.rstrip(' 0123456789') + " + est défaillant.")
                            self.diagConsole.itemconfig('end', fg= 'red')
                            self.actuatorErrDict['Electrovanne'][subCategory.rstrip('0123456789') + '+'].append('Erreur 4: Défaut actionneur')
                            self.errCount +=1

        self.diagConsole.insert('end', "[AutoDiag] : Fin du test des capteurs de position.")

        self.Stop(pressureSensorTest= True)
        return

    def Stop(self, pressureSensorTest= False):

        # Affichage du nombre d'erreur avec un code couleur approrié
        self.diagConsole.insert('end', "[AutoDiag] : Le diagnostic a trouvé " + str(self.errCount) + " erreur(s).")
        if self.errCount == 0:
            self.diagConsole.itemconfig('end', fg= 'green')
        else:
            self.diagConsole.itemconfig('end', fg= 'red')

        self.diagConsole.insert('end', "[AutoDiag] : Abaissement de la pression au minimum...")
        LowerPressure(self, pressureSensorTest)
        self.diagConsole.insert('end', "[AutoDiag] : Création du résumé du diagnostic...")

        for category in self.sensorErrDict:
            for subCategory in self.sensorErrDict[category]:
                errors = self.sensorErrDict[category][subCategory]
                if errors != []:
                    for error in errors:
                        self.diagConsole.insert('end', "[Conclusion] (" + category + ' ' + subCategory + ") : " + error)
                        self.diagConsole.itemconfig('end', fg= 'blue')
                        print('[Conclusion] (' + category + ' ' + subCategory + ') : ' + error)
        for category in self.actuatorErrDict:
            for subCategory in self.actuatorErrDict[category]:
                errors = self.actuatorErrDict[category][subCategory]
                if errors != []:
                    for error in errors:
                        self.diagConsole.insert('end', "[Conclusion] (" + category + ' ' + subCategory + ") : " + error)
                        self.diagConsole.itemconfig('end', fg= 'blue')
                        print('[Conclusion] (' + category + ' ' + subCategory + ') : ' + error)

        self.diagConsole.insert('end', "[AutoDiag] : Fin du diagnostic automatique.")

        pdf = PDF()
        pdf.add_page()
        pdf.setup()
        pdf.add_robot(self.robotSelected.get())
        for category in self.sensorErrDict:
            for subCategory in self.sensorErrDict[category]:
                errList = self.sensorErrDict[category][subCategory]
                if len(errList) != 0:
                    for error in errList:
                        if 'Robot' in subCategory:
                            pdf.add_error('Pression', error)
                        elif 'Sélection' in subCategory:
                            pdf.add_error('Sélection', error)
                        elif 'Embrayage' in subCategory:
                            pdf.add_error('Embrayage', error)
                        elif 'Engagement' in subCategory:
                            pdf.add_error('Engagement', error)
                        else:
                            pdf.add_error('Autre', error)

        for category in self.actuatorErrDict:
            for subCategory in self.actuatorErrDict[category]:
                errList = self.actuatorErrDict[category][subCategory]
                if len(errList) != 0:
                    for error in errList:
                        if 'Robot' in subCategory:
                            pdf.add_error('Pression', error)
                        elif 'Sélection' in subCategory:
                            pdf.add_error('Sélection', error)
                        elif 'Embrayage' in subCategory:
                            pdf.add_error('Embrayage', error)
                        elif 'Engagement' in subCategory:
                            pdf.add_error('Engagement', error)
                        else:
                            pdf.add_error('Autre', error)

        if pdf.errPre == 0:
            pdf.add_error('Pression', 'Fonctionnement nominal')
        if pdf.errSel == 0:
            pdf.add_error('Sélection', 'Fonctionnement nominal')
        if pdf.errEmb == 0:
            pdf.add_error('Embrayage', 'Fonctionnement nominal')
        if pdf.errEng == 0:
            pdf.add_error('Engagement', 'Fonctionnement nominal')
        if pdf.errAut == 0:
            pdf.add_error('Autre', 'Fonctionnement nominal')

        self.diagConsole.insert('end', "[Rapport] : Le rapport à été généré.")
        self.diagConsole.insert('end', "[Rapport] : Envoi du mail contenant le rapport...")
        
        validation = pdf.done()

        if validation:
            self.diagConsole.insert('end', "[Rapport] : Le rapport à été envoyé.")
        else:
            self.diagConsole.insert('end', "[Rapport] : Le rapport n'a pas pu être envoyé.")

        self.buttonRelancer.config(state= 'normal')
        self.buttonRetour.config(state= 'normal')
        return
