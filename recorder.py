from threading import *
import time
from datetime import datetime
import wiringpi as wpi
import os
import sys
sys.path.append('..')
from pi_video_stream import pi_video_stream
from RFID_reader import RFID_reader
from datalogger import datalogger
from configparser import ConfigParser

class recorder():
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'
        self.data_root  = config.get(cfg, 'data_root')

        # Object for recording
        self.video = pi_video_stream()
        self.frame_count = 0

        # TODO: threads
        self.datalogger0 = datalogger('0', self.data_root)
        self.reader0 = RFID_reader('/dev/ttyUSB0', '0')
        #self.reader1 = RFID_reader('/dev/ttyUSB1', '1')
        #self.reader2 = RFID_reader('/dev/ttyUSB2', '2')
        #self.reader3 = RFID_reader('/dev/ttyUSB3', '3')
                        
        
    def run(self):
        t_end = time.time() + 15
        self.video.record_prep()
        while True:
            frame_count = self.video.record()
            rfid_pickup0 = self.reader0.scan()
            self.datalogger.write_to_log_file(frame_count, rfid_pickup0)
            # Check for timeout
            if time.time() >= t_end:
                break
            


rc = recorder()
rc.run()

'''
def record():
    global frameCount, goodEvent, badEvent
    goodEvent = threading.Event()
    badEvent = threading.Event()

    #Pi video sttream object    Pi
    folder = "/mnt/frameData/" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    video = folder + "/tracking_system" + trialName + ".h264"

    # os.mkdir(folder)
    # os.system("sudo rm /home/pi/tmp.txt")
    # os.system("sudo touch /home/pi/tmp.txt")
    #Actual stuff starts here
    # os.system("sudo raspivid -t 0 -w 912 -h 720 -fps 15 -ex off -o " + video + " -pts /home/pi/tmp.txt &")
    vs = PiVideoStream(trialName=trialName)
    with open (vs.folder + "/RTS_test.txt" , "w") as f:
        startTime = time.time()
 #THreading start stuff
        thread0 = threading.Thread(target=scan, daemon= True, args=(reader0, vs, 0,))
        thread1 = threading.Thread(target=scan, daemon= True, args=(reader1, vs, 1,))
        thread2 = threading.Thread(target=scan, daemon= True, args=(reader2, vs, 2,))
        thread3 = threading.Thread(target=scan, daemon= True, args=(reader3, vs, 3,))
        thread0.start()
        thread1.start()
        thread2.start()
        thread3.start()
        vs.start(goodEvent, badEvent)
        #Override interrupt with stop Handler, all child processes ignore interrupt
        signal.signal(signal.SIGINT, stopHandler)
        while True:
            time.sleep(0.05)
            if not thread0.is_alive():
                thread0 = threading.Thread(target=scan, daemon= True, args=(reader0, vs, 0))
                thread0.start()
            if not thread1.is_alive():
                thread1 = threading.Thread(target=scan, daemon= True, args=(reader1, vs, 1))
                thread1.start()
            if not thread2.is_alive():
                thread2 = threading.Thread(target=scan, daemon= True, args=(reader2, vs, 2))
                thread2.start()
            if not thread3.is_alive():
                thread3 = threading.Thread(target=scan, daemon= True, args=(reader3, vs, 3))
                thread3.start()
            if goodEvent.isSet():
                print('caught event')
#                vs.frames.join()
                print("done")
                sys.exit(0)
               # os.system("sudo kill -s 2 $(pgrep raspivid)")
                break
            if badEvent.isSet():
                print("frame queue full")
                print("done")
                sys.exit(1)
                break
                
'''