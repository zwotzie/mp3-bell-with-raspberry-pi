#!/usr/bin/python
import datetime
import os
import sys
import time
from time import gmtime, strftime
import platform
from ConfigParser import SafeConfigParser
import logging
from logging import config

raspberry = False
if 'raspberrypi' in platform.uname():
    # global raspberry
    raspberry = True
    import RPi.GPIO as GPIO

# Set up a specific logger with our desired output level
_config_path = os.path.abspath(os.path.dirname(sys.argv[0]))
_config_file = _config_path + "/etc/bell.conf"
_config_logger = _config_path+'/etc/logging.conf'

parser = SafeConfigParser()
parser.read(_config_file)
log2log = parser.get('bell', 'logger')

logging.config.fileConfig(_config_logger)
logger = logging.getLogger('bell')
logger.propagate = False


def logmessage(message):
    if log2log == "True":
        logger.info(message)
    else:
        print message

# Relais_x = 23
# Relais_y = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setwarnings(True)

Relais_oben = 8
Relais_unten = 25
GPIO.setup(Relais_oben,   GPIO.OUT)
GPIO.setup(Relais_unten,  GPIO.OUT)
GPIO.output(Relais_oben,  GPIO.LOW)
GPIO.output(Relais_unten, GPIO.LOW)

# .
# G
# P  oo => Taster_vorne
# I  oo => Taster_Haustuer_unten
# O  oo => Taster_Haustuer_oben
# .

Taster_vorne = 14
Taster_Haustuer_unten = 15
Taster_Haustuer_oben = 18
GPIO.setup(Taster_Haustuer_oben,  GPIO.IN)
GPIO.setup(Taster_Haustuer_unten, GPIO.IN)
GPIO.setup(Taster_vorne,          GPIO.IN)

# if you want to shut down the bell at night
# adjust your time frame here:
ruhe_start = datetime.time(22, 30, 0) # Start Time
ruhe_ende  = datetime.time(6, 30, 0)  # End Time

mp3_file_name = "Klingelton_Trompete_Attacke.mp3"
mp3_file_name = "Kuckucksuhr.mp3"
mp3_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ringtones', mp3_file_name)


def PlaySound():
    """ please play the mp3 """
    # first switch power on to amplifier
    GPIO.output(Relais_unten, GPIO.HIGH)  # switch base of bc 550c
    # play sound
    os.system('mpg321 '+mp3_file )
    # switch off power to amplifier
    GPIO.output(Relais_unten, GPIO.LOW)   # switch off again

    GPIO.output(Relais_oben,  GPIO.HIGH)  # switch base of bc 550c
    # play sound
    os.system('mpg321 '+mp3_file )
    # switch off power to amplifier
    GPIO.output(Relais_oben,  GPIO.LOW)   # switch off again


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def checkSleep():
    return time_in_range(ruhe_start, ruhe_ende, datetime.datetime.now().time())


def main():
    while True:
        taster_use = [GPIO.input(Taster_Haustuer_unten),
                      GPIO.input(Taster_Haustuer_oben),
                      GPIO.input(Taster_vorne),
                      ]
        # debug output

        if 1 in taster_use:
            logmessage("+----------------------------------------------------")
            logmessage("|   ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            logmessage("|   checkSleeping Time:   ", checkSleep())
            logmessage("|   Taster_Haustuer_unten ", taster_use[0])
            logmessage("|   Taster_Haustuer_oben  ", taster_use[0])
            logmessage("|   Taster_vorne          ", taster_use[0])
            logmessage("+----------------------------------------------------")
            PlaySound()
        time.sleep(0.2)


if __name__ == '__main__':
    main()