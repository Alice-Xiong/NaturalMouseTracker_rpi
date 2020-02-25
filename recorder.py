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
        self.last_frame_count = 0

        # Object for RFID reading
        self.reader0 = RFID_reader('/dev/ttyUSB0', '0', self.data_path)
        self.reader1 = RFID_reader('/dev/ttyUSB1', '1', self.data_path)
        self.reader2 = RFID_reader('/dev/ttyUSB2', '2', self.data_path)
        self.reader3 = RFID_reader('/dev/ttyUSB3', '3', self.data_path)
    
    '''
    Main function that opens threads and runs the camera in main thread
    In each thread: rfid calls datalogger, data is only recorded when there is a pick up.
    ''' 
    def run(self):
        # Setting reference time
        self.video.record_prep()
        self.end_time = time.time() + int(self.record_time_sec)
        
        # Make threads for different objects
        #t_datalogging = Thread(target=self.datalogging_handler, args={self.end_time}, daemon=True)
        t_rfid0 = Thread(target=self.reader0.scan, daemon=True)
        t_rfid1 = Thread(target=self.reader1.scan, daemon=True)
        t_rfid2 = Thread(target=self.reader2.scan, daemon=True)
        t_rfid3 = Thread(target=self.reader3.scan, daemon=True)

        # Start threads
        #t_datalogging.start()
        t_rfid0.start()
        t_rfid1.start()
        t_rfid2.start()
        t_rfid3.start()
        self.video.record(self.end_time)


    def setdown(self):
        self.video.setdown()
        self.reader0.setdown()
        self.reader1.setdown()
        self.reader2.setdown()
        self.reader3.setdown()


rc = recorder()
rc.run()
rc.setdown()

fc.get_video_frame_count(rc.data_path)
fc.get_txt_frame_count(rc.data_path)
