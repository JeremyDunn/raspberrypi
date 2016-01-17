import picamera
from time import sleep

camera = picamera.PiCamera()

#camera.capture('image.jpg')

camera.hflip = True
camera.vflip = True

camera.start_recording('video.h264')
sleep(5)
camera.stop_recording()

