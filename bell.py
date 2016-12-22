#!/usr/bin/python
import datetime
import os
import time
from time import gmtime, strftime

import RPi.GPIO as GPIO

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

# if you want to shut down the bell at night
# adjust your time frame here:
ruhe_start = datetime.time(22, 30, 0) # Start Time
ruhe_ende  = datetime.time(6, 30, 0)  # End Time

mp3_file = "Klingelton_Trompete_Attacke.mp3"


def PlaySound():
    """ pleae play the mp3 """
    GPIO.output(Relais, GPIO.HIGH)  # switch base of bc 550c
    os.system('mpg321 '+mp3_file )
    GPIO.output(Relais, GPIO.LOW)   # switch off again


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def checkSleep():
    return time_in_range(ruhe_start, ruhe_ende, datetime.datetime.now().time())


while True:
    taster_use = GPIO.input(Taster_Haustuer_oben)
    # debug output
    print strftime("%Y-%m-%d %H:%M:%S", gmtime()), taster_use, checkSleep()

    if taster_use is True:
        PlaySound()
    time.sleep(0.2)

