import matplotlib.pyplot as plt
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
from time import sleep, time
import _thread

plt.ion()
class DynamicUpdate():
	def __init__(self):
		#Paramétrage
		self.min_x = 0
		self.max_x = 15
		self.min_y = 0
		self.max_y = 3.4
		#Initialisation des variables
		self.t0 = time()
		self.xdata1 = []
		self.ydata1 = []
		self.xdata2 = []
		self.ydata2 = []
		self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0,0))

	def on_launch(self):
		#Création de la figure
		self.figure, self.ax = plt.subplots()
		self.lines1, = self.ax.plot([],[])
		self.lines2, = self.ax.plot([],[])
		#Paramétrage de la figure
		self.ax.set_xlim(self.min_x, self.max_x)
		self.ax.set_ylim(self.min_y, self.max_y)
		self.ax.grid()
		#Paramétrage des GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(14,GPIO.OUT)
		GPIO.output(14,GPIO.HIGH)

	def on_running(self, xdata1, ydata1, xdata2, ydata2):
		#Rafraichissement des données de courbes
		self.lines1.set_xdata(xdata1)
		self.lines1.set_ydata(ydata1)
		self.lines2.set_xdata(xdata2)
		self.lines2.set_ydata(ydata2)
		#We need to draw *and* flush
		try:
			self.figure.canvas.draw()
			self.figure.canvas.flush_events()
		except:
			None

	#Fonction de démarrage
	def __call__(self):
		self.on_launch()
		#Création des variables internes
		temps = 0
		value = 0
		ncycle = 0
		#Démarrage de l'acquisition des données sur un thread séparé
		_thread.start_new_thread(self.refreshValues, ())
		#Affichage en continu des données
		while True:
			self.t0 = time()
			self.xdata1 = []
			self.ydata1 = []
			self.xdata2 = []
			self.ydata2 = []
			while time() - self.t0 <= self.max_x:
				self.on_running(self.xdata1, self.ydata1, self.xdata2, self.ydata2)

	def refreshValues(self):
		#Acquisition des valeurs pour le channel 1 et 2
		while True:
			value = self.mcp.read_adc(0)*5/1024
			temps = time() - d.t0
			d.xdata1.append(temps)
			d.ydata1.append(value)
			value = self.mcp.read_adc(0)*5/1024
			temps = time() - d.t0
			d.xdata2.append(temps)
			d.ydata2.append(value)

d = DynamicUpdate()
d()
