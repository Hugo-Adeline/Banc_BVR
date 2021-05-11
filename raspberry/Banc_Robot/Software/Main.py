# -*- coding: utf-8 -*-

import os
filepath = os.path.dirname(os.path.abspath(__file__)) 
from GUI.Root import Root
from RaspberryInterface.RaspberryInterface import RaspberryInterface
from dataBase.DataBase import DataBase


def main():
    
    # Initialisation de la base de données
    dBFileName = "Robot_dB.csv"
    dBpath = filepath + '/dataBase/' + dBFileName
    dB = DataBase(dBpath)
    
    # Initialisation de l'interface de la raspberry
    interface = RaspberryInterface()
    
    # Initialisation de l'interface graphique
    GUI = Root(dB, interface, filepath)
    
    # Démarrage du logiciel
    GUI.Start()
    
main()
