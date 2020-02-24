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
    Gets the last full tag in the ProTrinket serial buffer.
    Converts this into a readable string.
    """
    def readNumber(self, address_1):
        number1 = []
        try:
            #with SMBus(1) as bus:
            bus = SMBus(1)
            flag = False
            for i in range (0, 16):
                if flag:
                    number1.append(chr(bus.read_byte(address_1)))
                else:
                    x = bus.read_byte(address_1)
                    if x is 2:
                        flag = True

        except IOError as e:
            print (e)
        return number1,time.time()
    
    
    """
    Scans all readers based on their position in the map.
    If any mice detected, save and return their tag
    """
    def scan(self):
        while True:
            try:
                print("startedWait")
                Data = 0
                Data = self.reader.readTag()
                self.data = Data
                if Data > 0:
                    print("got data on reader "+ str(self.ID))
                    print("added tag " + str(Data))
                    print(datetime.now())
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
def hardwareTest():
    #Testing code
    print("running RFID scanner, ctrl+C to quit")
    reader0 = RFID_reader('/dev/ttyUSB0', 'A')
    reader0.scan()
    # Check for timeout


if __name__=="__main__":
    hardwareTest()
    

