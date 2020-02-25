import sys
sys.path.append('..')
import os
import time
from datetime import datetime

'''
Makes and writes to txt file
'''
class datalogger():
    def __init__(self, file_name, data_path):        
        if not os.path.exists(data_path):
                print("Creating data directory: ",data_path)
                os.makedirs(data_path)
        
        #Creating file
        logFileName = data_path + os.sep + "RFID_data_" + str(file_name) + ".txt" 
        self.logFile = open(logFileName, 'w', encoding="utf-8")
        self.logFile.write('Frame' + '\t' + 'Time' + '\t\t\t\t\t\t' + 'RFID pick up' +  '\t' +  "\n")        

    def write_to_txt(self, numFrames, RFID_pick_up):
        sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.logFile.write(str(numFrames) + '\t\t' + sttime + '\t' + str(RFID_pick_up) + "\n")

    def setdown(self):
        self.logFile.close()


'''
Testing code
'''
if __name__=="__main__":
    dl = datalogger('X', '/home/pi/rpi_utils')
    for i in range(200):
        dl.write_to_txt(i, time.time())
    dl.setdown()
