import RPi.GPIO as GPIO
import time

#########################################################################
#  Usage Example
#########################################################################

# from safeGPIO import safeGPIO as GPIO
# import time

# print("Hello World!")
# gpio = GPIO()
# gpio.setmode(GPIO.BOARD)
# gpio.setup(11, GPIO.OUT)

# gpio.output(11, 1)
# time.sleep(1)
# gpio.output(11, 0)
# time.sleep(1)
# gpio.output(11, 1)
# time.sleep(1)
# print("Exiting test")

#########################################################################
#  CLASSES
#########################################################################

class safeGPIO():
	''' Add automatic cleanup to RPi.GPIO module by calling in __del__ (we keep reference to GPIO to ensure its still there)'''

	# Class variables
	HIGH     = GPIO.HIGH
	LOW      = GPIO.LOW
	OUT      = GPIO.OUT
	IN       = GPIO.IN
	HARD_PWM = GPIO.HARD_PWM
	SERIAL   = GPIO.SERIAL
	I2C      = GPIO.I2C
	SPI      = GPIO.SPI
	UNKNOWN  = GPIO.UNKNOWN
	BOARD    = GPIO.BOARD
	BCM      = GPIO.BCM
	PUD_OFF  = GPIO.PUD_OFF
	PUD_UP   = GPIO.PUD_UP
	PUD_DOWN = GPIO.PUD_DOWN
	RISING   = GPIO.RISING
	FALLING  = GPIO.FALLING
	BOTH     = GPIO.BOTH
	VERSION  = GPIO.VERSION

	def __init__(self):
		# Create a reference to GPIO so that we can use it during delete
		self.gpio = GPIO
		self.gpio.setmode(self.BOARD)
		self.gpio.setup(13, self.OUT)

	def __del__(self):
		self.cleanup()

	# python function cleanup(channel=None)
	def cleanup(self, *args):
		return self.gpio.cleanup(*args)

	# python function setup(channel(s), direction, pull_up_down=PUD_OFF, initial=None)
	def setup(self, *args):
		return self.gpio.setup(*args)

	# python function output(channel(s), value(s))
	def output(self, *args):
		return self.gpio.output(*args)

	# python function value = input(channel)
	def input(self, *args):
		return self.gpio.input(*args)

	# python function setmode(mode)
	def setmode(self, *args):
		return self.gpio.setmode(*args)

	# python function getmode()
	def getmode(self, *args):
		return self.gpio.getmode(*args)

	# python function add_event_callback(gpio, callback)
	def add_event_callback(self, *args):
		return self.gpio.add_event_callback(*args)

	# python function add_event_detect(gpio, edge, callback=None, bouncetime=None)
	def add_event_detect(self, *args):
		return self.gpio.add_event_detect(*args)

	# python function remove_event_detect(gpio)
	def remove_event_detect(self, *args):
		return self.gpio.remove_event_detect(*args)

	# python function value = event_detected(channel)
	def event_detected(self, *args):
		return self.gpio.event_detected(*args)

	# python function channel = wait_for_edge(channel, edge, bouncetime=None, timeout=None)
	def wait_for_edge(self, *args):
		return self.gpio.wait_for_edge(*args)

	# python function value = gpio_function(channel)
	def gpio_function(self, *args):
		return self.gpio.gpio_function(*args)

	# python function setwarnings(state)
	def setwarnings(self, *args):
		return self.gpio.setwarnings(*args)
