import time
from datetime import datetime
import os
import sys
sys.path.append('..')
from pi_video_stream import pi_video_stream
from RFID_reader import RFID_reader
from datalogger import datalogger
from configparser import ConfigParser
from threading import Thread
import frame_counter as fc

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
        self.datalogger1 = datalogger('1', self.data_path)
        self.datalogger2 = datalogger('2', self.data_path)
        self.datalogger3 = datalogger('3', self.data_path)

        # Object for RFID reading
        self.reader0 = RFID_reader('/dev/ttyUSB0', '0')
        self.reader1 = RFID_reader('/dev/ttyUSB1', '1')
        self.reader2 = RFID_reader('/dev/ttyUSB2', '2')
        self.reader3 = RFID_reader('/dev/ttyUSB3', '3')
    
                        
        
    def run(self):
        self.video.record_prep()

        # Make threads for different objects
        t_camera = Thread(target=self.video.record, daemon=True)
        t_rfid0 = Thread(target=self.reader0.scan, daemon=True)
        t_rfid1 = Thread(target=self.reader1.scan, daemon=True)
        t_rfid2 = Thread(target=self.reader2.scan, daemon=True)
        t_rfid3 = Thread(target=self.reader3.scan, daemon=True)
        

        # Start threads
        t_camera.start()
        t_rfid0.start()
        t_rfid1.start()
        t_rfid2.start()
        t_rfid3.start()

        # Setting reference time and frame count
        t_end = time.time() + int(self.record_time_sec)
        self.frame_count = 0
        self.last_frame_count = 0

        # Main loop
        while True:
            # Ensure threads are all running
            if not t_rfid0.is_alive():
                t_rfid0 = threading.Thread(target=self.reader0.scan, daemon= True)
                t_rfid0.start()
            if not t_rfid1.is_alive():
                t_rfid1 = threading.Thread(target=self.reader0.scan, daemon= True)
                t_rfid1.start()
            if not t_rfid2.is_alive():
                t_rfid2 = threading.Thread(target=self.reader0.scan, daemon= True)
                t_rfid2.start()
            if not t_rfid3.is_alive():
                t_rfid3 = threading.Thread(target=self.reader0.scan, daemon= True)
                t_rfid3.start()

            # Log frame count and RFID pickup
            self.frame_count = self.video.get_frame_count()
            if self.frame_count != self.last_frame_count: 
                self.datalogger0.write_to_txt(self.frame_count, self.reader0.data)
                self.datalogger1.write_to_txt(self.frame_count, self.reader1.data)
                self.datalogger2.write_to_txt(self.frame_count, self.reader2.data)
                self.datalogger3.write_to_txt(self.frame_count, self.reader3.data)
                self.last_frame_count = self.frame_count

            # Check for timeout
            if time.time() >= t_end:
                break

    def setdown(self):
        self.video.setdown()
        self.datalogger0.setdown()
        self.datalogger1.setdown()
        self.datalogger2.setdown()
        self.datalogger3.setdown()
            


rc = recorder()
rc.run()
rc.setdown()

fc.get_video_frame_count(rc.data_path)
fc.get_txt_frame_count(rc.data_path)
