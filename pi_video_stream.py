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

from datalogger import datalogger

class pi_video_stream():
    def __init__(self, data_path, recorder):
        """Constructor for :class: 'pi_video_stream' object. Creates a :class: 'PiCamera' object and loads the settings
        from 'config.ini' for camera. 
        
        :param data_path: path to and name of the folder where video(s) will be saved
        :type data_path: string
        :param recorder: recorder object; contains information of RFID readers
        :type recorder: :class: 'recorder' object
        """
        # Read config file
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'
        
        # Set up text file and paths
        self.data_path = data_path
        self.datalogger = datalogger('all', self.data_path)
        self.rc = recorder

        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = list(map(int, config.get(cfg, 'resolution').split(', ')))
        self.camera.framerate = int(config.get(cfg, 'framerate'))
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1,1)
        self.camera.shutter_speed = 30000
        self.camera.iso = int(config.get(cfg, 'iso'))
        self.camera.sensor_mode = int(config.get(cfg, 'sensor_mode'))
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.record_time_sec = int(config.get(cfg, 'record_time_sec'))
        self.capture_frames = bool(config.get(cfg, 'capture_frames'))

        # Allow the camera to warmup
        time.sleep(0.1)

    def setdown(self):
        """Saves the recording and text file, stops camera preview, and display time and FPS on terminal.
        """
        self.datalogger.setdown()
        self.out.release()
        self.camera.stop_preview()  
        self.fps.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))

    def post_process(self, fps):
        """Takes the 'raw.avi' video and produces a new video 'fps_corrected.avi' such that the latter video 
        has the specified FPS
        
        :param fps: frame rate (frames per second) to be matched towards
        :type fps: integer
        """
        # Post processing to match FPS
        self.out = cv2.VideoWriter(self.data_path + os.sep + 'fps_corrected.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, self.camera.resolution)
        cap = cv2.VideoCapture(self.data_path + os.sep + 'raw.avi')
        while cap.isOpened():
            # Copy each frame of video and then rearrange with correct FPS
            ret, frame = cap.read()
            self.out.write(frame)
            if ret == False:
                break
        cap.release()
        self.out.release()
        
        
    def record(self, duration=None):
        """Starts a video stream that captures frame by frame and compiles into a video. Also writes the frame count,
        time stamp, and RFID readings into a text file.
        
        :param duration: time of record duration in seconds, defaults to None
        :type duration: integer, optional
        """
        # Starting camera, FPS and preview
        self.vstream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.camera.start_preview(fullscreen=False, window=(0,0,256,256))
        self.fps = FPS().start()
        self.out = cv2.VideoWriter(self.data_path + os.sep + 'raw.avi', cv2.VideoWriter_fourcc(*'DIVX'), self.camera.framerate, self.camera.resolution)
        print("Start recording\n\n")

        if duration is not None:
            end_time = time.time() + duration

        # Capturing frame by frame
        for img in self.vstream:
            # Update frame count
            self.fps.update()

            # Save individual frames
            if self.capture_frames:
                cv2.imwrite(self.data_path + os.sep + 'frame' + str(self.fps._numFrames) + '.jpg', img.array)
            # Write to video
            self.out.write(img.array)
            self.rawCapture.seek(0)

            #Save data to log file
            self.datalogger.write_to_txt(self.fps._numFrames, str(self.rc.reader0.data) + '\t\t\t' + str(self.rc.reader1.data) + '\t\t\t'\
                + str(self.rc.reader2.data) + '\t\t\t' + str(self.rc.reader3.data) + '\t') 
            if duration is not None and time.time() > end_time:
                break

    
            
        
       


        

