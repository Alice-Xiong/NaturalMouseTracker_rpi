from smbus import SMBus
import os
import sys
import time
import signal
from datetime import datetime

from RFIDTagReader.RFIDTagReader import TagReader
import pi_video_stream
from datalogger import datalogger

class RFID_reader():
    def __init__(self, pin, ID, data_path=None):
        """Constructor for a USB RFID reader-based RFID module.
        
        :param pin: RFID port number, usually a USB port
        :type pin: string
        :param ID: label to the RFID
        :type ID: string
        :param data_path: path to store the RFID reading information, defaults to None
        :type data_path: string
        """
        self.reader = TagReader (pin, doChecksum = True, timeOutSecs = None, kind='ID')
        self.data = 0
        self.ID = ID
        if data_path is not None:
            self.datalogger = datalogger(self.ID, data_path)


    def scan(self):
        """Scans the RFID reader and if any mice is detected, log the tag with the :class: 'datalogger' object
        """
        while True:
            try:
                self.data = 0
                # Caution! This method blocks if no tag is read. 
                self.data = self.reader.readTag()
                if self.data > 0:
                    print("got data on reader "+ str(self.ID))
                    print("added tag " + str(self.data) + " at time " + str(datetime.now()))
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

