# -*- coding: utf-8 -*-

from time import time

class Actuator():
    def __init__(self, category, subCategory, pin, interface):
        
        # Définition du capteur
        self.category = category
        self.subCategory = subCategory
        self.pinType = pin[0]
        self.pin = pin [1]
        self.interface = interface
        self.position = 0
        
    def GetdBValues(self, numberOfGear= 2):
        
        # Création des valeurs associées aux capteur en fonction du type
        return {'Time': None}
    
    
    def GetOverrideData(self):
        
        # Création des flèches de direction pour les buttons de contrôle
        if '+' in self.subCategory:
            column = 5
            text ='▶'
        elif '-' in self.subCategory:
            column = 3
            text ='◀'
        elif self.category == 'Electro_pompe':
            column = 5
            text ='▲'
        else:
            return None
            
        return column, text

    def Set(self, time= 0.5, state= None):
        # On envoie un signal à l'actionneur
        if state != None:
            return self.interface.Set(self.pin, state)
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
        else:
            return self.interface.SetTime(self.pin, time)
            
    def GetTime(self, robotAttributes):
        if self.category != "Electro_pompe":
            return None
        pressureSensor = self.interface.sensorClass['Pression']['Robot']
        target = robotAttributes['Sensors']['Pression']['Robot']['Max']
        t0 = time()
        self.Set(state= 1)
        while pressureSensor.Poll() < target:
            None
        t1 = time()
        self.Set(state= 0)
        return round(t1 - t0, 1)
            
        
