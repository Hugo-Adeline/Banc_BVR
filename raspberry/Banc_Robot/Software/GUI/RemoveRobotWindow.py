# -*- coding: utf-8 -*-

import tkinter as tk
from GUI.GUI_utils import SwitchWindow, Popup, RefreshOptionMenu

class RemoveRobotWindow():
    def __init__(self, root):

        # Définition de la fenêtre Parent
        self.root = root
        self.masterFrame = tk.Frame(self.root, bg= self.root.defaultbg)

        # Création des cadres
        self.titleFrame = tk.Frame(self.masterFrame, bg= self.root.defaultbg)
        self.centerFrame = tk.Frame(self.masterFrame, relief= 'groove', bd= 3, height= 250, width= 500, bg= self.root.defaultbg)
        self.centerSubFrame = tk.Frame(self.centerFrame, bg= self.root.defaultbg)

        # Placement des cadres
        self.titleFrame.pack(side= 'top')
        self.centerFrame.pack_propagate(0)
        self.centerFrame.pack(side= 'top', expand = True)
        self.centerSubFrame.pack(side= 'top', expand = True)

        # Déclaration des variables
        self.robotList = self.root.dB.GetRobotNameList()
        self.robotSelected = tk.StringVar(self.root)
        self.robotSelected.set(self.robotList[0])


    def Setup(self):

        # Création des boutons et labels fixes
        self.label = tk.Label(self.titleFrame, text= "Supprimer un robot de la base de données")
        self.label.config(font= self.root.fontTitle, bg= self.root.defaultbg)
        self.label.pack(pady= self.root.titlePadY)

        self.label = tk.Label(self.centerSubFrame, text="Sélectionnez le robot à supprimer :")
        self.label.config(font= self.root.fontLabel, bg= self.root.defaultbg)
        self.label.pack(pady= 10)

        self.om = tk.OptionMenu(self.centerSubFrame, self.robotSelected, *self.robotList)
        self.om.config(font= self.root.fontButton, bg= 'white', activebackground= 'white', relief= 'sunken', highlightbackground= self.root.defaultbg)
        self.om.pack()

        self.button = tk.Button(self.centerSubFrame, text="Supprimer", command= self.Remove)
        self.button.config(font= self.root.fontButton, bg= 'lightgrey')
        self.button.pack(pady= 10)

        self.button = tk.Button(self.masterFrame, text="Retour", command= self.root.maintenanceWindow.Open)
        self.button.config(font= self.root.fontButton, bg= 'lightgrey')
        self.button.place(relx= self.root.retourRelX, rely= self.root.retourRelY)



    def Open(self):
        SwitchWindow(self.masterFrame,self.root)
        RefreshOptionMenu(self)


    def Remove(self):

        # Popup de confirmation
        confirmation = Popup(self, 2, texte= "Souhaitez-vous confirmer la suppression du robot " + self.robotSelected.get() + " ?", valider= "Oui", fermer= "Non")
        if confirmation == False:
            return
        retour = self.root.dB.DeleteRobot(self.robotSelected.get())

        # Vérification que la suppression a bien été effectuée
        if retour == False:
            Popup(self, 1, texte= "Impossible de supprimer le dernier robot.")
            return

        Popup(self, 1, texte= "Le robot " + self.robotSelected.get() + " a bien été supprimé.")

        # Remise à zéro des menus déroulants
        RefreshOptionMenu(self)
        self.robotSelected.set(self.robotList[0])
        self.root.mainMenuWindow.robotSelected.set(self.robotList[0])
        self.root.maintenanceWindow.robotSelected.set(self.robotList[0])
