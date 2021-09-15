# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as font
from GUI.MainMenuWindow import MainMenuWindow
from GUI.MaintenanceWindow import MaintenanceWindow
from GUI.RemoveRobotWindow import RemoveRobotWindow
from GUI.AddRobotWindow import AddRobotWindow
from GUI.CalibrationWindow import CalibrationWindow
from GUI.AutomaticDiagnosisWindow import AutomaticDiagnosisWindow
from GUI.SimulationWindow import SimulationWindow
from GUI.ManualDiagnosisWindow import ManualDiagnosisWindow


class Root(tk.Tk):
    def __init__(self, dB, interface, filepath, configDict):

        # Création de la page racine
        tk.Tk.__init__(self)
        self.dB = dB
        self.interface = interface
        self.filepath = filepath + '/GUI'
        self.configDict = configDict

        # Paramétrage de la page racine
        self.wm_title("Banc d'essais robot")
        icon = tk.PhotoImage(file= self.filepath + "/Images/Icones/BVR.gif")
        self.tk.call('wm', 'iconphoto', self._w, icon)
        self.attributes('-fullscreen',True)
        self.config(bg= '#F0F0F0')

        # Déclaration des paramètres globaux de l'interface
        self.activeFrame = None
        self.retourRelX = 0.25
        self.retourRelY = 0.80
        self.validerRelX = 0.75
        self.validerRelY = 0.80
        self.titlePadY = 10
        self.fontButton = font.Font(size= 14,weight= 'bold')
        self.fontTitle = font.Font(size= 18, weight= 'bold')
        self.fontLabel = font.Font(size= 15)
        self.fontValues = font.Font(size= 25)
        self.fontSensor = font.Font(size= 20)
        self.defaultbg = '#F0F0F0'
        self.lightgrey = '#D3D3D3'
        self.interface.margin = float(configDict["Software_Parameters"]["DefaultMargin"])

        # Création du dictionnaire des chemins des images et du numéro de l'image indiquant la valeur nominale
        self.imageDict = {}
        self.imageDict['Electrovanne'] = {}
        for i in range(11):
            self.imageDict['Electrovanne'][i] = self.filepath + '/Images/Actuator/actuator' + str(i) + '.png'
        self.imageDict['Electrovanne']['ErrLow'] = self.filepath + '/Images/Actuator/actuatorErrLow.png'
        self.imageDict['Electrovanne']['ErrHigh'] = self.filepath + '/Images/Actuator/actuatorErrHigh.png'
        self.imageDict['Electrovanne']['Nominale'] = 10

        self.imageDict['Electro_pompe'] = {}
        for i in range(11):
            self.imageDict['Electro_pompe'][i] = self.filepath + '/Images/Pressure_gauge/pressure_gauge' + str(i) + '.png'
        self.imageDict['Electro_pompe']['ErrLow'] = self.filepath + '/Images/Pressure_gauge/pressure_gaugeErrLow.png'
        self.imageDict['Electro_pompe']['ErrHigh'] = self.filepath + '/Images/Pressure_gauge/pressure_gaugeErrHigh.png'
        self.imageDict['Electro_pompe']['Nominale'] = 6

        self.imageDict['Moteur_électrique'] = {}
        for i in range(11):
            self.imageDict['Moteur_électrique'][i] = self.filepath + '/Images/Electrique_motor/electric_motor' + str(i) + '.png'
        self.imageDict['Moteur_électrique']['ErrLow'] = self.filepath + '/Images/Electrique_motor/electric_motorErrLow.png'
        self.imageDict['Moteur_électrique']['ErrHigh'] = self.filepath + '/Images/Electrique_motor/electric_motorErrHigh.png'
        self.imageDict['Moteur_électrique']['Nominale'] = 10

        self.imageDict['Shifter'] = {}
        for i in range(11):
            self.imageDict['Shifter'][i+2] = self.filepath + '/Images/Shifter/shifter' + str(i+2) + '.png'

        self.imageDict['Warning'] =self.filepath + '/Images/Icones/Warning.gif'

        self.imageDict['SpeedBench'] = {}
        self.imageDict['SpeedBench']['Off'] = self.filepath + '/Images/Speed_bench/speed_benchOff.png'
        self.imageDict['SpeedBench']['TooFar'] = {}
        for i in range(4):
            self.imageDict['SpeedBench']['TooFar'][i] = self.filepath + '/Images/Speed_bench/speed_benchTooFar' + str(i) + '.png'
        self.imageDict['SpeedBench']['TooClose'] = {}
        for i in range(4):
            self.imageDict['SpeedBench']['TooClose'][i] = self.filepath + '/Images/Speed_bench/speed_benchTooClose' + str(i) + '.png'
        self.imageDict['SpeedBench']['Nominal'] = {}
        for i in range(4):
            self.imageDict['SpeedBench']['Nominal'][i] = self.filepath + '/Images/Speed_bench/speed_benchNominal' + str(i) + '.png'

        # Création des différentes fenêtres
        self.mainMenuWindow = MainMenuWindow(self)
        self.maintenanceWindow = MaintenanceWindow(self)
        self.addRobotWindow = AddRobotWindow(self)
        self.removeRobotWindow = RemoveRobotWindow(self)
        self.calibrationWindow = CalibrationWindow(self)
        self.automaticDiagnosisWindow = AutomaticDiagnosisWindow(self)
        #self.simulationWindow = SimulationWindow(self)
        self.manualDiagnosisWindow = ManualDiagnosisWindow(self)

        # Initialisation des différentes fenêtres
        self.mainMenuWindow.Setup()
        self.maintenanceWindow.Setup()
        self.addRobotWindow.Setup()
        self.removeRobotWindow.Setup()
        self.calibrationWindow.Setup()
        self.automaticDiagnosisWindow.Setup()
        #self.simulationWindow.Setup()
        self.manualDiagnosisWindow.Setup()

         # Création de la popup pour la fermeture du système
        self.protocol("WM_DELETE_WINDOW", self.mainMenuWindow.Close)

    def Start(self):

        # Lancement de l'interface et ouverture du menu principal
        self.mainMenuWindow.Open()
        self.mainloop()
