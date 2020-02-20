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
from configparser import ConfigParser
import wiringpi as wpi
import os
import tables
import csv

class pi_video_stream():
    def __init__(self):
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
        
        self.save_hdf5 = False
        # allow the camera to warmup
        time.sleep(0.1)

    def setdown(self):
        self.camera.stop_preview()
        self.vstream.close()
        self.rawCapture.close()
        self.camera.close()
        self.fps.stop()
        self.image_hdf5_file.close()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))

    def get_frame_count(self):
        return self.fps._numFrames
        
        
    def record_prep(self):
        #Deprecated, was using hdf5 but it took too much memory
        if self.save_hdf5:
            image_hdf5_path = self.data_root + os.sep + self.image_stream_filename      
            self.image_hdf5_file = tables.open_file(image_hdf5_path, mode='w')
            self.data_storage = self.image_hdf5_file.create_earray(self.image_hdf5_file.root, 'raw_images',
                                                                  tables.Atom.from_dtype(np.dtype('uint8')),
                                                                  shape=(0, self.camera.resolution[0], self.camera.resolution[1], 3))
                
        #Starting camera and preview
        print("Start preview\n\n")
        self.vstream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.camera.start_preview()
        self.fps = FPS().start()
        print("Start recording\n\n")
        
        
    def record(self):
        while True:
            # update the fps count
            self.fps.update()
             
            # Flush Picamera ready for next frame
            self.rawCapture.seek(0)

        

