# -*- coding: utf-8 -*-

import tkinter as tk
import subprocess
from GUI.GUI_utils import SwitchWindow, RefreshOptionMenu, Popup

class MainMenuWindow():
    def __init__(self, root):

        # Définition de la fenêtre Parent
        self.root = root

        # Création de la frame qui contient la page
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)

        # Déclaration et initialisation des variables pour le menu déroulant
        self.robotList = self.root.dB.GetRobotNameList()
        self.robotSelected = tk.StringVar(self.root)
        self.robotSelected.set(self.robotList[0])

        # Création des cadres
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)
        self.centerFrame = tk.Frame(self.masterFrame, relief= 'groove', bd= 3, height= 300, width= 750, bg= self.root.defaultbg)
        self.centerSubFrame = tk.Frame(self.centerFrame, bg= self.root.defaultbg)

        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerFrame.pack_propagate(0)
        self.centerFrame.pack(side= 'top', expand = True)
        self.centerSubFrame.pack(side= 'top', expand = True)

    def Setup(self):

        # Création des boutons et labels fixes
        self.label = tk.Label(self.titleFrame, text="Banc d'essai pour robot de boîte de vitesses")
        self.label.config(font = self.root.fontTitle, bg= self.root.defaultbg)
        self.label.pack(pady = self.root.titlePadY)

        self.label = tk.LabelFrame(self.centerSubFrame, text= 'Menu Principal')

        self.label = tk.Label(self.centerSubFrame, text="Sélectionnez le modèle du robot et le type de diagnostic:")
        self.label.config(font = self.root.fontLabel, bg= self.root.defaultbg)
        self.label.pack()

        self.om = tk.OptionMenu(self.centerSubFrame, self.robotSelected, *self.robotList)
        self.om.config(font = self.root.fontButton, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
        self.om.pack(pady = 8)

        self.button = tk.Button(self.centerSubFrame, text="Diagnostic automatique", command= self.root.automaticDiagnosisWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.pack(pady = 2)

        self.button = tk.Button(self.centerSubFrame, text="Diagnostic manuel", command= self.root.manualDiagnosisWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.pack()

        self.button = tk.Button(self.masterFrame, text="Gestion base de données", command= self.root.maintenanceWindow.Open)
        self.button.config(font = self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= 0.75, rely= 0.2)

        self.button = tk.Button(self.masterFrame, text="Arrêter", command= self.Close)
        self.button.config(font = self.root.fontButton, bg = 'lightgrey')
        self.button.place(relx= self.root.retourRelX, rely= self.root.retourRelY)

    def Open(self):
        SwitchWindow(self.masterFrame, self.root)
        RefreshOptionMenu(self)

    def Close(self):

        # Popup de confirmation pour arrêter le programme et éteindre la Raspberry
        arret = Popup(self, 2, texte= "Etes-vous sûr de vouloir arrêter le système ?", valider= "Oui", fermer= "Non")
        if arret == True:
            command = "/usr/bin/sudo /sbin/shutdown -h now"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            process.communicate()[0]
            self.root.destroy()
