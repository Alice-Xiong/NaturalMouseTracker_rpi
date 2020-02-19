def record():
    global frameCount, goodEvent, badEvent
    goodEvent = threading.Event()
    badEvent = threading.Event()
    """
    Setting to timeout to None means we don't return till we have a tag.
    If a timeout is set and no tag is found, 0 is returned.
    """
    #Creating instances of TagReader 
    reader0 = TagReader ('/dev/ttyUSB0', RFID_doCheckSum, timeOutSecs = None, kind=RFID_kind)
    reader1 = TagReader ('/dev/ttyUSB1', RFID_doCheckSum, timeOutSecs = None, kind=RFID_kind)
    reader2 = TagReader ('/dev/ttyUSB2', RFID_doCheckSum, timeOutSecs = None, kind=RFID_kind)
    reader3 = TagReader ('/dev/ttyUSB3', RFID_doCheckSum, timeOutSecs = None, kind=RFID_kind)

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