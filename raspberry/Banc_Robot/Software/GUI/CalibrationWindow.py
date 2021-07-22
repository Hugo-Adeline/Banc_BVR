# -*- coding: utf-8 -*-

import tkinter as tk
from GUI.GUI_utils import SwitchWindow, Popup
from GUI.AutoCalib import AutoCalib

class CalibrationWindow():
    def __init__(self, root):

        # Définition de la fenêtre Parent
        self.root = root

        # Création de la frame qui contient la page
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)

        # Déclaration des variables
        self.title = tk.StringVar()
        self.robotSelected = tk.StringVar()
        self.robotAttributes = {}
        self.sensorDict = {}
        self.actuatorDict = {}
        self.sensorLabelList = []
        self.actuatorLabelList = []
        self.sensorEntryList = []
        self.actuatorEntryList = []
        self.sensorEntryVarList = []
        self.actuatorEntryVarList = []
        self.nameRobot = tk.StringVar()
        self.gearsRobot = tk.StringVar()
        self.typeRobot = tk.StringVar()

        # Création des cadres
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)
        self.centerFrame = tk.Frame(self.masterFrame, relief= 'groove', bd = 3, bg= self.root.defaultbg)
        self.centerCanvas = tk.Canvas(self.centerFrame, bg= self.root.defaultbg)
        self.centerSubFrame = tk.Frame(self.centerCanvas, bg= self.root.defaultbg)
        self.centerSubFrameBis = tk.Frame(self.masterFrame, relief= 'groove', bd= 1, bg= 'white')

        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerFrame.place(relx = 0.20, rely= 0.20)
        self.centerCanvas.pack(side= 'left')
        self.centerSubFrame.pack()

        # Création de la barre de défilement
        self.centerFrameScrollbar = tk.Scrollbar(self.centerFrame,orient="vertical",command= self.centerCanvas.yview)
        self.centerCanvas.configure(yscrollcommand= self.centerFrameScrollbar.set)
        self.centerFrameScrollbar.pack(side="right",fill="y")
        self.centerCanvas.create_window((0,0), window= self.centerSubFrame, anchor='nw')
        self.centerSubFrame.bind("<Configure>",self._resizeCanvas)

        # Création de la fonction de validation pour les champs textuels
        self.vcmdFloat = self.root.register(self._validateEntryFloat)


    def Setup(self):

        # Récupération de la robot sélectionnée dans le menu déroulant sur la page de maintenance
        self.robotSelected = self.root.maintenanceWindow.robotSelected
        self.robotAttributes = self.root.dB.GetRobotAttributes(self.robotSelected.get())

        # Initialisation des variables des champs de texte
        self.nameRobot.set(self.robotAttributes['Name'])
        self.gearsRobot.set(self.robotAttributes['Gears'])
        self.typeRobot.set(self.robotAttributes['Type'])

        # Création des boutons et labels fixes
        self.title.set("Calibration du robot: "+self.robotSelected.get())
        self.label = tk.Label(self.titleFrame, textvariable= self.title)
        self.label.config(font = self.root.fontTitle, bg= self.root.defaultbg)
        self.label.pack(pady = self.root.titlePadY)

        self.label = tk.Label(self.centerSubFrame, text="Détail du robot")
        self.label.config(font = self.root.fontButton, anchor= 'w', bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 0, columnspan= 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Détail des capteurs")
        self.label.config(font = self.root.fontButton, anchor= 'w', bg= self.root.defaultbg)
        self.label.grid(column = 3, row = 0, columnspan= 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Détail des actionneurs")
        self.label.config(font = self.root.fontButton, anchor= 'w', bg= self.root.defaultbg)
        self.label.grid(column = 5, row = 0, columnspan= 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Nom du robot: ")
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 1, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Nombre de rapports: ", state= 'disabled')
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Type du robot: ", state= 'disabled')
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 3, sticky= 'w')

        self.label = tk.Entry(self.centerSubFrame, textvariable= self.nameRobot)
        self.label.config(font = self.root.fontLabel, bg= 'white')
        self.label.grid(column = 2, row = 1)

        self.entry = tk.Entry(self.centerSubFrame, textvariable= self.gearsRobot, state= 'disabled')
        self.entry.config(font= self.root.fontLabel, bg= self.root.defaultbg)
        self.entry.grid(column = 2, row = 2)

        self.entry = tk.Entry(self.centerSubFrame, textvariable= self.typeRobot, state= 'disabled')
        self.entry.config(font= self.root.fontLabel, bg= self.root.defaultbg)
        self.entry.grid(column = 2, row = 3)

        self.button = tk.Button(self.masterFrame, text="Valider", command= self.ValidateCalibration)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= self.root.validerRelX, rely= self.root.validerRelY)

        self.button = tk.Button(self.masterFrame, text="Calibration automatique", command= self.AutomaticCalibration)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= 0.5, rely= self.root.validerRelY)

        self.button = tk.Button(self.masterFrame, text="Retour", command= self.Close)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= self.root.retourRelX, rely= self.root.retourRelY)

        # Création de la console
        self.diagConsole = tk.Listbox(self.centerSubFrameBis, bg= 'white', width= 75, height= 38)
        self.diagConsole.pack()


    def Open(self):

        # Appel de la fonction de changement de page depuis GUI_utils.py
        SwitchWindow(self.masterFrame,self.root)

        # Rafraichissement des données de la page
        self.RefreshSelection()
        self.Refresh()


    def Close(self):

        retour = Popup(self, 2, texte= "Toute calibration non validée sera perdue.", fermer= "Annuler", valider= "Quitter")
        if retour == True:
            self.root.maintenanceWindow.Open()

    def RefreshSelection(self):

        # Rafraichissement de la robot sélectionnée dans le menu déroulant sur la page de de maintenance
        self.robotSelected = self.root.maintenanceWindow.robotSelected
        self.robotAttributes = self.root.dB.GetRobotAttributes(self.robotSelected.get())
        self.title.set("Calibration du robot: "+self.robotSelected.get())


    def Refresh(self):

        # Rafraichissement des variables des champs de texte
        self.nameRobot.set(self.robotAttributes['Name'])
        self.gearsRobot.set(self.robotAttributes['Gears'])
        self.typeRobot.set(self.robotAttributes['Type'])

        # Destruction de la partie variable de la page
        for i in range(len(self.sensorEntryVarList)):
            sensor = self.sensorEntryVarList[-1]
            for j in range(len(sensor)):
                if type(sensor[-1]) == tuple:
                    for k in range(len(sensor[-1])):
                        sensor[-1][k].set(None)
                else:
                    sensor[-1].set(None)
                sensor.pop()
            self.sensorEntryVarList.pop()
        while self.sensorLabelList != []:
            self.sensorLabelList[-1].destroy()
            self.sensorLabelList.pop()
        while self.sensorEntryList != []:
            self.sensorEntryList[-1].destroy()
            self.sensorEntryList.pop()

        for i in range(len(self.actuatorEntryVarList)):
            actuator = self.actuatorEntryVarList[-1]
            for j in range(len(actuator)):
                if type(actuator[-1]) == tuple:
                    for k in range(len(actuator[-1])):
                        actuator[-1][k].set(None)
                else:
                    actuator[-1].set(None)
                actuator.pop()
            self.actuatorEntryVarList.pop()
        while self.actuatorLabelList != []:
            self.actuatorLabelList[-1].destroy()
            self.actuatorLabelList.pop()
        while self.actuatorEntryList != []:
            self.actuatorEntryList[-1].destroy()
            self.actuatorEntryList.pop()

        # Création des nouveaux labels pour les capteurs
        rowCount = 1
        for category in self.robotAttributes['Sensors']:
            for subCategory in self.robotAttributes['Sensors'][category]:
                sensor = self.robotAttributes['Sensors'][category][subCategory]
                sensorVarList = []
                self.sensorLabelList.append(tk.Label(self.centerSubFrame, text= "Type:", state= 'disabled'))
                self.sensorLabelList[-1].config(font= self.root.fontLabel, bg= self.root.defaultbg)
                self.sensorLabelList[-1].grid(row= rowCount, column= 3, sticky= 'w')
                sensorVarList.append(tk.StringVar())
                sensorVarList[-1].set(category)
                self.sensorEntryList.append(tk.Entry(self.centerSubFrame, text= sensorVarList[-1], state= 'disabled', width= 16))
                self.sensorEntryList[-1].config(font= self.root.fontLabel)
                self.sensorEntryList[-1].grid(row= rowCount, column= 4)
                rowCount +=1
                self.sensorLabelList.append(tk.Label(self.centerSubFrame, text= "Sous Type:", state= 'disabled'))
                self.sensorLabelList[-1].config(font= self.root.fontLabel, bg= self.root.defaultbg)
                self.sensorLabelList[-1].grid(row= rowCount, column= 3, sticky= 'w')
                sensorVarList.append(tk.StringVar())
                sensorVarList[-1].set(subCategory)
                self.sensorEntryList.append(tk.Entry(self.centerSubFrame, text= sensorVarList[-1], state= 'disabled', width= 16))
                self.sensorEntryList[-1].config(font= self.root.fontLabel)
                self.sensorEntryList[-1].grid(row= rowCount, column= 4, sticky= 'w')
                rowCount +=1
                if sensor != None:
                    for dataKey in sensor:
                        sensorVarList.append((tk.StringVar(),tk.StringVar()))
                        sensorVarList[-1][0].set(dataKey)
                        self.sensorLabelList.append(tk.Label(self.centerSubFrame, textvariable= sensorVarList[-1][0]))
                        self.sensorLabelList[-1].config(font= self.root.fontLabel, bg= self.root.defaultbg)
                        self.sensorLabelList[-1].grid(row= rowCount, column= 3, sticky= 'w')
                        sensorVarList[-1][1].set(sensor[dataKey])
                        self.sensorEntryList.append(tk.Entry(self.centerSubFrame, textvariable= sensorVarList[-1][1], width= 6, validate= 'key', validatecommand= (self.vcmdFloat, '%P')))
                        self.sensorEntryList[-1].config(font= self.root.fontLabel)
                        self.sensorEntryList[-1].grid(row= rowCount, column= 4, sticky= 'w')
                        rowCount +=1
                self.sensorEntryVarList.append(sensorVarList)

        # Création des nouveaux labels pour les actionneurs
        rowCount = 1

        for category in self.robotAttributes['Actuators']:
            for subCategory in self.robotAttributes['Actuators'][category]:
                actuator = self.robotAttributes['Actuators'][category][subCategory]
                actuatorVarList = []
                self.actuatorLabelList.append(tk.Label(self.centerSubFrame, text= "Type:", state= 'disabled'))
                self.actuatorLabelList[-1].config(font= self.root.fontLabel, bg= self.root.defaultbg)
                self.actuatorLabelList[-1].grid(row= rowCount, column= 5, sticky= 'w')
                actuatorVarList.append(tk.StringVar())
                actuatorVarList[-1].set(category)
                self.actuatorEntryList.append(tk.Entry(self.centerSubFrame, text= actuatorVarList[-1], state= 'disabled'))
                self.actuatorEntryList[-1].config(font= self.root.fontLabel, width= 17)
                self.actuatorEntryList[-1].grid(row= rowCount, column= 6)
                rowCount +=1
                self.actuatorLabelList.append(tk.Label(self.centerSubFrame, text= "Sous Type:", state= 'disabled'))
                self.actuatorLabelList[-1].config(font= self.root.fontLabel, bg= self.root.defaultbg)
                self.actuatorLabelList[-1].grid(row= rowCount, column= 5, sticky= 'w')
                actuatorVarList.append(tk.StringVar())
                actuatorVarList[-1].set(subCategory)
                self.actuatorEntryList.append(tk.Entry(self.centerSubFrame, text= actuatorVarList[-1], state= 'disabled'))
                self.actuatorEntryList[-1].config(font= self.root.fontLabel, width= 17)
                self.actuatorEntryList[-1].grid(row= rowCount, column= 6)
                rowCount +=1
                if actuator != None:
                    for dataKey in actuator:
                        actuatorVarList.append((tk.StringVar(),tk.StringVar()))
                        actuatorVarList[-1][0].set(dataKey)
                        self.actuatorLabelList.append(tk.Label(self.centerSubFrame, textvariable= actuatorVarList[-1][0]))
                        self.actuatorLabelList[-1].config(font= self.root.fontLabel, bg= self.root.defaultbg)
                        self.actuatorLabelList[-1].grid(row= rowCount, column= 5, sticky= 'w')
                        actuatorVarList[-1][1].set(actuator[dataKey])
                        self.actuatorEntryList.append(tk.Entry(self.centerSubFrame, textvariable= actuatorVarList[-1][1], width= 15, validate= 'key', validatecommand= (self.vcmdFloat, '%P')))
                        self.actuatorEntryList[-1].config(font= self.root.fontLabel)
                        self.actuatorEntryList[-1].grid(row= rowCount, column= 6, sticky= 'w')
                        rowCount +=1
                self.actuatorEntryVarList.append(actuatorVarList)

    def AutomaticCalibration(self):
        # Lancement de la calibration automatique après popup de vérification
        validation = Popup(self, 2, texte= "ATTENTION: Le processus de calibration ne peut pas être interrompu.", valider= "Continuer", fermer= "Annuler")
        if validation == False:
            return
        validation = AutoCalib(self)
        if validation == True:
            self.Refresh()
            Popup(self, 1, texte= "La calibration automatique a été effectuée, vous pouvez rebrancher les capteurs.")
        else:
            Popup(self, 1, texte= "Il y a eu une erreur lors de la calibration.")


    def _resizeCanvas(self, event):

        self.centerCanvas.configure(scrollregion=self.centerCanvas.bbox("all"),width=1250,height=600)


    def ValidateCalibration(self):

        # Remise à zéro des listes de données pour éviter les duplicatas
        self.sensorDict = {}
        self.actuatorDict = {}

        # On récupère la liste des valeurs des capteurs depuis les champs de texte
        for sensor in self.sensorEntryVarList:
            category = sensor[0].get()
            subCategory = sensor[1].get()
            try:
                self.sensorDict[category]
            except:
                self.sensorDict[category] = {}
            self.sensorDict[category][subCategory] = {}
            for dataTuple in sensor[2:]:
                if dataTuple[1].get() == None or dataTuple[1].get() == '':
                    self.sensorDict[category][subCategory][dataTuple[0].get()] = float(0)
                elif dataTuple[1].get() == 'None':
                    self.sensorDict[category][subCategory][dataTuple[0].get()] = None
                else:
                    try:
                        self.sensorDict[category][subCategory][dataTuple[0].get()] = float(dataTuple[1].get())
                    except:
                        self.sensorDict[category][subCategory][dataTuple[0].get()] = dataTuple[1].get()

        # On récupère la liste des valeurs des actionneurs depuis les champs de texte
        for actuator in self.actuatorEntryVarList:
            category = actuator[0].get()
            subCategory = actuator[1].get()
            try:
                self.actuatorDict[category]
            except:
                self.actuatorDict[category] = {}
            self.actuatorDict[category][subCategory] = {}
            for dataTuple in actuator[2:]:
                if dataTuple[1].get() == None or dataTuple[1].get() == '':
                    self.actuatorDict[category][subCategory][dataTuple[0].get()] = float(0)
                elif dataTuple[1].get() == 'None':
                    self.actuatorDict[category][subCategory][dataTuple[0].get()] = None
                else:
                    try:
                        self.actuatorDict[category][subCategory][dataTuple[0].get()] = float(dataTuple[1].get())
                    except:
                        self.actuatorDict[category][subCategory][dataTuple[0].get()] = dataTuple[1].get()


        # On ouvre une popup de validation et on récupère le choix de l'utilisateur
        confirmation = Popup(self, 2, texte= "Souhaitez-vous confirmer la calibration ?", valider= "Oui", fermer= "Non")

        # On modifie les valeurs de la robot dans la base de donnée via la fonction de robot_dB et on ouvre un popup de confirmation
        if confirmation == True:
            self.root.dB.ModifyRobot(self.robotSelected.get(), self.nameRobot.get(), int(self.gearsRobot.get()), self.typeRobot.get(), self.sensorDict, self.actuatorDict)
            Popup(self, 1, texte= "La calibration du robot " + self.nameRobot.get() + " a été enregistré dans la base de données.")

        # On réinitialise les listes de capteurs et d'actionneurs
        self.sensorDict = {}
        self.actuatorDict = {}

        # On ferme la page de calibration
        self.root.maintenanceWindow.Open()

    def _validateEntryFloat(self,inp):

        # Vérification que l'entrée le caractère ajouté donne bien un flottant
        try:
            float(inp)
            return True
        except:
            if inp == '':
                return True
            return False
