#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import datetime
from time import gmtime, strftime

# Taster_vorne = None
# Taster_Haustuer_unten = None
Taster_Haustuer_oben = 14

# Relais_oben = None
# Relais_unten = None
Relais = 7

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setwarnings(True)
GPIO.setup(Relais, GPIO.OUT)
GPIO.setup(Taster_Haustuer_oben, GPIO.IN)
GPIO.output(Relais, GPIO.LOW)

ruhe_start = datetime.time(20, 10, 0) # Start Uhrzeit
ruhe_ende  = datetime.time(6, 30, 0)  # Ende Uhrzeit


def Klingeln():
    """ Ansteuern der Klingel nach Tastendruck """
    GPIO.output(Relais, GPIO.HIGH)
    os.system('mpg321 Klingelton_Trompete_Attacke.mp3')
    GPIO.output(Relais, GPIO.LOW)


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def checkNachtruhe():
    return time_in_range(ruhe_start, ruhe_ende, datetime.datetime.now().time())


while True:
    taster_use = GPIO.input(Taster_Haustuer_oben)
    print strftime("%Y-%m-%d %H:%M:%S", gmtime()), taster_use, checkNachtruhe()
    if taster_use == True:
        Klingeln()
    time.sleep(0.2)

