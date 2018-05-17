from safeGPIO import safeGPIO as GPIO
import time

print("Hello World!")
gpio = GPIO()
gpio.setmode(GPIO.BOARD)
gpio.setup(11, GPIO.OUT)

gpio.output(11, 1)
time.sleep(1)
gpio.output(11, 0)
time.sleep(1)
gpio.output(11, 1)
time.sleep(1)
print("Exiting test")

