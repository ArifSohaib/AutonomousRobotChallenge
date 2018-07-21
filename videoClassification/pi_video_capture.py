from picamera import PiCamera

#from https://blog.coast.ai/continuous-online-video-classification-with-tensorflow-inception-and-a-raspberry-pi-785c8b1e13e1
def capture_images(save_folder):
    """Stream images off camera and save them"""
    camera = PiCamera()
    camera.resolution = (320,240)
    camera.framerate = 10
    #warmup
    time.sleep(2)
    #capture continously 
    for i, frame in enumerate(camera.capture_continous(save_folder + '{timestamp}.jpg','jpg',use_video_port=True )):
        pass

