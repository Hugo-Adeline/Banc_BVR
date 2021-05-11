# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as font
from math import trunc
from GUI.GUI_utils import SwitchWindow, Popup
from PIL import Image, ImageTk
from Thread import Thread

class OverrideWindow():
    def __init__(self, root):

        # Définition de la fenêtre Parent
        self.root = root

        # Création de la frame qui contient la page
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)

        # Création des cadres
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)
        self.centerFrame = tk.Frame(self.masterFrame, relief= 'groove', bd= 3, bg= self.root.defaultbg)

        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerFrame.pack(side= 'top', pady= 115)

        # Déclaration des variables
        self.titre = tk.StringVar()
        self.robotSelected = tk.StringVar()
        self.activationTime = 0.5
        self.robotAttributes = None
        self.refreshingThread = None
        self.sensorMinMaxDict = {}
        self.actuatorButtonDict = {}
        self.animatedLabelDict = {}
        self.sensorLabelDict = {}
        self.sensorLabelVarDict = {}

        # Paramètres
        self.fontTitleSensor = font.Font(size= 20, weight= 'bold')
        self.fontSensor = font.Font(size= 19, weight= 'bold')


    def Setup(self):

        # Création des boutons et labels fixes
        label = tk.Label(self.titleFrame, textvariable= self.titre, bg= self.root.defaultbg)
        label.config(font = self.root.fontTitle)
        label.pack(pady = self.root.titlePadY)

        button = tk.Button(self.masterFrame, text= "TEST", command= self.TEST)
        button.config(font = self.root.fontButton)
        button.place(relx= 0.5, rely= self.root.retourRelY)

        button = tk.Button(self.masterFrame, text= "Retour", command= self.Close)
        button.config(font = self.root.fontButton)
        button.place(relx= self.root.retourRelX, rely= self.root.retourRelY)


    def Open(self):
        #retour = Popup(self, 2, texte= "ATTENTION: Ce menu est reservé au personnel habilité", valider= "Continuer", fermer= "Retour")
        #if retour == False:
        #    return
        SwitchWindow(self.masterFrame,self.root)
        self.Refresh()
        if self.refreshingThread == None:
            self.refreshingThread = Thread('refreshingThread', self.SensorRefresh, 0.1)
            self.refreshingThread.start()


    def Close(self):
        self.root.interface.GPIOReset()
        self.root.mainMenuWindow.Open()


    def Refresh(self):

        # Rafraichissement du robot sélectionné
        self.robotSelected = self.root.mainMenuWindow.robotSelected
        self.titre.set("Diagnostique manuel avancé du robot " + str(self.robotSelected.get()))
        self.robotAttributes = self.root.dB.GetRobotAttributes(self.robotSelected.get())

        # Destruction de l'ancienne interface
        self.centerFrame.destroy()
        for key in self.sensorLabelDict:
            for i in range(len(self.sensorLabelDict[key])):
                j = len(self.sensorLabelDict[key])-1-i
                self.sensorLabelDict[key][j][0].destroy()
                self.sensorLabelDict[key][j][1].destroy()
                self.sensorLabelDict[key].pop()
        self.sensorLabelDict = {}
        for key in self.sensorLabelVarDict:
            self.sensorLabelVarDict[key].set(None)
        self.sensorLabelVarDict = {}
        for key in self.actuatorButtonDict:
            self.actuatorButtonDict[key].destroy()
        self.actuatorButtonDict = {}
        for key in self.animatedLabelDict:
            self.animatedLabelDict[key]['Label'].destroy()
        self.animatedLabelDict = {}

        # Création d'un nouveau cadre
        self.centerFrame = tk.Frame(self.masterFrame, relief= 'groove', bd= 3, bg= self.root.defaultbg)
        self.centerFrame.pack(side= 'top', pady= 115)

        # Création des nouveaux labels
        label = tk.Label(self.centerFrame, text="Capteur", bg= self.root.defaultbg)
        label.config(font = self.fontTitleSensor)
        label.grid(column= 1, row= 0)

        label = tk.Label(self.centerFrame, text="Actionneur", bg= self.root.defaultbg)
        label.config(font = self.fontTitleSensor, width= 13)
        label.grid(column= 4, row= 0)

        for category in self.robotAttributes['Sensors']:
            for subCategory in self.robotAttributes['Sensors'][category]:
                key = category + subCategory.rstrip(' 0123456789')
                try:
                    type(self.sensorLabelDict[key]) == list()
                except:
                    self.sensorLabelDict[key] = []
                self.sensorLabelVarDict[category + ' ' + subCategory] = tk.StringVar()
                self.sensorLabelVarDict[category + ' ' + subCategory].set(0)
                self.sensorLabelDict[key].append((tk.Label(self.centerFrame, text= category + ' ' + subCategory + ':', bg= self.root.defaultbg),
                                                       tk.Label(self.centerFrame, textvariable= self.sensorLabelVarDict[category + ' ' + subCategory], bg= self.root.defaultbg)))
                self.sensorLabelDict[key][-1][0].config(font= self.root.fontSensor)
                self.sensorLabelDict[key][-1][1].config(font = self.root.fontValues, borderwidth= 2, bg= 'white', relief= "groove", width= 10)

        rowCount = 1
        for key in self.sensorLabelDict:
            rowActuator = rowCount
            for widgets in self.sensorLabelDict[key]:
                if (widgets == self.sensorLabelDict[key][0]) and (len(self.sensorLabelDict[key]) > 1):
                    widgets[0].grid(column= 1, row= rowCount, sticky= 'sw')
                    widgets[1].grid(column= 2, row= rowCount, sticky= 's')
                elif (widgets == self.sensorLabelDict[key][-1]) and (len(self.sensorLabelDict[key]) > 1):
                    widgets[0].grid(column= 1, row= rowCount, sticky= 'nw')
                    widgets[1].grid(column= 2, row= rowCount, sticky= 'n')
                else:
                    widgets[0].grid(column= 1, row= rowCount, sticky= 'w')
                    widgets[1].grid(column= 2, row= rowCount)
                rowCount += 1
            for category in self.robotAttributes['Actuators']:
                for subCategory in self.robotAttributes['Actuators'][category]:
                    subType = subCategory.rstrip(' +-')
                    if subType in key:
                        if self.root.interface.actuatorClass[category][subCategory].GetOverrideData() != None:
                            column, text = self.root.interface.actuatorClass[category][subCategory].GetOverrideData()
                            self.actuatorButtonDict[category + ' ' + subCategory] = tk.Button(self.centerFrame, text= text, command= self.root.interface.actuatorClass[category][subCategory].Set)
                            self.actuatorButtonDict[category + ' ' + subCategory].config(width = 6, height = 3, bg= 'lightgrey')
                            self.actuatorButtonDict[category + ' ' + subCategory].grid(column= column, row = rowActuator, rowspan= len(self.sensorLabelDict[key]))

                        try:
                            imageActuator = Image.open(self.root.imageDict[category][0])
                            self.animatedLabelDict[category + ' ' + subType] = {}
                            self.animatedLabelDict[category + ' ' + subType]['subType'] = subType
                            self.animatedLabelDict[category + ' ' + subType]['ImageNumber'] = None
                            self.animatedLabelDict[category + ' ' + subType]['Filepath'] = self.root.imageDict[category]
                            self.animatedLabelDict[category + ' ' + subType]['Image'] = ImageTk.PhotoImage(imageActuator)
                            self.animatedLabelDict[category + ' ' + subType]['Label'] = tk.Label(self.centerFrame, image=self.animatedLabelDict[category + ' ' + subType]['Image'])
                            self.animatedLabelDict[category + ' ' + subType]['Row'] = rowActuator
                            self.animatedLabelDict[category + ' ' + subType]['Rowspan'] = len(self.sensorLabelDict[key])
                            self.animatedLabelDict[category + ' ' + subType]['Label'].grid(column= 4, row= self.animatedLabelDict[category + ' ' + subType]['Row'], rowspan= self.animatedLabelDict[category + subType]['Rowspan'], sticky= 'w')
                        except:
                            None

        # Rafraichissement des valeurs min max capteurs
        for category in self.robotAttributes['Sensors']:
            for subCategory in self.robotAttributes['Sensors'][category]:
                sensor = self.robotAttributes['Sensors'][category][subCategory]
                self.sensorMinMaxDict[category + ' ' + subCategory] = (sensor['Min'], sensor['Max'])


    def SetAnimationPos(self, label, pos):
        pos = pos * label['Filepath']['Nominale']
        pos = trunc(pos)
        if label['ImageNumber'] != None:
            if label['ImageNumber'] == pos:
                return
            elif label['ImageNumber'] > 10 and pos > 10:
                return
            elif label['ImageNumber'] < 0 and pos < 0:
                return
        label['ImageNumber'] = pos
        if pos > 10:
            imageActuator = Image.open(label['Filepath']["ErrHigh"])
        elif pos < 0:
            imageActuator = Image.open(label['Filepath']["ErrLow"])
        else:
            imageActuator = Image.open(label['Filepath'][pos])
        label['Image'] = ImageTk.PhotoImage(imageActuator)
        label['Label'].config(image= label['Image'], bg= self.root.defaultbg)
        label['Label'].grid(column= 4, row= label['Row'], rowspan= label['Rowspan'], sticky= 'w')


    def SensorRefresh(self):
        if self.root.activeFrame == self.masterFrame:
            try:
                for key in self.sensorLabelVarDict:
                    self.sensorLabelVarDict[key].set(self.root.interface.sensorValue[key])

                # Rafraichissement des labels animés
                for key in self.animatedLabelDict:
                    sensorType = self.animatedLabelDict[key]['subType']
                    for key2 in self.sensorLabelVarDict:
                        if sensorType in key2:
                            value = float(self.sensorLabelVarDict[key2].get())
                            break
                    minValue, maxValue = self.sensorMinMaxDict[key2]
                    minValue = float(minValue)
                    maxValue = float(maxValue)
                    if (maxValue - minValue) == 0:
                        normValue = 0
                    else:
                        normValue = (value - minValue)/(maxValue - minValue)
                    self.SetAnimationPos(self.animatedLabelDict[key], normValue)
            except:
                None
