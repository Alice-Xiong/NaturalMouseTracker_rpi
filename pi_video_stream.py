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
import io

frame_count = 0
last_frame_count = 0

class pi_video_stream():
    def __init__(self, data_path):
        # Read config file
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'
        res = list(map(int, config.get(cfg, 'resolution').split(', ')))
        fr = int(config.get(cfg, 'framerate'))
        iso = int(config.get(cfg, 'iso'))
        sensormode = int(config.get(cfg, 'sensor_mode'))
        
        self.data_path = data_path
        self.record_time_sec = int(config.get(cfg, 'record_time_sec'))

        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = res
        self.camera.framerate = fr
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1,1)
        # Camera.exposure_mode ='off'
        self.camera.shutter_speed = 30000
        self.camera.iso = iso
        self.camera.sensor_mode = sensormode
        self.rawCapture = PiRGBArray(self.camera, size=res)

        # allow the camera to warmup
        time.sleep(0.1)

    def setdown(self):
        self.out.release()
        self.camera.stop_preview()  
        self.fps.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
        
        
    def record_prep(self):
        # Starting camera and preview
        self.vstream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.camera.start_preview(fullscreen=False, window=(0,0,256,256))
        self.fps = FPS().start()
        self.out = cv2.VideoWriter(self.data_path + os.sep + 'frame.avi', cv2.VideoWriter_fourcc(*'DIVX'), self.camera.framerate, self.camera.resolution)
        print("Start recording\n\n")
        
        
    def record(self, end_time=None):
        # Capturing frame by frame
        for img in self.vstream:
            # Update frame count
            global frame_count, last_frame_count
            last_frame_count = frame_count
            self.fps.update()
            frame_count = self.fps._numFrames

            # Save individual frames
            #cv2.imwrite(self.data_path + os.sep + 'frame' + str(frame_count) + '.jpg', img.array)
            # Write to video
            self.out.write(img.array)
            self.rawCapture.seek(0)

            if end_time is not None and time.time() > end_time:
                break


if __name__=="__main__":       
    pc = pi_video_stream('/home/pi/rpi_utils/')
    pc.record_prep()
    end_time = time.time() + 10
    pc.record(end_time)
    pc.setdown()
    
            
        
       


        

