# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as font
from GUI.GUI_utils import SwitchWindow, Popup
from PIL import Image, ImageTk
from functools import partial
from Thread import Thread

class SimulationWindow():
    def __init__(self, root):

        # Définition de la fenêtre Parent
        self.root = root

        # Création de la frame qui contient la page
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)

        # Création des cadres
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)
        self.centerSubFrame = tk.Frame(self.masterFrame, relief= 'ridge', bd= 3, bg= self.root.defaultbg)
        self.sensorFrame = tk.Frame(self.centerSubFrame, relief= 'ridge', bd= 1, bg= self.root.defaultbg)
        self.buttonFrame = tk.Frame(self.centerSubFrame, bg= self.root.defaultbg)
        self.shifterFrame = tk.Frame(self.centerSubFrame, bg= self.root.defaultbg)

        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerSubFrame.pack(expand= 'true')
        self.sensorFrame.pack(side= 'left', fill= 'y')
        self.buttonFrame.pack(side= 'right', pady= 15, padx = 15)
        self.shifterFrame.pack(side= 'left', expand= True, padx = 15)

         # Définition des variables
        self.robotSelected = tk.StringVar()
        self.refreshingThread = None
        self.robotAttributes = None
        self.titre = tk.StringVar()
        self.selectedGearLabel = tk.StringVar()
        self.selectedGearLabel.set('N')
        self.sensorGearLabelList = []
        self.sensorRobotLabelList= []
        self.sensorLabelList = []
        self.sensorLabel = {}
        self.shifterButtonList = []
        self.sensorRobotLabelListVarDict = {}
        self.selectedGear = 0

        # Création des paramètres
        self.shifterButtonFont = font.Font(size= 22, weight= 'bold')
        self.shifterButtonHeight = 1
        self.shifterButtonWidth = 2
        self.fontGearButton = font.Font(size= 40, weight= 'bold')
        self.fontGear = font.Font(size= 40, weight= 'bold')
        self.fontSensorTitle = font.Font(size= 20, weight= 'bold')
        self.fontSensor = font.Font(size= 19, weight= 'bold')


    def Setup(self):

        # Récupération de la robot sélectionnée pour le diagnostic
        self.robotSelected = self.root.mainMenuWindow.robotSelected
        self.titre.set("Diagnostic manuel du robot " + str(self.robotSelected.get()))
        self.robotAttributes = self.root.dB.GetRobotAttributes(self.robotSelected.get())

        # Création des boutons et labels fixes
        self.label = tk.Label(self.titleFrame, textvariable= self.titre)
        self.label.config(font = self.root.fontTitle, bg= self.root.defaultbg)
        self.label.pack(pady = self.root.titlePadY)

        self.label = tk.Label(self.buttonFrame, textvariable= self.selectedGearLabel)
        self.label.config(font = self.fontGear, bg= 'white', borderwidth= 3, relief= "groove", width= 2, height=1)
        self.label.pack()

        self.button = tk.Button(self.buttonFrame, text= "▲", command= self.Upshift)
        self.button.config(font = self.fontGearButton, borderwidth= 3, width= 5, height=3, bg = 'lightgrey')
        self.button.pack()

        self.button = tk.Button(self.buttonFrame, text= "▼", command= self.Downshift)
        self.button.config(font = self.fontGearButton, borderwidth= 3, width= 5, height=3, bg = 'lightgrey')
        self.button.pack()

        self.label = tk.Label(self.sensorFrame, text="Capteur")
        self.label.config(font = self.fontSensorTitle, bg= self.root.defaultbg)
        self.label.grid(column= 1, row= 1, sticky= 'w')

        self.label = tk.Label(self.sensorFrame, text="Robot")
        self.label.config(font = self.fontSensorTitle, bg= self.root.defaultbg)
        self.label.grid(column= 2, row= 1, sticky= 'w')

        self.label = tk.Label(self.sensorFrame, text="Nominal")
        self.label.config(font = self.fontSensorTitle, bg= self.root.defaultbg)
        self.label.grid(column= 3, row= 1, sticky= 'w')

        # Ajout de l'image du levier de vitesse pour le nombre de vitesse du robot
        self.image = Image.open(self.root.imageDict['Shifter'][self.robotAttributes['Gears']])
        self.render = ImageTk.PhotoImage(self.image)
        self.imgLabel = tk.Label(self.shifterFrame, image=self.render, bg= self.root.defaultbg)
        self.imgLabel.grid(column= 0, columnspan= str(self.robotAttributes['Gears']//2+1), row=2)

        # Création des boutons de sélection des vitesses
        self.shifterButtonList.append(tk.Button(self.shifterFrame, text= 'R', command= lambda: self.SelectGear('R')))
        self.shifterButtonList[0].config(font = self.shifterButtonFont, width= self.shifterButtonWidth, height= self.shifterButtonHeight)
        self.shifterButtonList[0].grid(column= 0, row= 1)
        self.shifterButtonList.append(tk.Button(self.shifterFrame, text= 'N', command= lambda: self.SelectGear('N')))
        self.shifterButtonList[1].config(font = self.shifterButtonFont, width= self.shifterButtonWidth, height= self.shifterButtonHeight)
        self.shifterButtonList[1].grid(column= 2, row= 2)

        self.button = tk.Button(self.masterFrame, text= "Retour", command= self.Retour)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= self.root.retourRelX, rely= self.root.retourRelY)


    # Fonction pour ouvrir la fenêtre
    def Open(self):
        SwitchWindow(self.masterFrame,self.root)
        self.Refresh()
        if self.refreshingThread == None:
            self.refreshingThread = Thread('refreshingThread', self.SensorRefresh, 0.5)
            self.refreshingThread.start()


    def Retour(self):
        self.root.interface.GPIOReset()
        self.root.mainMenuWindow.Open()


    # Fonction pour monter un rapport
    def Upshift(self):
        if self.selectedGearLabel.get() == 'R':
            self.selectedGearLabel.set('N')
            self.selectedGear = 0
        elif self.selectedGearLabel.get() == 'N':
            self.selectedGearLabel.set('1')
            self.selectedGear = 1
        elif int(self.selectedGearLabel.get()) < (self.robotAttributes['Gears']-1):
            self.selectedGear += 1
            self.selectedGearLabel.set(self.selectedGear)
        self.Refresh()


    # Fonction pour changer le rapport
    def SelectGear(self, gear):
        if gear == 'R':
            self.selectedGearLabel.set('R')
            self.selectedGear = -1
        elif gear == -1:
            self.selectedGearLabel.set('R')
            self.selectedGear = -1
        elif gear == 'N':
            self.selectedGearLabel.set('N')
            self.selectedGear = 0
        elif gear == 0:
            self.selectedGearLabel.set('N')
            self.selectedGear = 0
        elif gear < (self.robotAttributes['Gears']-1):
            self.selectedGear = gear
            self.selectedGearLabel.set(gear)
        else:
            self.selectedGear = self.robotAttributes['Gears']-1
            self.selectedGearLabel.set(self.robotAttributes['Gears']-1)
        self.Refresh()


    # Fonction pour descendre un rapport
    def Downshift(self):
        if self.selectedGearLabel.get() == 'N':
            self.selectedGearLabel.set('R')
            self.selectedGear = -1
        elif self.selectedGearLabel.get() == '1':
            self.selectedGearLabel.set('N')
            self.selectedGear = 0
        elif self.selectedGearLabel.get() != 'R':
            self.selectedGear -= 1
            self.selectedGearLabel.set(self.selectedGear)
        self.Refresh()


    def Refresh(self):

        # Rafraichissement du robot sélectionné
        self.robotSelected = self.root.mainMenuWindow.robotSelected
        self.titre.set("Diagnostic manuel du robot " + str(self.robotSelected.get()))
        self.robotAttributes = self.root.dB.GetRobotAttributes(self.robotSelected.get())

        # Changement de l'image
        self.image = Image.open(self.root.imageDict['Shifter'][self.robotAttributes['Gears']])
        self.render = ImageTk.PhotoImage(self.image)
        self.imgLabel.config(image= self.render, bg= self.root.defaultbg)
        self.imgLabel.grid(column= 0, columnspan= str(self.robotAttributes['Gears']//2+1), row=2)

        # Suppression des anciens capteurs
        for i in range(len(self.sensorLabelList)):
            self.sensorLabelList[-1].destroy()
            self.sensorLabelList.pop()
            self.sensorRobotLabelList[-1].destroy()
            self.sensorRobotLabelList.pop()
            self.sensorGearLabelList[-1].destroy()
            self.sensorGearLabelList.pop()
        for key in self.sensorRobotLabelListVarDict:
            for subKey in self.sensorRobotLabelListVarDict[key]:
                self.sensorRobotLabelListVarDict[key][subKey].set(None)
            self.sensorRobotLabelListVarDict[key] = {}
        self.sensorRobotLabelListVarDict = {}


        # Création des nouveaux labels
        sensors = self.robotAttributes['Sensors']
        for category in sensors:
            for subCategory in sensors[category]:
                self.sensorLabelList.append(tk.Label(self.sensorFrame, text= category + ' ' + subCategory + ":"))
                self.sensorLabelList[-1].config(font = self.root.fontSensor, bg= self.root.defaultbg)
                self.sensorLabelList[-1].grid(row = i+2, column = 1, sticky= 'w')
                try:
                    self.sensorRobotLabelListVarDict[category][subCategory] = tk.StringVar()
                except:
                    self.sensorRobotLabelListVarDict[category] = {}
                    self.sensorRobotLabelListVarDict[category][subCategory] = tk.StringVar()
                self.sensorRobotLabelListVarDict[category][subCategory].set(0)
                self.sensorRobotLabelList.append(tk.Label(self.sensorFrame, textvariable= self.sensorRobotLabelListVarDict[category][subCategory]))
                self.sensorRobotLabelList[-1].config(font = self.root.fontValues, bg= 'white', borderwidth= 2, relief= "groove", width= 10)
                self.sensorRobotLabelList[-1].grid(row = i+2, column = 2)
                if self.root.interface.sensorClass[category][subCategory].GetNominalValue(sensor) != None:
                    self.sensorGearLabelList.append(tk.Label(self.sensorFrame, text= self.root.interface.sensorClass[category][subCategory].GetNominalValue(sensor, self.selectedGear)))
                    self.sensorGearLabelList[-1].config(font = self.root.fontValues, bg= 'white', borderwidth= 2, relief= "groove", width= 10)
                else:
                    self.sensorGearLabelList.append(tk.Label(self.sensorFrame, text= ''))
                    self.sensorGearLabelList[-1].config(font = self.root.fontValues, borderwidth= 2, relief= "groove", width= 10, bg= self.root.defaultbg)
                self.sensorGearLabelList[-1].grid(row = i+2, column = 3)


        # Destruction des anciens bouttons jusqu'au neutre
        while len(self.shifterButtonList) != 1:
            button = self.shifterButtonList[-1]
            button.destroy()
            self.shifterButtonList.pop()

        # Création du nombre de boutons nécessaires
        for i in range(self.robotAttributes['Gears']):
            gear = i
            if gear == 0:
                button = tk.Button(self.shifterFrame, text= 'N', command= partial(self.SelectGear, 0))
                if self.robotAttributes['Gears'] < 4:
                    button.grid(row= 2, column= 1)
                elif self.robotAttributes['Gears'] < 6:
                    button.grid(row= 2, column= 1, columnspan= 2)
                else:
                    button.grid(row= 2, column= 2)
            else:
                button = tk.Button(self.shifterFrame, text= gear, command= partial(self.SelectGear, gear))
                if gear%2 == 1:
                    button.grid(row= 1, column= (gear+1)//2)
                if gear%2 == 0:
                    button.grid(row= 3, column= (gear+1)//2)
            button.config(font = self.shifterButtonFont, width= self.shifterButtonWidth, height= self.shifterButtonHeight)
            self.shifterButtonList.append(button)

        # Coloration des boutons de sélection du rapport
        for i in range(len(self.shifterButtonList)):
            button = self.shifterButtonList[i]
            if (i-1) == self.selectedGear:
                button.config(bg= 'green')
            else:
                button.config(bg= 'lightgrey')


    def SensorRefresh(self):
        if self.root.activeFrame == self.masterFrame:
            try:
                for key in self.sensorRobotLabelListVarDict:
                    for subKey in self.sensorRobotLabelListVarDict[key]:
                        self.sensorRobotLabelListVarDict[key][subKey].set(self.root.interface.sensorValue[key + ' ' + subKey])
            except:
                None
