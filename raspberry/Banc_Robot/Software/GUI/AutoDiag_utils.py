# -*- coding: utf-8 -*-
from time import sleep

def LowerPressure(self):

	pressureSensor = self.root.interface.sensorClass['Pression']['Robot']

	# Récupération des actionneurs hydraulique du robot
	evDict = self.robotAttributes['Actuators']['Electrovanne']
	evClassList = []
	for subCategory in evDict:
		evClassList.append(self.root.interface.actuatorClass['Electrovanne'][subCategory])

	# Activation répétée des actionneurs jusqu'à ce que la pression atteigne le minimum avec un timeout si jamais atteinte
	counter = 0
	while (pressureSensor.Poll() > self.root.interface.margin*self.robotAttributes['Sensors']['Pression']['Robot']['Deviation'] + self.robotAttributes['Sensors']['Pression']['Robot']['Min']) and (counter < 20):
		for ev in evClassList:
			ev.Set(state= 1)
			sleep(0.5)
			ev.Set(state= 0)
			sleep(0.25)
		counter += 1

	# Retour de la validation due l'abaissement de pression
	if counter == 20:
		return False
	else:
		return True
