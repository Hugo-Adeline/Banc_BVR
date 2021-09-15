# -*- coding: utf-8 -*-
from time import sleep

def LowerPressure(self, pressureSensorTest= False):

	pressureSensor = self.root.interface.sensorClass['Pression']['Robot']

	# Récupération des actionneurs hydraulique du robot
	evDict = self.robotAttributes['Actuators']['Electrovanne']
	evClassList = []
	for subCategory in evDict:
		evClassList.append(self.root.interface.actuatorClass['Electrovanne'][subCategory])

	margin = self.robotAttributes['Margin']
	scaling = self.robotAttributes['Sensors']['Pression']['Robot']['MarginScaling']
	target = self.robotAttributes['Sensors']['Pression']['Robot']['Min']

	# Activation répétée des actionneurs jusqu'à ce que la pression atteigne le minimum avec un timeout si jamais atteinte
	for i in range(10):
		self.root.update()
		for ev in evClassList:
			ev.Set(state= 1)
			sleep(0.5)
			ev.Set(state= 0)
			sleep(0.25)
		if pressureSensorTest:
			pressure = pressureSensor.Poll(10)
			# La pression a-t-elle atteint Pmin ?
			print("pression = ", pressure, "; target = ", target + margin*scaling)
			if ((pressure <= target + margin*scaling) and (pressure >= target - margin*scaling)):
				return

	"""
	# Retour de la validation de l'abaissement de pression
	if counter == 20:
		return False
	else:
		return True
	"""
