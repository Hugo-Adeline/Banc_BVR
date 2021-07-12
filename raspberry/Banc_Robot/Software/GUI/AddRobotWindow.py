# -*- coding: utf-8 -*-

import tkinter as tk
from GUI.GUI_utils import SwitchWindow, Popup

class AddRobotWindow():
    def __init__(self, root):

        # Définition de la fenêtre Parent
        self.root = root
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)

        # Création des cadres
        self.centerSubFrame = tk.Frame(self.masterFrame, relief= 'groove', bd = 3, bg= self.root.defaultbg)
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)

        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerSubFrame.pack(side= 'top', expand = True)

        # Création des fonction interne pour la validation du texte des Entry
        self.vcmd2Int = self.root.register(self._validateEntry2Int)
        self.vcmd1Int = self.root.register(self._validateEntry1Int)

        # Définition des paramètres de mise en page
        self.entryWidth = 10

        # Déclaration des variables
        self.typeRobotList = ['Hydraulique', 'Electrique', 'Hybride']
        self.nameRobot = tk.StringVar()
        self.numberOfGear = tk.StringVar()
        self.typeRobot = tk.StringVar()
        self.sensorAmountEntry = tk.StringVar()
        self.actuatorAmountEntry = tk.StringVar()
        self.sensorAmountEntry.set(0)
        self.actuatorAmountEntry.set(0)
        self.numberOfGear.set(0)
        self.typeRobot.set(self.typeRobotList[0])
        self.sensorOMList = []
        self.sensorSubOMList = []
        self.actuatorOMList = []
        self.actuatorSubOMList = []
        self.sensorOMVarList = []
        self.sensorSubOMVarList = []
        self.actuatorOMVarList = []
        self.actuatorSubOMVarList = []
        self.sensorLabelList = []
        self.actuatorLabelList = []
        self.sensorDict = []
        self.actuatorDict = []
        self.sensorAmount = 0
        self.actuatorAmount = 0


    def Setup(self):

        # Création des boutons et labels fixes
        self.label = tk.Label(self.titleFrame, text="Ajouter un robot à la base de données")
        self.label.config(font = self.root.fontTitle, bg= self.root.defaultbg)
        self.label.pack(side= 'top', pady = self.root.titlePadY)

        self.label = tk.Label(self.centerSubFrame, text="Détail du robot")
        self.label.config(font = self.root.fontButton, anchor= 'w', width = 30, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 0, columnspan= 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Détail des capteurs")
        self.label.config(font = self.root.fontButton, width = 20, anchor= 'w', bg= self.root.defaultbg)
        self.label.grid(column = 3, row = 0, columnspan= 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Position")
        self.label.config(font = self.root.fontButton, width = 20, anchor= 'w', bg= self.root.defaultbg)
        self.label.grid(column = 5, row = 0, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Détail des actionneurs")
        self.label.config(font = self.root.fontButton, width = 25, anchor= 'w', bg= self.root.defaultbg)
        self.label.grid(column = 6, row = 0, columnspan= 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Position")
        self.label.config(font = self.root.fontButton, width = 20, anchor= 'w', bg= self.root.defaultbg)
        self.label.grid(column = 8, row = 0, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Nom du robot:", bg= self.root.defaultbg)
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 1, sticky= 'w')

        self.entry = tk.Entry(self.centerSubFrame, textvariable= self.nameRobot)
        self.entry.config(font= self.root.fontLabel, width= self.entryWidth)
        self.entry.grid(column = 2, row = 1, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Nombre de rapports:")
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 2, sticky= 'w')

        self.entry = tk.Entry(self.centerSubFrame, textvariable= self.numberOfGear, validate= 'key', validatecommand= (self.vcmd1Int, '%P'))
        self.entry.config(font= self.root.fontLabel, width= self.entryWidth-9)
        self.entry.grid(column = 2, row = 2, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Type du robot:", bg= self.root.defaultbg)
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 3, sticky= 'w')

        self.om = tk.OptionMenu(self.centerSubFrame, self.typeRobot, *self.typeRobotList)
        self.om.config(font = self.root.fontLabel, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
        self.om['menu'].config(bg= 'white', font= self.root.fontLabel)
        self.om.grid(column = 2, row = 3, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Nombre de capteurs:")
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 4, sticky= 'w')

        self.entry = tk.Entry(self.centerSubFrame, textvariable= self.sensorAmountEntry, validate= 'key', validatecommand= (self.vcmd2Int, '%P'))
        self.entry.config(font= self.root.fontLabel, width= self.entryWidth-8)
        self.entry.grid(column = 2, row = 4, sticky= 'w')

        self.label = tk.Label(self.centerSubFrame, text="Nombre d'actionneurs:")
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.grid(column = 1, row = 5, sticky= 'w')

        self.entry = tk.Entry(self.centerSubFrame, textvariable= self.actuatorAmountEntry, validate= 'key', validatecommand= (self.vcmd2Int, '%P'))
        self.entry.config(font= self.root.fontLabel, width= self.entryWidth-8)
        self.entry.grid(column = 2, row = 5, sticky= 'w')

        self.button = tk.Button(self.centerSubFrame, text="Mettre à jour", command= self.RefreshEntryNumber)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.grid(column = 1, row = 6, columnspan= 2)

        self.button = tk.Button(self.centerSubFrame, text="Reset", command= self.Reset)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.grid(column = 1, row = 7, columnspan= 2)

        self.button = tk.Button(self.masterFrame, text="Valider", command= self.Valid)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= self.root.validerRelX, rely= self.root.validerRelY)

        self.button = tk.Button(self.masterFrame, text="Retour", command= self.root.maintenanceWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= self.root.retourRelX, rely= self.root.retourRelY)


    def Open(self):
        SwitchWindow(self.masterFrame,self.root)

    def RefreshEntryNumber(self,var = 0):

        # Récupération du nombre de capteurs souhaité
        if self.sensorAmountEntry.get() == '':
            self.sensorAmount = 0
        else:
            self.sensorAmount = int(self.sensorAmountEntry.get())

        # Création de nouveaux widgets pour les capteurs si besoin
        while self.sensorAmount > len(self.sensorLabelList):
            # Labels
            self.sensorLabelList.append(tk.Label(self.centerSubFrame, text= "Capteur " + str(len(self.sensorLabelList)+1) + ":"))
            self.sensorLabelList[-1].config(font = self.root.fontLabel, bg= self.root.defaultbg)
            self.sensorLabelList[-1].grid(column= 3, row= len(self.sensorLabelList), sticky= 'w')
            # Variables pour les Menus Déroulants de séléction du type
            self.sensorOMVarList.append(tk.StringVar())
            self.sensorOMVarList[-1].set(self.root.interface.sensorList[0])
            # Menus Déroulants de séléction du type
            self.sensorOMList.append(tk.OptionMenu(self.centerSubFrame,
                                                   self.sensorOMVarList[-1],
                                                   *self.root.interface.sensorList,
                                                   command = self.RefreshEntryNumber))
            self.sensorOMList[-1].config(font = self.root.fontLabel, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
            self.sensorOMList[-1]['menu'].config(bg= 'white', font= self.root.fontLabel)
            self.sensorOMList[-1].grid(column= 4, row= len(self.sensorOMList), sticky= 'w')
            # Variables des Menus Déroulants de séléction du sous type
            self.sensorSubOMVarList.append(tk.StringVar())
            self.sensorSubOMVarList[-1].set(self.root.interface.sensorDict[self.sensorOMVarList[-1].get()][0])
            # Menus Déroulants de séléction du sous type
            self.sensorSubOMList.append(tk.OptionMenu(self.centerSubFrame,
                                                      self.sensorSubOMVarList[-1],
                                                      *self.root.interface.sensorDict[self.sensorOMVarList[-1].get()]))
            self.sensorSubOMList[-1].config(font = self.root.fontLabel, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
            self.sensorSubOMList[-1]['menu'].config(bg= 'white', font= self.root.fontLabel)
            self.sensorSubOMList[-1].grid(column= 5, row= len(self.sensorOMList), sticky= 'w')

        # Suppression d'anciens widgets pour les capteurs si besoin
        while self.sensorAmount < len(self.sensorLabelList):
            # Labels
            self.sensorLabelList[-1].destroy()
            self.sensorLabelList.pop()
            # Variables des Menus Déroulants de séléction du type
            self.sensorOMVarList[-1].set(None)
            self.sensorOMVarList.pop()
            # Menus Déroulants de séléction du type
            self.sensorOMList[-1].destroy()
            self.sensorOMList.pop()
            # Variables pour des Menus Déroulants de séléction du sous type
            self.sensorSubOMVarList[-1].set(None)
            self.sensorSubOMVarList.pop()
            # Menus Déroulants de séléction du sous type
            self.sensorSubOMList[-1].destroy()
            self.sensorSubOMList.pop()

        # Paramétrage des Menus Déroulants des sous types
        for i in range(len(self.sensorOMList)):
            # Récupération de la valeur du Menu Déroulant associé
            key = self.sensorOMVarList[i].get()
            # Vérification que le sous Menu Déroulant est différent
            if self.sensorSubOMVarList[i].get() not in self.root.interface.sensorDict[key]:
                # Changement de la valeur de la variable du Menu Déroulant
                self.sensorSubOMVarList[i].set(self.root.interface.sensorDict[key][0])
                # Suppression puis création d'un nouveau Menu Déroulant
                self.sensorSubOMList[i].destroy()
                self.sensorSubOMList[i] = (tk.OptionMenu(self.centerSubFrame,
                                                         self.sensorSubOMVarList[i],
                                                         *self.root.interface.sensorDict[key]))
                self.sensorSubOMList[i].config(font = self.root.fontLabel, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
                self.sensorSubOMList[i]['menu'].config(bg= 'white', font= self.root.fontLabel)
                self.sensorSubOMList[i].grid(column= 5, row= i+1, sticky= 'w')


        # Récupération du nombre de actionnerus souhaité
        if self.actuatorAmountEntry.get() == '':
            self.actuatorAmount = 0
        else:
            self.actuatorAmount = int(self.actuatorAmountEntry.get())

        # Création de nouveaux widgets pour les actionneurs si besoin
        while self.actuatorAmount > len(self.actuatorLabelList):
            # Labels
            self.actuatorLabelList.append(tk.Label(self.centerSubFrame, text= "Actionneur " + str(len(self.actuatorLabelList)+1) + ":"))
            self.actuatorLabelList[-1].config(font = self.root.fontLabel, bg= self.root.defaultbg)
            self.actuatorLabelList[-1].grid(column= 6, row= len(self.actuatorLabelList), sticky= 'w')
            # Variables pour les Menus Déroulants de séléction du type
            self.actuatorOMVarList.append(tk.StringVar())
            self.actuatorOMVarList[-1].set(self.root.interface.actuatorList[0])
            # Menus Déroulants de séléction du type
            self.actuatorOMList.append(tk.OptionMenu(self.centerSubFrame,
                                                           self.actuatorOMVarList[-1],
                                                           *self.root.interface.actuatorList,
                                                           command = self.RefreshEntryNumber))
            self.actuatorOMList[-1].config(font = self.root.fontLabel, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
            self.actuatorOMList[-1]['menu'].config(bg= 'white', font= self.root.fontLabel)
            self.actuatorOMList[-1].grid(column= 7, row= len(self.actuatorOMList), sticky= 'w')
            # Variables des Menus Déroulants de séléction du sous type
            self.actuatorSubOMVarList.append(tk.StringVar())
            self.actuatorSubOMVarList[-1].set(self.root.interface.actuatorDict[self.actuatorOMVarList[-1].get()][0])
            # Menus Déroulants de séléction du sous type
            self.actuatorSubOMList.append(tk.OptionMenu(self.centerSubFrame,
                                                      self.actuatorSubOMVarList[-1],
                                                      *self.root.interface.actuatorDict[self.actuatorOMVarList[-1].get()]))
            self.actuatorSubOMList[-1].config(font = self.root.fontLabel, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
            self.actuatorSubOMList[-1]['menu'].config(bg= 'white', font= self.root.fontLabel)
            self.actuatorSubOMList[-1].grid(column= 8, row= len(self.actuatorOMList), sticky= 'w')

        # Suppression d'anciens widgets pour les actionneurs si besoin
        while self.actuatorAmount < len(self.actuatorLabelList):
            # Labels
            self.actuatorLabelList[-1].destroy()
            self.actuatorLabelList.pop()
            # Variables des Menus Déroulants de séléction du type
            self.actuatorOMVarList[-1].set(None)
            self.actuatorOMVarList.pop()
            # Menus Déroulants de séléction du type
            self.actuatorOMList[-1].destroy()
            self.actuatorOMList.pop()
            # Variables pour des Menus Déroulants de séléction du sous type
            self.actuatorSubOMVarList[-1].set(None)
            self.actuatorSubOMVarList.pop()
            # Menus Déroulants de séléction du sous type
            self.actuatorSubOMList[-1].destroy()
            self.actuatorSubOMList.pop()

        # Paramétrage des Menus Déroulants des sous types
        for i in range(len(self.actuatorOMList)):
            # Récupération de la valeur du Menu Déroulant associé
            key = self.actuatorOMVarList[i].get()
            # Vérification que le sous Menu Déroulant est différent
            if self.actuatorSubOMVarList[i].get() not in self.root.interface.actuatorDict[key]:
                # Changement de la valeur de la variable du Menu Déroulant
                self.actuatorSubOMVarList[i].set(self.root.interface.actuatorDict[key][0])
                # Suppression puis création d'un nouveau Menu Déroulant
                self.actuatorSubOMList[i].destroy()
                self.actuatorSubOMList[i] = (tk.OptionMenu(self.centerSubFrame,
                                                         self.actuatorSubOMVarList[i],
                                                         *self.root.interface.actuatorDict[key]))
                self.actuatorSubOMList[i].config(font = self.root.fontLabel, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
                self.actuatorSubOMList[i]['menu'].config(bg= 'white', font= self.root.fontLabel)
                self.actuatorSubOMList[i].grid(column= 8, row= i+1, sticky= 'w')


    def Reset(self):

        # Remise à zéro des valeurs
        self.nameRobot.set('')
        self.numberOfGear.set(0)
        self.sensorAmountEntry.set(0)
        self.actuatorAmountEntry.set(0)
        self.typeRobot.set(self.typeRobotList[0])

        # Actualisation de la page avec les valeurs à zéro
        self.RefreshEntryNumber()


    def _validateEntry2Int(self,inp):

        # Vérification que la valeur entrée est bien un entier avec au plus 2 chiffres
        try:
            if (int(inp) < 0) or (int(inp) > 99):
                return False
        except:
            if inp == '':
                return True
            return False
        return True


    def _validateEntry1Int(self,inp):

        # Vérification que la valeur entrée est bien un entier a un chiffre
        try:
            if (int(inp) < 0) or (int(inp) > 9):
                return False
        except:
            if inp == '':
                return True
            return False
        return True


    def Valid(self):

        # On rafraichit la page pour éviter les bugs
        self.RefreshEntryNumber()

        # On vide les listes de données pour éviter les duplicatas
        self.sensorDict = {}
        self.actuatorDict = {}

        # On récupère le nombre de rapports et on vérifie qu'il vaut au moins 2
        if self.numberOfGear.get() == '':
            self.numberOfGear.set(0)
        if int(self.numberOfGear.get()) < 2:
            Popup(self, 1, texte= "La robot doit avoir au moins deux rapports.")
            return

        # On ajoute les capteurs sélectionnés à notre liste de données capteurs et on vérifie qu'il n'y a pas de doublon
        for i in range(len(self.sensorOMVarList)):
            category = self.sensorOMVarList[i].get()
            subCategory = self.sensorSubOMVarList[i].get()
            try:
                self.sensorDict[category]
            except:
                self.sensorDict[category] = {}
            if subCategory in self.sensorDict[category]:
                Popup(self, 1, texte= "La robot ne peut pas avoir deux fois le même capteur.")
                return
            self.sensorDict[category][subCategory] = (self.root.interface.sensorClass[category][subCategory].GetdBValues())

        # On ajoute les actionneurs sélectionnés à notre liste de données actionneurs et on vérifie qu'il n'y a pas de doublon
        for i in range(len(self.actuatorOMVarList)):
            category = self.actuatorOMVarList[i].get()
            subCategory = self.actuatorSubOMVarList[i].get()
            try:
                self.actuatorDict[category]
            except:
                self.actuatorDict[category] = {}
            if subCategory in self.actuatorDict[category]:
                Popup(self, 1, texte= "La robot ne peut pas avoir deux fois le même actionneur.")
                return
            for category in self.actuatorDict:
                if subCategory in self.actuatorDict[category]:
                    Popup(self, 1, texte= "La robot ne peut pas avoir deux actionneurs à la même position.")
                    return
            self.actuatorDict[category][subCategory] = (self.root.interface.actuatorClass[category][subCategory].GetdBValues())

        # On envoi le tout à la base de données et on vérifie qu'il n'y a pas eu d'erreur
        retour = self.root.dB.AddRobot(self.nameRobot.get() ,int(self.numberOfGear.get()), self.typeRobot.get(), self.sensorDict, self.actuatorDict)
        if retour == False:
            Popup(self, 1, texte= "La robot existe déjà ou le nom est invalide.")
            return
        Popup(self, 1, texte= "La robot a bien été ajouté.")

        # On remet à zéro la fenêtre
        self.Reset()
