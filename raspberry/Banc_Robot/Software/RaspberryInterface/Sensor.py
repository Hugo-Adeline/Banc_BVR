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
                    'Max': 5,
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
        if self.subCategory == 'Sélection 1' and actCount == 1:
            print('test S-shaft')
            actUp = self.interface.actuatorClass['Electrovanne']['Sélection +']
            val1 = self.Poll(10)
            sleep(0.5)
            actUp.Set(state= 1)
            sleep(0.5)
            val2 = self.Poll(10)
            sleep(0.5)
            actUp.Set(state= 0)
            sleep(0.5)
            dev = robotAttributes['Sensors'][self.category][self.subCategory]['Deviation']
            margin = self.interface.margin
            print('val1 = ', val1, ' ; val2= ', val2)
            if (val1 <= val2 + margin*dev) and (val1 >= val2 - margin*dev):
                print('oui test S-Shaft')
                actBisUp = self.interface.actuatorClass['Electrovanne']['Engagement +']
                actBisDown = self.interface.actuatorClass['Electrovanne']['Engagement -']
                actBisDown.Set(state= 1)
                sleep(0.5)
                actBisDown.Set(state= 0)
                sleep(0.5)
                val1 = self.Poll(10)
                sleep(0.5)
                actUp.Set(state= 1)
                sleep(0.5)
                actBisUp.Set(state= 1)
                sleep(0.5)
                val2 = self.Poll(10)
                sleep(0.5)
                actBisUp.Set(state= 0)
                sleep(0.5)
                actUp.Set(state= 0)
                sleep(0.5)
                print('val1 = ', val1, ' ; val2= ', val2)
                if (val1 >= val2 + margin*dev) or (val1 <= val2 - margin*dev):
                    return 'S-Shaft'
                val1 = self.Poll(10)
                sleep(0.5)
                actUp.Set(state= 1)
                sleep(0.5)
                actBisDown.Set(state= 1)
                sleep(0.5)
                val2 = self.Poll(10)
                sleep(0.5)
                actBisDown.Set(state= 0)
                sleep(0.5)
                if (val1 >= val2 + margin*dev) or (val1 <= val2 - margin*dev):
                    return 'S-Shaft'
        if actCount == 1:
            return 'Bouton'
        actUp = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' +']
        if actCount == 2:
            actDown = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' -']
            sleep(0.5)
            actDown.Set(state= 1)
            sleep(0.5)
            actDown.Set(state= 0)
            sleep(0.5)
            valSensor1 = self.Poll(10)
            sleep(0.5)
        actUp.Set(state= 1)
        sleep(0.5)
        actUp.Set(state= 0)
        sleep(0.5)
        valSensor2 = self.Poll(10)
        dev = robotAttributes['Sensors'][self.category][self.subCategory]['Deviation']
        margin = self.interface.margin
        if (valSensor1 <= valSensor2 + margin*dev) and (valSensor1 >= valSensor2 - margin*dev):
            return 'Toggle'
        else:
            return 'Linéaire'


    def GetMinMax(self, robotAttributes):
        # On cherche le nombre d'actionneurs associés
        self.interface.GPIOReset()
        actuatorType = robotAttributes['Sensors'][self.category][self.subCategory]['ActuatorType']
        actuatorUp = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' +']
        if actuatorType == 'S-Shaft':
            actuatorBisUp = self.interface.actuatorClass['Electrovanne']['Engagement +']
            actuatorBisDown = self.interface.actuatorClass['Electrovanne']['Engagement -']
            minSensor1 = 0
            minSensor2 = 5
            dev = robotAttributes['Sensors'][self.category][self.subCategory]['Deviation']
            margin = self.interface.margin
            while (minSensor1 > minSensor2 + margin*dev) or (minSensor1 < minSensor2 - margin*dev):
                minSensor1 = self.Poll(10)
                actuatorBisUp.Set(state= 1)
                sleep(0.3)
                actuatorBisUp.Set(state= 0)
                sleep(0.3)
                actuatorUp.Set(state= 1)
                sleep(0.3)
                actuatorBisDown.Set(state= 1)
                sleep(0.3)
                actuatorBisDown.Set(state= 0)
                sleep(0.3)
                actuatorUp.Set(state= 0)
                sleep(0.3)
                minSensor2 = self.Poll(10)
            minSensor = minSensor2
            pressureSensor = self.interface.sensorClass['Pression']['Robot']
            pressureActuator = self.interface.actuatorClass['Electro_pompe']['Robot']
            pressureActuator.Set(state= 1)
            while robotAttributes['Sensors']['Pression']['Robot']['Max'] > pressureSensor.Poll(10):
                sleep(0.1)
            pressureActuator.Set(state= 0)
            maxSensor1 = 0
            maxSensor2 = 5
            while (maxSensor1 > maxSensor2 + margin*dev) or (maxSensor1 < maxSensor2 - margin*dev):
                maxSensor1 = self.Poll(10)
                actuatorBisDown.Set(state= 1)
                sleep(0.3)
                actuatorBisDown.Set(state= 0)
                sleep(0.3)
                actuatorUp.Set(state= 1)
                sleep(0.3)
                actuatorBisUp.Set(state= 1)
                sleep(0.3)
                actuatorBisUp.Set(state= 0)
                sleep(0.3)
                actuatorUp.Set(state= 0)
                sleep(0.3)
                maxSensor2 = self.Poll(10)
            maxSensor = maxSensor2
            return minSensor, maxSensor
        if actuatorType != 'Bouton' :
            actuatorDown = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' -']
        if actuatorType == 'Bouton' :
            minSensor = self.Poll(10)
        else:
            sleep(0.5)
            actuatorDown.Set(state= 1)
            sleep(0.5)
            if actuatorType == 'Toggle':
                minSensor = self.Poll(10)
            actuatorDown.Set(state= 0)
            sleep(0.5)
            if actuatorType == 'Linéaire':
                minSensor = self.Poll(10)
        actuatorUp.Set(state= 1)
        sleep(0.5)
        if actuatorType == 'Toggle' or actuatorType == 'Bouton':
            maxSensor = self.Poll(10)
        actuatorUp.Set(state= 0)
        sleep(0.5)
        if actuatorType == 'Linéaire':
            maxSensor = self.Poll(10)
        return minSensor, maxSensor
