import time
from datetime import datetime
import os
import sys

sys.path.append('..')
from pi_video_stream import pi_video_stream
from RFID_reader import RFID_reader
from configparser import ConfigParser
from threading import Thread
import frame_counter as fc


class rpi_recorder():
    """:class: 'rpi_recorder' is the top level class of natural mouse tracker. It creates :class: 'RFID_reader' objects
    which run in separate threads, and also runs camera recording in the main loop. Each RFID reader then logs its
    data in a text file.

    Note that camera is very slow if placed in a thread. (Benchmark: 20 fps in main loop, 11 fps in a thread)
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
        self.video = pi_video_stream(self.data_path)
        self.record_time_sec = int(config.get(cfg, 'record_time_sec'))
        self.frame_count = 0
        self.last_frame_count = 0

        # Object for RFID reading
        self.reader0 = RFID_reader('/dev/ttyUSB0', '0', self.data_path)
        self.reader1 = RFID_reader('/dev/ttyUSB1', '1', self.data_path)
        self.reader2 = RFID_reader('/dev/ttyUSB2', '2', self.data_path)
        self.reader3 = RFID_reader('/dev/ttyUSB3', '3', self.data_path)

    def run(self):
        """Main function that opens threads and runs the camera in main thread. In each thread,
         :class:'RFID_reader' calls :class:'datalogger', data is only recorded when there is an RFID pickup.
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
        self.video.record(self.record_time_sec)

    def setdown(self):
        """Shuts down the :class:'pi_video_stream' object and :class:'RFID_reader' objects. 
        Note that this method has to execute for the video and txt files to save properly.
        """
        self.video.setdown()
        self.reader0.setdown()
        self.reader1.setdown()
        self.reader2.setdown()
        self.reader3.setdown()


if __name__ == "__main__":
    rc = rpi_recorder()
    rc.run()
    rc.setdown()

    # Displays the fps and frame counts on terminal
    fc.get_video_frame_count(rc.data_path)
    fc.get_txt_frame_count(rc.data_path)
