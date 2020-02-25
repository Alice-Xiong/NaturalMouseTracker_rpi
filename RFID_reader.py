#Imports
from smbus import SMBus
import os
import sys
import time
import signal
from datetime import datetime
from RFIDTagReader.RFIDTagReader import TagReader
import pi_video_stream
from datalogger import datalogger

'''
RFID reader module used for USB based RFID readers
'''
class RFID_reader():
    
    '''
    Makes a TagReader object
    '''
    def __init__(self, pin, ID, data_path):
        self.reader = TagReader (pin, doChecksum = True, timeOutSecs = None, kind='ID')
        self.data = 0
        self.ID = ID
        self.datalogger = datalogger(self.ID, data_path)

    
    """
    Scans the reader
    If any mice detected, save and return their tag
    Also writes to log file
    """
    def scan(self):
        while True:
            try:
                self.data = 0
                self.data = self.reader.readTag()
                if self.data > 0:
                    print("got data on reader "+ str(self.ID))
                    print("added tag " + str(self.data))
                    print(datetime.now())
                    self.datalogger.write_to_txt(pi_video_stream.frame_count, self.data)
            except Exception as e:
                print(str(e))
                
    def setdown(self):
        self.datalogger.setdown()

'''
Testing code
'''
if __name__=="__main__":
    #Testing code
    print("running RFID scanner, ctrl+C to quit")
    reader0 = RFID_reader('/dev/ttyUSB0', 'A')
    reader0.scan()
    # Check for timeout

