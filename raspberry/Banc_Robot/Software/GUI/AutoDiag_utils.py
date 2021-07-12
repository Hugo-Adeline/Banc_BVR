# -*- coding: utf-8 -*-
from time import sleep

def LowerPressure(self, pressureSensorTest= False):

	pressureSensor = self.root.interface.sensorClass['Pression']['Robot']

	# Récupération des actionneurs hydraulique du robot
	evDict = self.robotAttributes['Actuators']['Electrovanne']
	evClassList = []
	for subCategory in evDict:
		evClassList.append(self.root.interface.actuatorClass['Electrovanne'][subCategory])

	margin = self.root.interface.margin
	dev = self.robotAttributes['Sensors']['Pression']['Robot']['Deviation']
	target = self.robotAttributes['Sensors']['Pression']['Robot']['Min']

	# Activation répétée des actionneurs jusqu'à ce que la pression atteigne le minimum avec un timeout si jamais atteinte
	for i in range(10):
		for ev in evClassList:
			ev.Set(state= 1)
			sleep(0.5)
			ev.Set(state= 0)
			sleep(0.25)
		if pressureSensorTest:
			pressure = pressureSensor.Poll(10)
			# La pression a-t-elle atteint Pmin ?
			print("pression = ", pressure, "; target = ", target + margin*dev)
			if ((pressure <= target + margin*dev) and (pressure >= target - margin*dev)):
				return

	"""
	# Retour de la validation due l'abaissement de pression
	if counter == 20:
		return False
	else:
		return True
	"""
