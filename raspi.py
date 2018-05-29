
import sys
import time
import RPi.GPIO as GPIO
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("turn")
args = parser.parse_args()

## ------ ###

GPIO.setmode(GPIO.BCM)

Trig = 23          # Entree Trig du HC-SR04 branchee au GPIO 23
Echo = 24         # Sortie Echo du HC-SR04 branchee au GPIO 24

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

GPIO.output(Trig, False)
GPIO.output(Trig, True)
time.sleep(0.00001)
GPIO.output(Trig, False)

while GPIO.input(Echo) == 0:  # Emission de l'ultrason
    debutImpulsion = time.time()

while GPIO.input(Echo) == 1:  # Retour de l'Echo
    finImpulsion = time.time()

distance = round((finImpulsion - debutImpulsion) * 340 *
                 100 / 2, 1)  # Vitesse du son = 340 m/s

#----#

ForwardL=26
BackwardL=20
ForwardR=19
BackwardR=16
sleeptime=1


GPIO.setup(ForwardL, GPIO.OUT)
GPIO.setup(BackwardL, GPIO.OUT)
GPIO.setup(BackwardR, GPIO.OUT)
GPIO.setup(ForwardR, GPIO.OUT)

def forward(x):
	GPIO.output(ForwardL, GPIO.HIGH) # Envoyer une impulsion avant sur les moteurs de gauche
	GPIO.output(ForwardR, GPIO.HIGH) # Envoyer une impulsion avant sur les moteurs de droite
	print("Moving Forward")
	time.sleep(x)
	GPIO.output(ForwardL, GPIO.LOW) # arrêter une impulsion avant sur les moteurs de gauche
	GPIO.output(ForwardR, GPIO.LOW) # arrêter une impulsion avant sur les moteurs de droite

def reverse(x):
	GPIO.output(BackwardL, GPIO.HIGH)
	GPIO.output(BackwardR, GPIO.HIGH)
	print("Moving Backward")
	time.sleep(x)
	GPIO.output(BackwardL, GPIO.LOW)
	GPIO.output(BackwardR, GPIO.LOW)

def left(x):
    GPIO.output(ForwardL, GPIO.HIGH)
    GPIO.output(BackwardR, GPIO.HIGH)
    print("Moving left")
    time.sleep(x)
    GPIO.output(ForwardL, GPIO.LOW)
    GPIO.output(BackwardR, GPIO.LOW)


def right(x):
    GPIO.output(BackwardL, GPIO.HIGH)
    GPIO.output(ForwardR, GPIO.HIGH)
    print("Moving right")
    time.sleep(x)
    GPIO.output(BackwardL, GPIO.LOW)
    GPIO.output(ForwardR, GPIO.LOW)

if(args.turn == "left" ): # Appele la fonction "tourner a gauche" pour tourner a gauche
    left(1)

if(args.turn == "right"):
    right(1)

if(args.turn == "down"):
    reverse(1)

print(distance)

if(args.turn == "up" and distance >= 10):
    forward(1)


GPIO.cleanup()
