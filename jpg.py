from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
from fractions import Fraction
import mailer
import RPi.GPIO as GPIO
import time
import owncloud
import os

oc = owncloud.Client('https://up.bauman.is')
oc.login(os.environ['OWNCLOUD_USER'], os.environ['OWNCLOUD_PASS'])
#oc.mkdir('piCamera')

camera = PiCamera(
    resolution=(2592,1944),
    framerate=Fraction(1, 6),
    sensor_mode=3)
camera.rotation = 180 
camera.shutter_speed = 400000
#camera.shutter_speed = 400000
camera.iso = 800
time.sleep(10)
camera.exposure_mode = 'off'
path = "/var/ramdisk/"
run = True
count = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)         #Read output from PIR motion sensor

try:
	mailer.sendMail("karl@bauman.is","Detection started", ":)")
	while run:
			i=GPIO.input(17)
			if count == 1:
				mailer.sendMail("karl@bauman.is","Something is detected", ":)")
			if i==0:                 #When output from motion sensor is LOW
				#print ("No intruders",i)
				time.sleep(0.1)
				count = 0
			elif i==1:               #When output from motion sensor is HIGH
				print ("Intruder detected",i)
				filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S_"+str(count)+".jpg")
				camera.capture(path + filename)
				
				while True:
					try:
						oc.put_file('piCamera/' + filename, path + filename)
					except:
						continue
					break
					
				os.remove(path + filename)
				count = count + 1
except KeyboardInterrupt:
	print (" Quit")
	GPIO.cleanup()  # Reset GPIO settings
	camera.close()
	run = False