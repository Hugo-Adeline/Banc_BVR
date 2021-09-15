# -*- coding: utf-8 -*-

from time import sleep, time

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

        # Création des valeurs associées aux capteurs
        if self.category == "Vitesse":
            return {'Min': 0,
                    'Max': 100,
                    'MarginScaling': 100,
                    'Deviation': None,
                    'DeviationErr': None,
                    'ActuatorType': None}
        elif self.category == "Pression":
            return {'Min': 0.5,
                    'Max': 2.5,
                    'MarginScaling': 0.5,
                    'Deviation': None,
                    'DeviationErr': None,
                    'ActuatorType': None}
        return {'Min': 0,
                'Max': 5,
                'MarginScaling': 1,
                'Deviation': None,
                'DeviationErr': None,
                'ActuatorType': None}


    def GetNominalValue(self, sensorData, gear= 0):

        # On retourne la valeur nominale du capteur pour le rapport engagé
        # Utilisé par SimulationWindow qui n'est pas activé dans cette version
        return None


    def Poll(self, averaging= 1):

        # Retourne la valeur du capteur réel
        return float(self.interface.Poll(self.pinType, self.pin, averaging))


    def GetActuatorType(self, robotAttributes):

        # Détermination du type d'actionneur associé au capteur

        # Le capteur de vitesse n'a pas d'actionneur
        if self.category == 'Vitesse':
            return None

        # Le capteur de pression est associé à la pompe
        elif self.category == 'Pression':
            return 'Pompe'

        # Comptage du nombre d'actionneurs associées (1 ou 2)
        try:
            robotAttributes['Actuators']['Electrovanne'][self.subCategoryRoot + ' -']
            actCount = 2
        except:
            actCount = 1

        # Si il y a deux moteurs électriques, alors l'actionneur est linéaire
        if actCount == 1:
            try:
                robotAttributes['Actuators']['Moteur_électrique'][self.subCategoryRoot + ' -']
                return 'Linéaire'
            except:
                actCount = 1

        # Si il n'y a qu'un seul actionneur, il est soit de type Bouton soit S-Cam

        #
        if 'Sélection' in self.subCategory and actCount == 1:
            actUp = self.interface.actuatorClass['Electrovanne']['Sélection +']
            val1 = self.Poll(10)
            sleep(0.5)
            actUp.Set(state= 1)
            sleep(0.5)
            val2 = self.Poll(10)
            sleep(0.5)
            actUp.Set(state= 0)
            sleep(0.5)
            scaling = robotAttributes['Sensors'][self.category][self.subCategory]['MarginScaling']
            margin = robotAttributes['Margin']
            if (val1 <= val2 + margin*scaling) and (val1 >= val2 - margin*scaling):
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
                if (val1 >= val2 + margin*scaling) or (val1 <= val2 - margin*scaling):
                    return 'S-Cam'
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
                if (val1 >= val2 + margin*scaling) or (val1 <= val2 - margin*scaling):
                    return 'S-Cam'
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
        scaling = robotAttributes['Sensors'][self.category][self.subCategory]['MarginScaling']
        margin = robotAttributes['Margin']
        if (valSensor1 <= valSensor2 + margin*scaling) and (valSensor1 >= valSensor2 - margin*scaling):
            return 'Toggle'
        else:
            return 'Linéaire'


    def GetMinMax(self, robotAttributes):
        # On cherche le nombre d'actionneurs associés
        self.interface.GPIOReset()
        if self.category == "Vitesse":
            data = []
            minSensor = self.Poll(10)
            sleep(0.25)
            self.interface.SetMotor(True)
            sleep(0.75)
            maxSensor = self.GetSpeed(250)
            sleep(0.25)
            self.interface.SetMotor(False)
            return minSensor, maxSensor
        actuatorType = robotAttributes['Sensors'][self.category][self.subCategory]['ActuatorType']
        actuatorUp = self.interface.actuatorClass['Electrovanne'][self.subCategoryRoot + ' +']
        if actuatorType == 'S-Cam':
            actuatorBisUp = self.interface.actuatorClass['Electrovanne']['Engagement +']
            actuatorBisDown = self.interface.actuatorClass['Electrovanne']['Engagement -']
            minSensor1 = 0
            minSensor2 = 5
            scaling = robotAttributes['Sensors'][self.category][self.subCategory]['MarginScaling']
            margin = robotAttributes['Margin']
            while (minSensor1 > minSensor2 + margin*scaling) or (minSensor1 < minSensor2 - margin*scaling):
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
            while (maxSensor1 > maxSensor2 + margin*scaling) or (maxSensor1 < maxSensor2 - margin*scaling):
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


    def GetSpeed(self, averaging= 1):
        data = []
        t0 = time()
        status = False
        datacount = 0
        while datacount < averaging + 1:
            if status == False:
                value = self.Poll()
                status = value >= 0.2
                if status == True:
                    freq = 1/(time() - t0)
                    t0 = time()
                    data.append(freq)
                    datacount += 1
            else:
                status = self.Poll() >= 0.2
            if time() - t0 > 0.5:
                t0 = time()
                break
        try:
            data = data[1:]
        except:
            None
        if len(data) == 0:
            frequency = 0
        elif len(data) > 1:
            moy = 0
            for value in data:
                moy += value
                frequency = moy/len(data)
        else:
            frequency = data[0]
        frequency = float(round(frequency, 1))
        return frequency
