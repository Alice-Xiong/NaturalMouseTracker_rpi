#Imports
from smbus import SMBus
import os
import sys
import time
import signal
import RPi.GPIO as GPIO
import datetime
from random import shuffle
import argparse
from RFIDTagReader.RFIDTagReader import TagReader
from shutil import copyfile

#Reader stuff
##readerMap = [
##    (103, 170), (177, 160), (274, 145), (390, 140), (475, 138), (542, 145), #1-(1-6) [y-x]
##    (105, 253), (183, 250), (278, 248), (393, 237), (487, 235), (550, 230), #2-(1-6) [y-x]
##    (118, 330), (190, 336), (288, 332), (401, 326), (496, 320), (556, 305)  #3-(1-5) [y-x]
##]
#readerMap = [(100, 100),(550, 350), (100, 350), (550, 100)]
seenTags = []
#Hex I2C Addresses of all ProTrinkets
'''
ProT [0] = 0x11
ProT [1] = 0x12
ProT [2] = 0x13
ProT [3] = 0x14
ProT [4] = 0x15
ProT [5] = 0x16
ProT [6] = 0x31
ProT [7] = 0x32
ProT [8] = 0x33
ProT [9] = 0x34
ProT [10] = 0x35
ProT [11] = 0x36
ProT [12] = 0x51
'''


class RFID_scanner():
    
    def __init__(self, pin):
        RFID_kind = 'ID'
        RFID_doCheckSum = True
        self.reader = TagReader (RFID_doCheckSum, timeOutSecs = None, kind=RFID_kind)
    
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
    If any mice detected, save their tag and position with the frame number.
    """
    frameCount = 0

    def scan(self, reader, f, readerNum):
        global frameCount, startTime
        mice = []
        try:
            print("startedWait")
            Data = reader.readTag()
            if f is not False and Data > 0:
                print("got data")
                if Data not in seenTags:
                    seenTags.append(Data)
                print("added tag")
                try:
                    f.camera.annotate_text = str(seenTags.index(Data)) + str(readerNum)
                except PiCameraValueError as e:
                    print(str(e))
                print("modded text")
                f.camera.annotate_text_size = 16
                time.sleep(0.1)
                f.camera.annotate_text = ""
                print("pickup")
        except Exception as e:
            print(str(e))
        finally:
            return



while True:
    reader0 = RFID_scanner('/dev/ttyUSB0')
    reader0.scan()
    # Check for timeout
    t_end = time.time() + 10
    if time.time() >= t_end:
        break

