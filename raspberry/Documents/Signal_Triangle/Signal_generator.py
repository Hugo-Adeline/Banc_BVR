import RPi.GPIO as GPIO
from time import time
from math import trunc

x = []              #Signal triangle
x1 = []             #Intégrale signal triangle
y = []              #Largeur d'impulsion (en %)
y1 = []             #Signal carré
t = []              #Temps
t1 = []             #Temps carré
At = 2              #Amplitude triangle
Ac = 3.3
e = 500             #Fréquence d'échantillonnage
P = 0.02            #Période
pt = trunc(e*P)     #Points triangle
pc = 25             #Résolution signal carré
pin1 = 4            #Pin bobinage principal
pin2 = 16           #Pin Bobinage secondaire

for k in range(pt):
    t.append(k/e)

for k in range(pt):
    if (k/e)%P <= P/2:
        x.append(2*At/P*((k/e)%P))
    else:
        x.append(2*At*(1-1/P*((k/e)%P)))

for k in range(pt):
    x1.append(min(x[k],x[k-1])*1/e + (max(x[k],x[k-1])-min(x[k],x[k-1]))/e/2)
    y.append(x1[k]/Ac*e*pc)

for k in range(pt):
    for i in range(pc):
        if i < y[k]:
            y1.append(GPIO.HIGH)
        else:
            y1.append(GPIO.LOW)
        t1.append(k/e+i/pc/e)

t = t1
y = y1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

while True:
    step = 0
    t0 = time()
    while step != len(y)-1:
        if step <= len(y)/5:
            GPIO.output(pin2, GPIO.HIGH)
        else:
            GPIO.output(pin2, GPIO.LOW)
        GPIO.output(pin1, y[step])
        while time() - t0 < t[step]:
            None
        step += 1
