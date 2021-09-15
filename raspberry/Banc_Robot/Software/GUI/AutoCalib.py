# -*- coding: utf-8 -*-

from time import sleep
from numpy import mean
from GUI.GUI_utils import Popup

def AutoCalib(self):

    # On demande de vérifier le branchement des capteurs
    self.centerFrame.place_forget()
    self.centerSubFrameBis.pack(side= 'top', pady= 100)

    self.diagConsole.delete(0, last= 'end')
            
    self.diagConsole.insert('end', "[AutoCalib] : Initialisation de la calibration automatique pour le robot: " + self.robotAttributes['Name'] + '...')
    self.root.update()

    Popup(self, 1, texte= "Assurez vous que tous les capteurs sont branchés avant de continuer.", fermer= 'Continuer')
    self.root.update()

    # On éteint les relais
    self.root.interface.GPIOReset()

    # Récupération de la déviation des capteurs branchés
    self.diagConsole.insert('end', "[AutoCalib] : Récupération de la déviation nominale des capteurs...")
    self.root.update()

    for category in self.robotAttributes['Sensors']:
        for subCategory in self.robotAttributes['Sensors'][category]:
            tempList = []
            for i in range(1000):
                tempList.append(self.root.interface.sensorClass[category][subCategory].Poll())
            avgVal = mean(tempList)
            variance = 0
            for i in tempList:
                variance += (i - avgVal)**2
            variance = variance / len(tempList)
            if round(variance**(0.5), 2) < 0.01:
                self.robotAttributes['Sensors'][category][subCategory]['Deviation'] = 0.02
            else:
                self.robotAttributes['Sensors'][category][subCategory]['Deviation'] = round(variance**(0.5), 2)

    self.diagConsole.insert('end', "[AutoCalib] : Déviation nominale des capteurs enregistrée.")
    self.diagConsole.itemconfig('end', fg= 'green')
    self.root.update()
    if self.robotAttributes['Type'] != 'Electrique':
        # Calibration du système de pression
        self.diagConsole.insert('end', "[AutoCalib] : Initialisation de la calibration du système de pression...")
        self.root.update()

        pressureSensor = self.root.interface.sensorClass['Pression']['Robot']
        pressureActuator = self.root.interface.actuatorClass['Electro_pompe']['Robot']
        evDict = self.robotAttributes['Actuators']['Electrovanne']
        evClassList = []
        for subCategory in evDict:
        	evClassList.append(self.root.interface.actuatorClass['Electrovanne'][subCategory])

        # Vidage de la pression
        self.diagConsole.insert('end', "[AutoCalib] : Diminution de la pression...")
        self.root.update()

        for i in range(5):
            for ev in evClassList:
                ev.Set(state= 1)
                sleep(0.5)
                ev.Set(state= 0)
                sleep(0.25)

        # Sauvegarde de la pression minimale
        self.robotAttributes['Sensors']['Pression']['Robot']['Min'] = pressureSensor.Poll(100)
        minPressure = self.robotAttributes['Sensors']['Pression']['Robot']['Min']

        self.diagConsole.insert('end', "[AutoCalib] : Pression minimale atteinte à " + str(minPressure) + "V .")
        self.diagConsole.itemconfig('end', fg= 'green')
        self.root.update()

        # Détermination de la pression maximale et minimale
        self.diagConsole.insert('end', "[AutoCalib] : Détermination de la pression maximale...")
        self.root.update()

        timer = 5
        counter = 0
        # Sélection d'un actionneur hydraulique
        for actuator in evDict:
            if '+' in actuator:
                print(actuator)
                positionSensor = self.root.interface.sensorClass['Position'][actuator.rstrip(' +-') + ' 1']
                actuatorUp = self.root.interface.actuatorClass['Electrovanne'][actuator]
                try:
                    actuatorDown = self.root.interface.actuatorClass['Electrovanne'][actuator.rstrip(' +') + ' -']
                except:
                    actuatorDown = self.root.interface.actuatorClass['Electrovanne'][actuator]
                objective = 4
                # Récupération de son min et max
                pressureActuator.Set(state = 1)
                sleep(3)
                pressureActuator.Set(state = 0)
                val1 = positionSensor.Poll(5)
                actuatorDown.Set(state= 1)
                sleep(0.5)
                val2 = positionSensor.Poll(5)
                actuatorDown.Set(state= 0)
                sleep(0.5)
                val3 = positionSensor.Poll(5)
                actuatorUp.Set(state= 1)
                sleep(0.5)
                val4 = positionSensor.Poll(5)
                actuatorUp.Set(state= 0)
                sleep(0.5)
                val5 = positionSensor.Poll(5)
                minSensor = min(val1, val2, val3, val4, val5)
                maxSensor = min(val1, val2, val3, val4, val5)
                # Vidage de la pression
                scaling = self.robotAttributes['Sensors']['Pression']['Robot']['MarginScaling']
                margin = self.robotAttributes['Margin']
                while pressureSensor.Poll(100) > minPressure + margin*scaling:
                    for ev in evClassList:
                        ev.Set(state= 1)
                        sleep(0.5)
                        ev.Set(state= 0)
                        sleep(0.25)
                # Augmentation de la pression max jusqu'à ce que l'actionneur effectue le nombre de va et vient ciblé
                counter = 0
                scalingSensor = self.robotAttributes['Sensors']['Position'][actuator.rstrip(' +-') + ' 1']['MarginScaling']
                while counter < objective:
                    counter = 0
                    pressureActuator.Set(state = 1)
                    sleep(timer)
                    pressureActuator.Set(state = 0)
                    sleep(0.5)
                    self.robotAttributes['Sensors']['Pression']['Robot']['Max'] = pressureSensor.Poll(5)
                    print('new max pressure =', self.robotAttributes['Sensors']['Pression']['Robot']['Max'], 'timer =', timer)
                    while counter < objective:
                        val1 = positionSensor.Poll(5)
                        actuatorDown.Set(state= 1)
                        sleep(0.5)
                        val2 = positionSensor.Poll(5)
                        actuatorDown.Set(state= 0)
                        sleep(0.5)
                        val3 = positionSensor.Poll(5)
                        actuatorUp.Set(state= 1)
                        sleep(0.5)
                        val4 = positionSensor.Poll(5)
                        actuatorUp.Set(state= 0)
                        sleep(0.5)
                        val5 = positionSensor.Poll(5)
                        minTest = min(val1, val2, val3, val4, val5)
                        maxTest = min(val1, val2, val3, val4, val5)
                        if abs(minTest-minSensor) > margin*scalingSensor and abs(maxTest-maxSensor) > margin*scalingSensor:
                            break
                        counter += 1
                    print('counter = ', counter)
                    if counter != objective:
                        timer += 1
                # Vidage de la pression
                while pressureSensor.Poll(100) > minPressure + margin*scaling:
                    for ev in evClassList:
                        ev.Set(state= 1)
                        sleep(0.5)
                        ev.Set(state= 0)
                        sleep(0.25)

        self.diagConsole.insert('end', "[AutoCalib] : Pression maximale atteinte à " + str(self.robotAttributes['Sensors']['Pression']['Robot']['Max']) + "V .")
        self.diagConsole.itemconfig('end', fg= 'green')
        self.root.update()

        # Récupération du temps que met la pompe pour atteindre la pression max
        self.diagConsole.insert('end', "[AutoCalib] : Détermination du temps de monté en pression...")
        self.root.update()

        self.robotAttributes['Actuators']['Electro_pompe']['Robot']['Time'] = self.root.interface.actuatorClass['Electro_pompe']['Robot'].GetTime(self.robotAttributes)

        self.diagConsole.insert('end', "[AutoCalib] : La pompe met " + str(self.robotAttributes['Actuators']['Electro_pompe']['Robot']['Time']) + "sec à monter en pression.")
        self.diagConsole.itemconfig('end', fg= 'green')
        self.root.update()

    # Détermination des min et max capteur position et de leur type
    self.diagConsole.insert('end', "[AutoCalib] : Détermination du min/max des actionneurs et de leur type...")
    self.root.update()
    for subCategory in self.robotAttributes['Sensors']['Position']:
        if self.robotAttributes['Type'] != 'Electrique':
            pressureActuator.Set(state= 1)
            while self.robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(50):
                sleep(0.1)
            pressureActuator.Set(state= 0)
        self.robotAttributes['Sensors']['Position'][subCategory]['ActuatorType'] = self.root.interface.sensorClass['Position'][subCategory].GetActuatorType(self.robotAttributes)
        if self.robotAttributes['Type'] != 'Electrique':
            pressureActuator.Set(state= 1)
            while self.robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(50):
                sleep(0.1)
            pressureActuator.Set(state= 0)
        self.robotAttributes['Sensors']['Position'][subCategory]['Min'], self.robotAttributes['Sensors']['Position'][subCategory]['Max'] = self.root.interface.sensorClass['Position'][subCategory].GetMinMax(self.robotAttributes)

        self.diagConsole.insert('end', "[AutoCalib] : Actionneur de " + str(subCategory) + " (Min: " + str(self.robotAttributes['Sensors']['Position'][subCategory]['Min']) + "V; Max: " + str(self.robotAttributes['Sensors']['Position'][subCategory]['Max']) + "V; Type: " + str(self.robotAttributes['Sensors']['Position'][subCategory]['ActuatorType']) + ").")
        self.diagConsole.itemconfig('end', fg= 'green')
        self.root.update()

    self.robotAttributes['Sensors']['Vitesse']['Boîte de vitesses']['Min'], self.robotAttributes['Sensors']['Vitesse']['Boîte de vitesses']['Max'] = self.root.interface.sensorClass['Vitesse']['Boîte de vitesses'].GetMinMax(self.robotAttributes)

    self.diagConsole.insert('end', "[AutoCalib] : Capteur de vitesse (Repos: " + str(self.robotAttributes['Sensors']['Vitesse']['Boîte de vitesses']['Min']) + "V; Nominal: " + str(self.robotAttributes['Sensors']['Vitesse']['Boîte de vitesses']['Max']) + "Hz).")
    self.diagConsole.itemconfig('end', fg= 'green')
    self.root.update()

    # Récupération de la déviation des capteurs branchés
    self.diagConsole.insert('end', "[AutoCalib] : Récupération de la déviation dégradée des capteurs...")
    self.root.update()

    print('début du calcul dev')
    Popup(self, 1, texte= "Veuillez débrancher tous les capteurs et appuyer sur 'Continuer'", fermer= 'Continuer')
    self.root.update()
    for category in self.robotAttributes['Sensors']:
        for subCategory in self.robotAttributes['Sensors'][category]:
            tempList = []
            for i in range(1000):
                tempList.append(self.root.interface.sensorClass[category][subCategory].Poll())
            avgVal = mean(tempList)
            variance = 0
            for i in tempList:
                variance += (i - avgVal)**2
            variance = variance / len(tempList)
            self.robotAttributes['Sensors'][category][subCategory]['DeviationErr'] = round(variance**(0.5), 2)
    print('fin du calcul dev')

    print(self.robotAttributes)

    self.diagConsole.insert('end', "[AutoCalib] : Déviation dégradée des capteurs enregistrée.")
    self.diagConsole.itemconfig('end', fg= 'green')
    self.root.update()

    # Vidage de la pression
    self.diagConsole.insert('end', "[AutoCalib] : Diminution de la pression...")
    self.root.update()

    for i in range(5):
        for ev in evClassList:
            ev.Set(state= 1)
            sleep(0.5)
            ev.Set(state= 0)
            sleep(0.25)

    self.diagConsole.insert('end', "[AutoCalib] : Fin de la calibration automatique.")
    self.root.update()

    self.centerFrame.place(relx = 0.20, rely= 0.20)
    self.centerSubFrameBis.pack_forget()

    return True
