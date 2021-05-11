# -*- coding: utf-8 -*-

import tkinter as tk
from GUI.GUI_utils import SwitchWindow, RefreshOptionMenu, Popup

class MaintenanceWindow():
    def __init__(self, root):
        
        # Définition de la fenêtre Parent
        self.root = root
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)
        
        # Création des cadres
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)
        self.centerFrame = tk.Frame(self.masterFrame, relief= 'groove', bd= 3, height= 250, width= 500, bg= self.root.defaultbg)
        self.bottomFrame = tk.Frame(self.centerFrame, bg= self.root.defaultbg)
        self.topFrame = tk.Frame(self.centerFrame, bg= self.root.defaultbg)
        
        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerFrame.pack_propagate(0)
        self.centerFrame.pack(side= 'top', expand = True)
        self.topFrame.pack(pady = 25)
        self.bottomFrame.pack()
        
        # Déclaration des variables
        self.robotList = self.root.dB.GetRobotNameList()
        self.robotSelected = tk.StringVar(self.root)
        self.robotSelected.set(self.robotList[0])
        
    def Setup(self):
        
        # Création des labels et boutons fixes
        self.label = tk.Label(self.titleFrame, text="Maintenance de la base de données")
        self.label.config(font = self.root.fontTitle, bg= self.root.defaultbg)
        self.label.pack(pady = self.root.titlePadY)
        
        self.label = tk.Label(self.topFrame, text="Sélectionnez le robot à calibrer:")
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.pack()
        
        self.om = tk.OptionMenu(self.topFrame, self.robotSelected, *self.robotList)
        self.om.config(font = self.root.fontButton, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
        self.om.pack()
        
        self.button = tk.Button(self.topFrame, text="Calibrer le robot", command= self.root.calibrationWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.pack()
        
        self.button = tk.Button(self.bottomFrame, text="Ajouter un robot", command= self.root.addRobotWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.pack()
        
        self.button = tk.Button(self.bottomFrame, text="Retirer un robot", command= self.root.removeRobotWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.pack(pady = 2)
        
        self.button = tk.Button(self.masterFrame, text="Retour", command= self.root.mainMenuWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= self.root.retourRelX, rely= self.root.retourRelY)
        
    def Open(self):
        if self.root.activeFrame == self.root.mainMenuWindow.masterFrame:
            retour = Popup(self, 2, texte= "ATTENTION: Ce menu est réservé aux personnel habilité.", valider= "Continuer", fermer= "Retour")
            if retour == False:
                return
        SwitchWindow(self.masterFrame,self.root)
        RefreshOptionMenu(self)

        
