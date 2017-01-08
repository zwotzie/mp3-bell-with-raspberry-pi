# MP3 Bell with Raspberry Pi

* download one or more mp3 files of your choice to the directory ringtones (will played completely)
* don't forget to "chmod 755 belly.py" so that the programm is executable

To run the program as a "deamon", I decided to use 
supervisor http://supervisord.org. The advantages are awesome: 

* supervisord will start the program automatically - also after reboot 
* take care of restart, if the script exited unexpected!

# Acknowledgment

Thanks to Erik Bartmann for his inspiring Book "Die elektronische Welt mit Raspberry Pi entdecken"
