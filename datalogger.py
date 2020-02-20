import sys
sys.path.append('..')
import os
from datetime import datetime

class datalogger():
    def __init__(self, file_name, data_root):
        #Making directory
        tm = datetime.now()
        data_root_full = data_root + str(tm.year) + format(tm.month, '02d') + format(tm.day, '02d') + \
                           format(tm.hour, '02d') + format(tm.minute, '02d') + format(tm.second, '02d')
        if not os.path.exists(data_root_full):
                print("Creating data directory: ",data_root_full)
                os.makedirs(data_root_full)
        
        #Creating file
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
