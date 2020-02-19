import sys
sys.path.append('..')
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils
from imutils.video import FPS
import time
from datetime import datetime
from threading import *
import wiringpi as wpi
import os
import tables
from configparser import ConfigParser
import csv

class pi_video_stream:
    def init(self):
        # Read config file
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'
        res = list(map(int, config.get(cfg, 'resolution').split(', ')))
        fr = int(config.get(cfg, 'framerate'))
        iso = int(config.get(cfg, 'iso'))
        sensormode = int(config.get(cfg, 'sensor_mode'))
        
        self.data_root   = config.get(cfg, 'data_root')
        self.image_stream_filename = config.get(cfg, 'raw_image_file')
        self.record_time_sec = int(config.get(cfg, 'record_time_sec'))
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = res
        self.camera.framerate = fr
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1,1)
        #camera.exposure_mode ='off'
        self.camera.shutter_speed = 30000
        self.camera.iso = iso
        self.camera.sensor_mode = sensormode
        self.rawCapture = PiRGBArray(self.camera, size=res)
        
        self.open_log_file('test')
        # allow the camera to warmup
        time.sleep(0.1)

    def setdown(self):
        self.camera.stop_preview()
        self.vstream.close()
        self.rawCapture.close()
        self.camera.close()
        self.fps.stop()
        self.image_hdf5_file.close()
        self.logFile.close()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))


    def open_log_file(self, filename):
        logFileName = self.data_root + os.sep + "RFID_data_" + str(filename) + ".txt" 
        self.logFile = open(logFileName, 'w', encoding="utf-8")
        self.logFile.write('frame' + '\t' + 'time' + '\t\t\t\t' + 'RFID pick up' +  '\t' +  "\n")
        
        
    def record(self):
        mouse_id = input("Please enter mouse ID: ")
        
        print("Start preview\n\n")
        self.vstream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.camera.start_preview()
        
        # Get the current time and initialize the project folder
        tm = datetime.now()
        data_root_full = self.data_root + str(tm.year) + format(tm.month, '02d') + format(tm.day, '02d') + \
                           format(tm.hour, '02d') + format(tm.minute, '02d') + format(tm.second, '02d')
        if not os.path.exists(data_root_full):
                print("Creating data directory: ",data_root_full)
                os.makedirs(data_root_full)
        
        image_hdf5_path = self.data_root + os.sep + self.image_stream_filename      
        self.image_hdf5_file = tables.open_file(image_hdf5_path, mode='w')
        data_storage = self.image_hdf5_file.create_earray(self.image_hdf5_file.root, 'raw_images',
                                      tables.Atom.from_dtype(np.dtype('uint8')),
                                      shape=(0, self.camera.resolution[0], self.camera.resolution[1], 3))

        print("Start recording\n\n")

        self.fps = FPS().start()
        t_end = time.time() + self.record_time_sec
        for img in self.vstream:
            start = time.time()
            image = img.array
            self.fps.update()
            print("analog gain: ", eval(str(self.camera.analog_gain)))
            print("digital gain: ", eval(str(self.camera.digital_gain))) 

            data_storage.append(image[None])
            sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            self.logFile.write(str(self.fps._numFrames) + '\t' + sttime + '\t' + str(1) + "\n")
            
            # Flush Picamera ready for next frame
            self.rawCapture.seek(0)
            
            # Check for timeout
            if time.time() >= t_end:
                break

if __name__=="__main__":
    pd = pi_video_stream()
    pd.init()
    pd.record()
    pd.setdown()

