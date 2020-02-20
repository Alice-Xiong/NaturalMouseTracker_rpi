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
        try:
            print("startedWait")
            Data = self.reader.readTag()
            if Data > 0:
                print("got data on reader "+ str(self.ID))
                print("added tag " + str(Data))
                #self.pickup = 1
                #self.tag_read = 
                time.sleep(0.1)
        except Exception as e:
            print(str(e))
        finally:
            return Data
     
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
    print("running RFID scanner for 10 seconds")
    t_end = time.time() + 10
    reader0 = RFID_reader('/dev/ttyUSB0', 'A')
    while True:
        reader0.scan()
        # Check for timeout
        if time.time() >= t_end:
            break



if __name__=="__main__":
    hardwareTest()
    

