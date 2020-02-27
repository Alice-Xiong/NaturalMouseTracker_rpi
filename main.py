import time
from datetime import datetime
import os
import sys
import signal

sys.path.append('..')
from pi_video_stream import pi_video_stream
from RFID_reader import RFID_reader
from configparser import ConfigParser
from threading import Thread
import frame_counter as fc
from datalogger import datalogger


class rpi_recorder():
    """:class: 'rpi_recorder' is the top level class of natural mouse tracker. It creates :class: 'RFID_reader' objects
    which run in separate threads, and also runs camera recording in the main loop. User config files can be found in 
    'config.ini'
    """

    def __init__(self):
        """Constructor for :class: 'recorder'. Loads the config file 'config.ini' and creates a :class:'pi_video_stream' 
        object and four :class:'RFID_reader' objects.
        """
        # Load configs
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'

        # Making directory
        self.data_root = config.get(cfg, 'data_root')
        tm = datetime.now()
        self.data_path = self.data_root + str(tm.year) + "_" + format(tm.month, '02d') + '_' + format(tm.day, '02d') + \
            '_' + format(tm.hour, '02d') + ':' + format(tm.minute, '02d') + ':' + format(tm.second, '02d')

        # Object and settings for recording
        self.video = pi_video_stream(self.data_path, self)
        self.user_interrupt_only = config.get(cfg, 'user_interrupt_only')
        if self.user_interrupt_only == "True":
            self.record_time_sec = None        
        else:
            self.record_time_sec = int(config.get(cfg, 'record_time_sec'))
        self.fps_post_process = config.get(cfg, 'fps_post_process')

        # Object for RFID reading
        self.reader0 = RFID_reader('/dev/ttyUSB0', '0')
        self.reader1 = RFID_reader('/dev/ttyUSB1', '1')
        self.reader2 = RFID_reader('/dev/ttyUSB2', '2')
        self.reader3 = RFID_reader('/dev/ttyUSB3', '3')

    def run(self):
        """Main function that opens threads and runs :class: 'pi_video_stream' in main thread. In each thread,
         :class:'RFID_reader' checks for RFID pickup. The pickup data is then logged to a text file 
         by :class: 'pi_video_stream'.
        """
        # Make threads for different objects
        t_rfid0 = Thread(target=self.reader0.scan, daemon=True)
        t_rfid1 = Thread(target=self.reader1.scan, daemon=True)
        t_rfid2 = Thread(target=self.reader2.scan, daemon=True)
        t_rfid3 = Thread(target=self.reader3.scan, daemon=True)

        # Start threads
        t_rfid0.start()
        t_rfid1.start()
        t_rfid2.start()
        t_rfid3.start()

        # keyboard interrupt handler, stops program once ctrl-c is pressed
        def keyboardInterruptHandler(signal, frame):
            self.setdown()
            exit(0)
        signal.signal(signal.SIGINT, keyboardInterruptHandler)

        # Start recording
        self.video.record(self.record_time_sec)
        

    def setdown(self):
        """Shuts down the :class:'pi_video_stream' object and :class:'RFID_reader' objects. 
        Note that this method has to execute for the video and txt files to save properly.
        """
        self.video.setdown()

        # Displays the fps and frame counts on terminal
        fc.get_video_frame_count(rc.data_path)
        fc.get_txt_frame_count(rc.data_path)

        # Post process the video to match FPS if specified by user
        if self.fps_post_process == "True":
            self.video.post_process(self.video.fps.fps())
            print("Finished post processing at "+str(datetime.now()))


if __name__ == "__main__":
    rc = rpi_recorder()
    rc.run()
    print("Finished recording at "+str(datetime.now()))
    rc.setdown()
    
