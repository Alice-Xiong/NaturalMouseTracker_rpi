import sys
sys.path.append('..')
import os
from datetime import datetime

class datalogger():
    def __init__(self, file_name, data_root):
        logFileName = data_root + os.sep + "RFID_data_" + str(file_name) + ".txt" 
        self.logFile = open(logFileName, 'w', encoding="utf-8")
        self.logFile.write('Frame' + '\t' + 'Time' + '\t\t\t\t\t\t' + 'RFID pick up' +  '\t' +  "\n")        

    def write_to_txt(self, numFrames, RFID_pick_up):
        sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.logFile.write(str(numFrames) + '\t\t' + sttime + '\t' + str(RFID_pick_up) + "\n")

    def setdown(self):
        self.logFile.close()


def hardwareTest():
    dl = datalogger('X', '/home/pi/rpi_utils')
    dl.write_to_txt(1, 1)
    dl.setdown()
