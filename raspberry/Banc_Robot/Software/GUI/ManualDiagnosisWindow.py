# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as font
from math import trunc
from GUI.GUI_utils import SwitchWindow, Popup
from PIL import Image, ImageTk
from Thread import Thread
from GUI.AutoDiag_utils import LowerPressure


class ManualDiagnosisWindow():
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
        self.motorState = False

        # Paramètres
        self.fontTitleSensor = font.Font(size= 20, weight= 'bold')
        self.fontSensor = font.Font(size= 19, weight= 'bold')


    def Setup(self):

        # Création des boutons et labels fixes
        label = tk.Label(self.titleFrame, textvariable= self.titre, bg= self.root.defaultbg)
        label.config(font = self.root.fontTitle)
        label.pack(pady = self.root.titlePadY)

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
        self.titre.set("Diagnostic manuel du robot " + str(self.robotSelected.get()))
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
                key = category + ' ' + subCategory.rstrip(' 0123456789')
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
                #DEBUT AJOUT
                if 'Vitesse' in key:
                    self.motorButton = tk.Button(self.centerFrame, text= '▶', command= self.SetMotor)
                    self.motorButton.config(width = 6, height = 3, bg= 'lightgrey', activebackground= self.root.defaultbg)
                    self.motorButton.grid(column= 3, row= rowCount)
                    imageSpeed = Image.open(self.root.imageDict['SpeedBench']['Off'])
                    self.animatedLabelDict[key] = {}
                    self.animatedLabelDict[key]['subType'] = "Boîte de vitesses"
                    self.animatedLabelDict[key]['PrevState'] = "Off"
                    self.animatedLabelDict[key]['ImageNumber'] = 0
                    self.animatedLabelDict[key]['Filepath'] = self.root.imageDict['SpeedBench']
                    self.animatedLabelDict[key]['Image'] = ImageTk.PhotoImage(imageSpeed)
                    self.animatedLabelDict[key]['Label'] = tk.Label(self.centerFrame, image=self.animatedLabelDict[key]['Image'])
                    self.animatedLabelDict[key]['Row'] = rowCount
                    self.animatedLabelDict[key]['Rowspan'] = 1
                    self.animatedLabelDict[key]['Label'].grid(column= 4, row= self.animatedLabelDict[key]['Row'], rowspan= self.animatedLabelDict[key]['Rowspan'], sticky= 'w')
                if 'Pression' in key:
                    self.pressureButton = tk.Button(self.centerFrame, text= '▼', command= self.LowerPressure)
                    self.pressureButton.config(width = 6, height = 3, bg= 'lightgrey', activebackground= self.root.defaultbg)
                    self.pressureButton.grid(column= 5, row= rowCount)
                #FIN AJOUT
                rowCount += 1
            for category in self.robotAttributes['Actuators']:
                for subCategory in self.robotAttributes['Actuators'][category]:
                    subType = subCategory.rstrip(' +-')
                    if subType in key:
                        if self.root.interface.actuatorClass[category][subCategory].GetOverrideData() != None:
                            column, text = self.root.interface.actuatorClass[category][subCategory].GetOverrideData()
                            try:
                                sensor = self.robotAttributes['Sensors']['Position'][subCategory.rstrip('+-') + '1']
                                if sensor['ActuatorType'] == 'S-Cam':
                                    sCat= category
                                    sSubCat = subCategory
                                    self.actuatorButtonDict[category + ' ' + subCategory] = tk.Button(self.centerFrame, text= text, command= lambda : self.root.interface.actuatorClass[sCat][sSubCat].Set(actuatorType= 'S-Cam'))
                                else:
                                    self.actuatorButtonDict[category + ' ' + subCategory] = tk.Button(self.centerFrame, text= text, command= self.root.interface.actuatorClass[category][subCategory].Set)
                            except:
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
                            self.animatedLabelDict[category + ' ' + subType]['Label'].grid(column= 4, row= self.animatedLabelDict[category + ' ' + subType]['Row'], rowspan= self.animatedLabelDict[category + ' ' + subType]['Rowspan'], sticky= 'w')
                        except:
                            None

        # Rafraichissement des valeurs min max capteurs
        for category in self.robotAttributes['Sensors']:
            for subCategory in self.robotAttributes['Sensors'][category]:
                sensor = self.robotAttributes['Sensors'][category][subCategory]
                self.sensorMinMaxDict[category + ' ' + subCategory] = (sensor['Min'], sensor['Max'])

        #Remise à zéro du moteur
        self.motorState = False
        self.root.interface.SetMotor(self.motorState)

    def SetAnimationPos(self, label, pos, key):
        key = key.rstrip(" 0123456789")
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
            for labelSensor in self.sensorLabelDict[key]:
                labelSensor[1].config(fg = 'red')
        elif pos < 0:
            imageActuator = Image.open(label['Filepath']["ErrLow"])
            for labelSensor in self.sensorLabelDict[key]:
                labelSensor[1].config(fg = 'red')
        else:
            imageActuator = Image.open(label['Filepath'][pos])
            for labelSensor in self.sensorLabelDict[key]:
                labelSensor[1].config(fg = 'black')
        label['Image'] = ImageTk.PhotoImage(imageActuator)
        label['Label'].config(image= label['Image'], bg= self.root.defaultbg)
        label['Label'].grid(column= 4, row= label['Row'], rowspan= label['Rowspan'], sticky= 'w')


    def SensorRefresh(self):

        # Vérification que le menu de diagnostique manuel est en cours d'utilisation
        if self.root.activeFrame == self.masterFrame:
            # L'ensemble est enclavé dans un try / except car il peut y avoir des erreurs non fatales qui stoppent l'affichage des animations (à enlever pour débugger)
            try:
                # Mise à jour des labels avec les valeurs capteur avec les valeurs de sensorValue qui sont mises à jour grâce au thread de RaspberryInterface
                for key in self.sensorLabelVarDict:
                    self.sensorLabelVarDict[key].set(self.root.interface.sensorValue[key])

                # Rafraichissement des labels animés et coloration en rouge des valeurs capteurs si besoin
                for key in self.animatedLabelDict:
                    sensorType = self.animatedLabelDict[key]['subType']
                    for key2 in self.sensorLabelVarDict:
                        if sensorType in key2:
                            value = float(self.sensorLabelVarDict[key2].get())
                            break
                    minValue, maxValue = self.sensorMinMaxDict[key2]
                    minValue = float(minValue)
                    maxValue = float(maxValue)
                    if 'Vitesse' in key:
                        if self.motorState:
                            self.animatedLabelDict[key]['ImageNumber'] +=1
                            if self.animatedLabelDict[key]['ImageNumber'] == 4:
                                self.animatedLabelDict[key]['ImageNumber'] = 0
                            if value < maxValue - 10:
                                imageSpeed = Image.open(self.animatedLabelDict[key]['Filepath']["TooFar"][self.animatedLabelDict[key]['ImageNumber']])
                                self.sensorLabelDict[key2][0][1].config(fg= 'red')
                                self.animatedLabelDict[key]['PrevState'] = "TooFar"
                            elif value > maxValue + 10:
                                imageSpeed = Image.open(self.animatedLabelDict[key]['Filepath']["TooClose"][self.animatedLabelDict[key]['ImageNumber']])
                                self.sensorLabelDict[key2][0][1].config(fg= 'red')
                                self.animatedLabelDict[key]['PrevState'] = "TooClose"
                            else:
                                imageSpeed = Image.open(self.animatedLabelDict[key]['Filepath']["Nominal"][self.animatedLabelDict[key]['ImageNumber']])
                                self.sensorLabelDict[key2][0][1].config(fg= 'black')
                            self.animatedLabelDict[key]['PrevState'] = "Nominal"
                            self.animatedLabelDict[key]['Image'] = ImageTk.PhotoImage(imageSpeed)
                            self.animatedLabelDict[key]['Label'].config(image= self.animatedLabelDict[key]['Image'], bg= self.root.defaultbg)
                            self.animatedLabelDict[key]['Label'].grid(column= 4, row= self.animatedLabelDict[key]['Row'], rowspan= self.animatedLabelDict[key]['Rowspan'], sticky= 'w')
                        elif self.animatedLabelDict[key]['PrevState'] != "Off":
                            imageSpeed = Image.open(self.animatedLabelDict[key]['Filepath']["Off"])
                            self.sensorLabelDict[key2][0][1].config(fg= 'black')
                            self.animatedLabelDict[key]['Image'] = ImageTk.PhotoImage(imageSpeed)
                            self.animatedLabelDict[key]['Label'].config(image= self.animatedLabelDict[key]['Image'], bg= self.root.defaultbg)
                            self.animatedLabelDict[key]['Label'].grid(column= 4, row= self.animatedLabelDict[key]['Row'], rowspan= self.animatedLabelDict[key]['Rowspan'], sticky= 'w')
                            self.animatedLabelDict[key]['PrevState'] = "Off"
                    else:
                        if (maxValue - minValue) == 0:
                            normValue = 0
                        else:
                            normValue = (value - minValue)/(maxValue - minValue)
                        self.SetAnimationPos(self.animatedLabelDict[key], normValue, key2)



                # Actualisation de la couleur des boutons (vert activé, gris désactivé)
                for category in self.robotAttributes['Actuators']:
                    for subCategory in self.robotAttributes['Actuators'][category]:
                        if self.root.interface.actuatorClass[category][subCategory].position == 1:
                            self.actuatorButtonDict[category + ' ' + subCategory].config(bg= 'green', activebackground= 'lightgreen')
                        else:
                            self.actuatorButtonDict[category + ' ' + subCategory].config(bg= 'lightgrey', activebackground= self.root.defaultbg)
            except:
                None


    def SetMotor(self):
        if self.motorState:
            self.motorState = False
            self.motorButton.config(bg= 'lightgrey', activebackground= self.root.defaultbg, text= '▶')
        else:
            self.motorState = True
            self.motorButton.config(bg= 'green', activebackground= 'lightgreen', text= '❚❚')
        self.root.interface.SetMotor(self.motorState)

    def LowerPressure(self):
        self.pressureButton.config(bg= 'green', activebackground= 'lightgreen', state= 'disabled')
        self.root.update()
        LowerPressure(self, True)
        self.pressureButton.config(bg= 'lightgrey', activebackground= self.root.defaultbg, state= 'normal')
