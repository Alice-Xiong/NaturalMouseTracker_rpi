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
from threading import Thread

class recorder():
    def __init__(self):
        # Load configs
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'

        #Making directory
        self.data_root  = config.get(cfg, 'data_root')        
        tm = datetime.now()
        self.data_path = self.data_root + str(tm.year) + "_" + format(tm.month, '02d') + '_' + format(tm.day, '02d') + \
                           '_' + format(tm.hour, '02d') +':' + format(tm.minute, '02d') + ':' + format(tm.second, '02d')
        
        self.record_time_sec = config.get(cfg, 'record_time_sec')

        # Object for recording
        self.video = pi_video_stream(self.data_path)
        self.frame_count = 0

        # Object for datalogging
        self.datalogger0 = datalogger('0', self.data_path)

        # Object for RFID reading
        self.reader0 = RFID_reader('/dev/ttyUSB0', '0')
        #self.reader1 = RFID_reader('/dev/ttyUSB1', '1')
        #self.reader2 = RFID_reader('/dev/ttyUSB2', '2')
        #self.reader3 = RFID_reader('/dev/ttyUSB3', '3')
                        
        
    def run(self):
        self.video.record_prep()

        # Make threads for different objects
        t_camera = Thread(target=self.video.record, daemon=True)
        t_rfid0 = Thread(target=self.reader0.scan, daemon=True)

        # Start threads
        t_camera.start()
        t_rfid0.start()

        # Setting reference time and frame count
        t_end = time.time() + int(self.record_time_sec)
        self.frame_count = 0
        self.last_frame_count = 0

        # Main loop
        while True:
            self.frame_count = self.video.get_frame_count()
            if self.frame_count != self.last_frame_count: 
                self.datalogger0.write_to_txt(self.frame_count, self.reader0.data)
                self.last_frame_count = self.frame_count
            # Check for timeout
            if time.time() >= t_end:
                break

    def setdown(self):
        self.pi_video_stream.setdown()
            


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