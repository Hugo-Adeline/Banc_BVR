# -*- coding: utf-8 -*-

from time import sleep
from numpy import mean
from GUI.GUI_utils import Popup

def AutoCalib(self):

    # On demande de vérifier le branchement des capteurs
    Popup(self, 1, texte= "Assurez vous que tous les capteurs sont branchés avant de continuer.", fermer= 'Continuer')

    # On éteint les relais
    self.root.interface.GPIOReset()

    # Récupération de la déviation des capteurs branchés
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
            if round(variance**(0.5), 2) == 0.0:
                self.robotAttributes['Sensors'][category][subCategory]['Deviation'] = 0.01
            else:
                self.robotAttributes['Sensors'][category][subCategory]['Deviation'] = round(variance**(0.5), 2)

    # Calibration du système de pression
    pressureSensor = self.root.interface.sensorClass['Pression']['Robot']
    pressureActuator = self.root.interface.actuatorClass['Electro_pompe']['Robot']
    evDict = self.robotAttributes['Actuators']['Electrovanne']
    evClassList = []
    for subCategory in evDict:
    	evClassList.append(self.root.interface.actuatorClass['Electrovanne'][subCategory])

    # Vidage de la pression
    for i in range(5):
        for ev in evClassList:
            ev.Set(state= 1)
            sleep(0.5)
            ev.Set(state= 0)
            sleep(0.25)
    # Sauvegarde de la pression minimale
    self.robotAttributes['Sensors']['Pression']['Robot']['Min'] = pressureSensor.Poll(100)
    minPressure = self.robotAttributes['Sensors']['Pression']['Robot']['Min']
    # Détermination de la pression maximale et minimale
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
                devSensor = self.robotAttributes['Sensors']['Position'][actuator.rstrip('-+') + '1']['Deviation']
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
            dev = self.robotAttributes['Sensors']['Pression']['Robot']['Deviation']
            margin = self.root.interface.margin
            while pressureSensor.Poll(100) > minPressure + margin*dev:
                for ev in evClassList:
                    ev.Set(state= 1)
                    sleep(0.5)
                    ev.Set(state= 0)
                    sleep(0.25)
            # Augmentation de la pression max jusqu'à ce que l'actionneur effectue le nombre de va et vient ciblé
            counter = 0
            dev = self.robotAttributes['Sensors']['Position'][actuator.rstrip(' +-') + ' 1']['Deviation']
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
                    if abs(minTest-minSensor) > margin*dev and abs(maxTest-maxSensor) > margin*dev:
                        break
                    counter += 1
                print('counter = ', counter)
                if counter != objective:
                    timer += 1
            # Vidage de la pression
            while pressureSensor.Poll(100) > minPressure + margin*dev:
                for ev in evClassList:
                    ev.Set(state= 1)
                    sleep(0.5)
                    ev.Set(state= 0)
                    sleep(0.25)

    # Récupération du temps que met la pompe pour atteindre la pression max
    self.robotAttributes['Actuators']['Electro_pompe']['Robot']['Time'] = self.root.interface.actuatorClass['Electro_pompe']['Robot'].GetTime(self.robotAttributes)

    pressureActuator.Set(state= 1)
    sleep(1)
    pressureActuator.Set(state= 0)

    # Détermination des min et max capteur position et de leur type
    for subCategory in self.robotAttributes['Sensors']['Position']:
        pressureActuator.Set(state= 1)
        while self.robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(50):
            sleep(0.1)
        pressureActuator.Set(state= 0)
        self.robotAttributes['Sensors']['Position'][subCategory]['ActuatorType'] = self.root.interface.sensorClass['Position'][subCategory].GetActuatorType(self.robotAttributes)
        pressureActuator.Set(state= 1)
        while self.robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(50):
            sleep(0.1)
        pressureActuator.Set(state= 0)
        self.robotAttributes['Sensors']['Position'][subCategory]['Min'], self.robotAttributes['Sensors']['Position'][subCategory]['Max'] = self.root.interface.sensorClass['Position'][subCategory].GetMinMax(self.robotAttributes)

    # Récupération de la déviation des capteurs branchés
    print('début du calcul dev')
    Popup(self, 1, texte= "Veuillez débrancher tous les capteurs et appuyer sur 'Continuer'", fermer= 'Continuer')
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

    # Vidage de la pression
    for i in range(5):
        for ev in evClassList:
            ev.Set(state= 1)
            sleep(0.5)
            ev.Set(state= 0)
            sleep(0.25)

    return True
