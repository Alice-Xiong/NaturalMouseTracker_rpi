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

config 		= ConfigParser()
config.read('config.ini')
cfg = 'tracker_cage_record'
data_root 	= config.get(cfg, 'data_root')
image_stream_filename = config.get(cfg, 'raw_image_file')
res 	= list(map(int, config.get(cfg, 'resolution').split(', ')))
fr = int(config.get(cfg, 'framerate'))
iso = int(config.get(cfg, 'iso'))
sensormode = int(config.get(cfg, 'sensor_mode'))
mogHistory = int(config.get(cfg, 'mogHistory'))
varThreshold = int(config.get(cfg, 'var_Threshold'))
record_time_sec = int(config.get(cfg, 'record_time_sec'))

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = res
camera.framerate = fr
camera.awb_mode = 'off'
camera.awb_gains = (1,1)
#camera.exposure_mode ='off'
camera.shutter_speed = 30000
camera.iso = iso
camera.sensor_mode = sensormode
rawCapture = PiRGBArray(camera, size=res)
# allow the camera to warmup
time.sleep(0.1)

runSession = True
runRecording = True
mouse_id = input("Please enter mouse ID: ")

vstream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
while runSession:
    print("Start preview\n\n")
    
    if runRecording:
        totRewards = 0;
        # Get the current time and initialize the project folder
        tm = datetime.now()
        data_root = data_root + str(tm.year) + format(tm.month, '02d') + format(tm.day, '02d') + \
                           format(tm.hour, '02d') + format(tm.minute, '02d') + format(tm.second, '02d')
        if not os.path.exists(data_root):
                print("Creating data directory: ",data_root)
                os.makedirs(data_root)
        
        image_hdf5_path = data_root + os.sep + image_stream_filename
        
        image_hdf5_file = tables.open_file(image_hdf5_path, mode='w')
        data_storage = image_hdf5_file.create_earray(image_hdf5_file.root, 'raw_images',
                                      tables.Atom.from_dtype(np.dtype('uint8')),
                                      shape=(0, res[0], res[1], 3))
        logFileName = data_root + os.sep + "VideoTimestamp.txt"
        logFile = open(logFileName, 'w', encoding="utf-8")
        logFile.write('frame' + '\t' + 'time' + '\t\t\t\t' + 'RFID pick up' +  '\t' +  "\n")
        print("Start recording\n\n")

    fps = FPS().start()
    t_end = time.time() + record_time_sec
    for img in vstream:
        start = time.time()
        image = img.array
        fps.update()
        print("analog gain: ", eval(str(camera.analog_gain)))
        print("digital gain: ", eval(str(camera.digital_gain))) 

        data_storage.append(image[None])
        sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logFile.write(str(fps._numFrames) + '\t' + sttime + '\t' + str(1) + "\n")
        
        # Flush Picamera ready for next frame
        rawCapture.seek(0)
        #rawCapture.truncate(0)
        # Press Esc or Ctrl-C to stop the program
        if time.time() >= t_end:
            run_threads = False
            runSession = False
            break

    fps.stop()
    image_hdf5_file.close()
    logFile.close()

vstream.close()
rawCapture.close()
camera.close()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

