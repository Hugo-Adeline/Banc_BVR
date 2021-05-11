# -*- coding: utf-8 -*-

from RaspberryInterface.Sensor import Sensor
from RaspberryInterface.Actuator import Actuator
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import _thread
from time import sleep

class RaspberryInterface():
    def __init__(self):
        # Initialisation de l'interface
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        SPI_PORT = 0
        SPI_DEVICE = 0
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

        # Définition des paramètres
        self.margin = 5

        # Création des dictionnaires des types et sous types de capteurs et actionneurs
        self.sensorDict = {"Position": ["Sélection 1", "Sélection 2", "Engagement 1", "Engagement 2", "Embrayage 1", "Embrayage 2"],
                           "Pression": ["Robot"],
                           "Vitesse": ["Boîte de vitesses"]}

        self.actuatorDict = {"Electrovanne": ["Sélection +", "Sélection -", "Engagement +", "Engagement -", "Embrayage +"],
                             "Moteur_électrique": ["Sélection +", "Sélection -", "Engagement +", "Engagement -", "Embrayage +"],
                             "Electro_pompe": ["Robot"],
                             "Extra": ["Extra 1", "Extra 2"]}

        self.pinDict = {"Position Sélection 1": ('A', 0), "Position Sélection 2": ('A', 1),
                        "Position Engagement 1": ('A', 2), "Position Engagement 2": ('A', 3),
                        "Position Embrayage 1": ('A', 4), "Position Embrayage 2": ('A', 5),
                        "Pression Robot": ('A', 6),
                        "Vitesse Boîte de vitesses": ('A', 7),
                        "Electrovanne Sélection +": ('D', 13), "Electrovanne Sélection -": ('D', 14),
                        "Electrovanne Engagement +": ('D', 21), "Electrovanne Engagement -": ('D', 22),
                        "Electrovanne Embrayage +": ('D', 15),
                        "Moteur_électrique Sélection +": ('D', 13), "Moteur_électrique Sélection -": ('D', 14),
                        "Moteur_électrique Engagement +": ('D', 21), "Moteur_électrique Engagement -": ('D', 22),
                        "Moteur_électrique Embrayage +": ('D', 15),
                        "Electro_pompe Robot": ('D', 16),
                        "Extra Extra 1": ('D', 26), "Extra Extra 2": ('D', 27)}

        self.GPIOReset()

        # Création de la liste des types
        self.sensorList = []
        for key in self.sensorDict:
            self.sensorList.append(key)
        self.actuatorList = []
        for key in self.actuatorDict:
            self.actuatorList.append(key)

        # Création du dictionnaire des classes de capteurs
        self.sensorClass = {}
        for category in self.sensorDict:
            self.sensorClass[category] = {}
            for subCategory in self.sensorDict[category]:
                self.sensorClass[category][subCategory] = Sensor(category, subCategory, self.pinDict[category+" "+subCategory], self)
        self.actuatorClass = {}
        for category in self.actuatorDict:
            self.actuatorClass[category] = {}
            for subCategory in self.actuatorDict[category]:
                self.actuatorClass[category][subCategory] = Actuator(category, subCategory, self.pinDict[category+" "+subCategory], self)

        # Création du dictionnaire de valeurs capteur
        self.sensorValue= {}
        for category in self.sensorDict:
            for subCategory in self.sensorDict[category]:
                self.sensorValue[category + ' ' + subCategory] = 0

        _thread.start_new_thread(self.SensorThread, ())


    def GPIOReset(self):
        for key in self.pinDict:
            if self.pinDict[key][0] == 'D':
                GPIO.setup(self.pinDict[key][1], GPIO.OUT)
                self.Set(self.pinDict[key][1], GPIO.LOW)


    def SensorThread(self):
        while True:
            for category in self.sensorClass:
                for subCategory in self.sensorClass[category]:
                    self.sensorValue[category + ' ' + subCategory] = self.sensorClass[category][subCategory].Poll()


    def Poll(self, pinType, pin, averaging):
        if pinType == 'A':
            value = 0
            for i in range(averaging):
                value += self.mcp.read_adc(pin)
            value = str(round(value / 1024 * 3.3 / averaging, 2))
        elif pinType == 'D':
            value = 0
        return value


    def Set(self, pin, value):
        if value == 0:
            value = GPIO.LOW
        elif value == 1:
            value = GPIO.HIGH
        else:
            return
        GPIO.output(pin, value)

    def SetTime(self, pin, time):
        _thread.start_new_thread(self._SetTime, (pin, time))


    def SetTarget(self, actuatorPin, sensorPin, sensorPinType, target):
        _thread.start_new_thread(self._SetTarget, (actuatorPin, sensorPin, sensorPinType, target))


    def _SetTime(self, actuatorPin, time):
        GPIO.output(actuatorPin, GPIO.HIGH)
        sleep(time)
        GPIO.output(actuatorPin, GPIO.LOW)


    def _SetTarget(self, actuatorPinUp, actuatorPinDown, sensorPin, sensorPinType, target):
        if self.mcp.read_adc(sensorPin) < target:
            GPIO.output(actuatorPinUp, GPIO.HIGH)
            while self.mcp.read_adc(sensorPin) < target:
                None
            GPIO.output(actuatorPinUp, GPIO.LOW)
        if self.mcp.read_adc(sensorPin) < target:
            GPIO.output(actuatorPinDown, GPIO.HIGH)
            while self.mcp.read_adc(sensorPin) < target:
                None
            GPIO.output(actuatorPinDown, GPIO.LOW)
