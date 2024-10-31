# MP3 Bell with Raspberry Pi

* download one or more mp3 files of your choice to the directory ringtones (will played completely)
* don't forget to "chmod 755 belly.py" so that the programm is executable

To run the program as a "deamon", I decided to use 
supervisor http://supervisord.org. The advantages are awesome: 

* supervisord will start the program automatically - also after reboot 
* take care of restart, if the script exited unexpected!


# GpIO
- gpio 25 Relais 1: rings the bell first flor
- gpio 08 Relais 2: rings the bell second flor
- gpio 23 Relais "heating system" see project raspberry-pi-heizung
- gpio 24 ?
- gpio 14 push button 1: for second flor
- gpio 15 push button 2: for first flor
- gpio 16 push button 3: for entrance to the property


# Acknowledgment

Thanks to Erik Bartmann for his inspiring Book "Die elektronische Welt mit Raspberry Pi entdecken"

