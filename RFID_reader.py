#Imports
from smbus import SMBus
import os
import sys
import time
import signal
from datetime import datetime
from RFIDTagReader.RFIDTagReader import TagReader

'''
RFID reader module used for USB based RFID readers
'''


class RFID_reader():
    
    '''
    Makes a TagReader object
    '''
    def __init__(self, pin, ID):
        RFID_kind = 'ID'
        RFID_doCheckSum = True
        self.reader = TagReader (pin, RFID_doCheckSum, timeOutSecs = None, kind=RFID_kind)
        self.ID = ID
        self.data = 0
    
    """
    Scans all readers based on their position in the map.
    If any mice detected, save and return their tag
    """
    def scan(self):
        while True:
            try:
                print("startedWait")
                self.data = 0
                self.data = self.reader.readTag()
                if self.data > 0:
                    print("got data on reader "+ str(self.ID))
                    print("added tag " + str(self.data))
                    print(datetime.now())
                    #Allow this read to be picked up by outside classes
                    time.sleep(0.1)
            except Exception as e:
                print(str(e))

                
     
    '''
    Return a string to identify the RFID reader
    '''
    def get_id(self):
         return self.ID
        

'''
Testing code
'''
if __name__=="__main__":
    #Testing code
    print("running RFID scanner, ctrl+C to quit")
    reader0 = RFID_reader('/dev/ttyUSB0', 'A')
    reader0.scan()
    # Check for timeout

