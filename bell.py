#!/usr/env/bin python
import datetime
import os
import sys
import time
from time import gmtime, strftime
import platform
import tomllib
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


with open(_config_file, 'rb') as f:
    config = tomllib.load(f)

mp3_file_name = config['bell'].get('mp3_file_name')
log2log = config['bell'].get('logger')

logging.config.fileConfig(_config_logger)
logger = logging.getLogger('bell')
logger.propagate = False


def log_message(message):
    if log2log == "True":
        logger.info(message)
    else:
        print(message)


log_message("+-----  S T A R T  ----------------------------------")
log_message("|   %r" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
log_message("+----------------------------------------------------")

# Relais_x = 23
# Relais_y = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setwarnings(True)

relais_oben = 8
relais_unten = 25

GPIO.setup(relais_oben, GPIO.OUT)
GPIO.setup(relais_unten, GPIO.OUT)
GPIO.output(relais_oben, GPIO.LOW)
GPIO.output(relais_unten, GPIO.LOW)

# .
# G
# P  oo => taster_vorne
# I  oo => taster_haustuer_unten
# O  oo => taster_haustuer_oben
# .

taster_vorne = 18
taster_haustuer_unten = 15
taster_haustuer_oben = 14

GPIO.setup(taster_haustuer_oben, GPIO.IN)
GPIO.setup(taster_haustuer_unten, GPIO.IN)
GPIO.setup(taster_vorne, GPIO.IN)

# if you want to shut down the bell at night
# adjust your time frame here:
ruhe_start = datetime.time(22, 30, 0) # Start Time
ruhe_ende  = datetime.time(6, 30, 0)  # End Time

mp3_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ringtones', mp3_file_name)


def play_sound(relais):
    """ please play the mp3 """
    log_message("playing file: %s" % mp3_file)

    # first switch power on to amplifier
    GPIO.output(relais, GPIO.HIGH)  # switch base of bc 550c
    os.system('mpg321 '+mp3_file )  # play sound
    # switch off power to amplifier
    GPIO.output(relais, GPIO.LOW)   # switch off again


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def check_sleep():
    return time_in_range(ruhe_start, ruhe_ende, datetime.datetime.now().time())


def main():
    while True:
        taster_use = [GPIO.input(taster_haustuer_unten),
                      GPIO.input(taster_haustuer_oben),
                      GPIO.input(taster_vorne),
                      ]
        # debug output

        if 1 in taster_use:
            log_message("+----------------------------------------------------")
            log_message("|   %r" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            log_message("|   checkSleeping Time:   %r" % check_sleep())
            log_message("|   taster_haustuer_unten %r" % taster_use[0])
            log_message("|   taster_haustuer_oben  %r" % taster_use[1])
            log_message("|   taster_vorne          %r" % taster_use[2])
            log_message("+----------------------------------------------------")
            play_sound(relais_unten)
            play_sound(relais_oben)
        time.sleep(0.2)


if __name__ == '__main__':
    main()