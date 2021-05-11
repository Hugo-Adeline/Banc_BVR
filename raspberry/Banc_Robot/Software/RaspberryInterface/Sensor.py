# -*- coding: utf-8 -*-

from time import sleep

class Sensor():
    def __init__(self, category, subCategory, pin, interface):
        # Définition du capteur
        self.category = category
        self.subCategory = subCategory
        self.subCategoryRoot = subCategory.rstrip(' 0123456789')
        self.pinType = pin[0]
        self.pin = pin [1]
        self.interface = interface

    def GetdBValues(self):
        # Création des valeurs associées aux capteur en fonction du type
            return {'Min': 0,
                    'Max': 3.3,
                    'Deviation': None,
                    'DeviationErr': None,
                    'ActuatorType': None}

    def GetNominalValue(self, sensorData, gear= 0):
        # On retourne la valeur nominale du capteur pour le rapport engagé
        return None


    def Poll(self, averaging= 1):
        # On retourneself.interface.marginla valeur du capteur réel
        return float(self.interface.Poll(self.pinType, self.pin, averaging))


    def GetActuatorType(self, robotAttributes):
        print(self.subCategory)
        if self.category == 'Vitesse':
            return None
        if self.category == 'Pression':
            return 'Pompe'
        try:
            robotAttributes['Actuators']['Electrovanne'][self.subCategoryRoot + ' -']
            actCount = 2
        except:
            actCount = 1
        if actCount == 1:
            try:
                robotAttributes['Actuators']['Moteur_électrique'][self.subCategoryRoot + ' -']
                return 'Linéaire'
            except:
                actCount = 1
        if actCount == 1:
            return 'Bouton'
        positionSensor = self.interface.sensorClass[self.category][self.subCategory]
        actUp = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' +']
        actDown = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' -']
        sleep(0.5)
        actDown.Set(state= 1)
        sleep(0.5)
        actDown.Set(state= 0)
        sleep(0.5)
        valSensor1 = positionSensor.Poll(5)
        sleep(0.5)
        actUp.Set(state= 1)
        sleep(0.5)
        actUp.Set(state= 0)
        sleep(0.5)
        valSensor2 = positionSensor.Poll(5)
        dev = robotAttributes['Sensors'][self.category][self.subCategory]['Deviation']
        if (valSensor1 <= valSensor2 + self.interface.margin*dev) and (valSensor1 >= valSensor2 - self.interface.margin*dev):
            return 'Toggle'
        else:
            return 'Linéaire'


    def GetMinMax(self, robotAttributes):
        # On cherche le nombre d'actionneurs associés
        self.interface.GPIOReset()
        actuatorType = robotAttributes['Sensors'][self.category][self.subCategory]['ActuatorType']
        actuatorUp = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' +']
        if actuatorType != 'Bouton' :
            actuatorDown = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' -']
        positionSensor = self.interface.sensorClass[self.category][self.subCategory]
        if actuatorType == 'Bouton' :
            minSensor = positionSensor.Poll(5)
        else:
            sleep(0.5)
            actuatorDown.Set(state= 1)
            sleep(0.5)
            if actuatorType == 'Toggle':
                minSensor = positionSensor.Poll(5)
            actuatorDown.Set(state= 0)
            sleep(0.5)
            if actuatorType == 'Linéaire':
                minSensor = positionSensor.Poll(5)
        actuatorUp.Set(state= 1)
        sleep(0.5)
        if actuatorType == 'Toggle' or actuatorType == 'Bouton':
            maxSensor = positionSensor.Poll(5)
        actuatorUp.Set(state= 0)
        sleep(0.5)
        if actuatorType == 'Linéaire':
            maxSensor = positionSensor.Poll(5)
        return minSensor, maxSensor
