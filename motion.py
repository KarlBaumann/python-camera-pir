from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import mailer

camera = PiCamera()
#camera.resolution = (1920,1080)
#camera.resolution = (2592,1944)
camera.resolution = (1296,972)
camera.rotation = 180
camera.framerate = 15

pir = MotionSensor(17)
run = True

try:
	mailer.sendMail("karl@bauman.is","Detection started", ":)")
	while run:
		pir.wait_for_motion()
		filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
		#filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.mjpeg")
		camera.start_recording(filename)
		
		#camera.capture(filename)
		mailer.sendMail("karl@bauman.is","Movement in Attic", filename)
		pir.wait_for_no_motion()
		camera.stop_recording()
		
except KeyboardInterrupt:
	print (" Quit")
	# Reset GPIO settings
	run = False
