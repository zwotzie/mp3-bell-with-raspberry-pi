#!/usr/bin/env python3
import datetime
import os
import sys
import time
from time import gmtime, strftime
import platform
import tomllib
import logging
from logging import config

# ====================== GPIO ======================
raspberry = False
h = None

if 'raspberrypi' in platform.uname().node:
    raspberry = True
    import lgpio

# ====================== Konfiguration ======================
_config_path = os.path.abspath(os.path.dirname(sys.argv[0]))
_config_file = _config_path + "/etc/bell.conf"
_config_logger = _config_path + '/etc/logging.conf'

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
log_message(f"|   {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
log_message("+----------------------------------------------------")

# ====================== GPIO Setup ======================
if raspberry:
    relais_oben = 8
    relais_unten = 25
    taster_vorne = 18
    taster_haustuer_unten = 15
    taster_haustuer_oben = 14

    h = lgpio.gpiochip_open(0)

    # Relais als Output
    lgpio.gpio_claim_output(h, relais_oben, 0)
    lgpio.gpio_claim_output(h, relais_unten, 0)


mp3_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ringtones', mp3_file_name)


def play_sound(relais):
    log_message(f"playing file: {mp3_file}")
    if raspberry and h is not None:
        lgpio.gpio_write(h, relais, 1)
        time.sleep(0.15)

    os.system(f'mpg123 -a plughw:0,0 {mp3_file}')

    if raspberry and h is not None:
        lgpio.gpio_write(h, relais, 0)


def main():
    try:
        print("=== Klingel-Debug gestartet ===")
        while True:
            if raspberry and h is not None:
                raw_unten = lgpio.gpio_read(h, taster_haustuer_unten)
                raw_oben  = lgpio.gpio_read(h, taster_haustuer_oben)
                raw_vorne = lgpio.gpio_read(h, taster_vorne)

                # Neue Logik: 0 = NICHT gedrückt, 1 = gedrückt
                # (weil Pull-Up nicht funktioniert)
                taster_use = [raw_unten == 1, raw_oben == 1, raw_vorne == 1]

                # print(f"DEBUG Raw | Unten:{raw_unten}  Oben:{raw_oben}  Vorne:{raw_vorne}  → Klingel aktiv: {taster_use}")

            else:
                taster_use = [False, False, False]

            if True in taster_use:
                log_message("+----------------------------------------------------")
                log_message(f"|   {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
                log_message(f"|   Taster betätigt! Raw: U{raw_unten} O{raw_oben} V{raw_vorne}")
                log_message("+----------------------------------------------------")

                if not check_sleep():
                    play_sound(relais_unten)
                    play_sound(relais_oben)
                else:
                    log_message("Ruhezeit - keine Klingel")

            time.sleep(0.25)

    finally:
        if raspberry and h is not None:
            lgpio.gpiochip_close(h)


# Ruhezeiten
ruhe_start = datetime.time(22, 30, 0)
ruhe_ende  = datetime.time(6, 30, 0)

def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def check_sleep():
    return time_in_range(ruhe_start, ruhe_ende, datetime.datetime.now().time())


if __name__ == '__main__':
    main()
