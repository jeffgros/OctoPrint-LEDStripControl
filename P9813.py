# Python P9813 LED Driver

# This module was has been changed. Orignal is Micropython-p9813 LED driver (https://github.com/mcauser/micropython-p9813/blob/master/p9813.py)
# Even so, I don't think it was original. I think it was a port to Raspberry Pi from the Seeed Studio Arduino source (http://wiki.seeedstudio.com/wiki/File:LEDStripDriver_library.zip)

# The version I changed was in micropython, and I wanted to use my safer safeGPIO library, so I did some modifications.
# The clock latches on rising edge, and is idle high (datasheet notes pullups on CLK and DATA)

from safeGPIO import safeGPIO as GPIO
import time

#########################################################################
#  CLASSES
#########################################################################

class P9813:

	def __init__(self, pin_clk, pin_data, num_leds = 1, sleepEnabled = False):
		self.pin_clk      = pin_clk
		self.pin_data     = pin_data
		self.num_leds     = num_leds
		self.sleepEnabled = sleepEnabled

		# Enforce boolean
		if (self.sleepEnabled != True):
			self.sleepEnabled = False

		# Configure the port pins
		self.gpio = GPIO()
		self.gpio.setmode(GPIO.BOARD)
		self.gpio.setwarnings(False)
		self.gpio.setup(self.pin_clk , GPIO.OUT)
		self.gpio.setup(self.pin_data, GPIO.OUT)
		self.gpio.output(self.pin_clk , 1)
		self.gpio.output(self.pin_data, 1)

		# Reset all LEDs and create space for the data
		self.reset()

	def __del__(self):
		self.gpio.cleanup()

	def __setitem__(self, index, val):
		offset = index * 3
		for i in range(3):
			self.buf[offset + i] = val[i]

	def __getitem__(self, index):
		offset = index * 3
		return tuple(self.buf[offset + i] for i in range(3))

	def fill(self, color):
		for i in range(self.num_leds):
			self[i] = color

	def reset(self):
		# Allocate space for LED data
		self.buf = bytearray(self.num_leds * 3)

		# Begin data frame 4 bytes
		self._frame()

		# 4 bytes for each led (checksum, blue, green, red)
		for i in range(self.num_leds):
			self._write_byte(0xC0)
			for i in range(3):
				self._write_byte(0)

		# End data frame 4 bytes
		self._frame()

	def write(self):
		# Begin data frame 4 bytes
		self._frame()

		# 4 bytes for each led (checksum, blue, green, red)
		for i in range(self.num_leds):
			self._write_color(self.buf[i * 3], self.buf[i * 3 + 1], self.buf[i * 3 + 2])

		# End data frame 4 bytes
		self._frame()

	def _sleep_us(self, microseconds):
		time.sleep(x/1000000.0)

	def _frame(self):
		# Send 32x zeros
		self.gpio.output(self.pin_data, 0)
		for i in range(32):
			self._clk()

	def _clk(self):
		self.gpio.output(self.pin_clk, 0)

		if (self.sleepEnabled):
			self._sleep_us(1) # works without it (3.6 us)
		self.gpio.output(self.pin_clk, 1)

		if (self.sleepEnabled):
			self._sleep_us(1) # works without it (3.6 us)

	def _write_byte(self, b):
		if (b == 0):
			# Fast send 8x zeros
			self.gpio.output(self.pin_data, 0)
			for i in range(8):
				self._clk()
		else:
			# Send each bit, MSB first
			for i in range(8):
				if ((b & 0x80) != 0):
					self.gpio.output(self.pin_data, 1)
				else:
					self.gpio.output(self.pin_data, 0)
				self._clk()

				# On to the next bit
				b <<= 1

	def _write_color(self, r, g, b):
		# Send a checksum byte with the format "1 1 ~B7 ~B6 ~G7 ~G6 ~R7 ~R6"
		# The checksum colour bits should bitwise NOT the data colour bits
		checksum  = 0xC0 # 0b11000000
		checksum |= (b >> 6 & 3) << 4
		checksum |= (g >> 6 & 3) << 2
		checksum |= (r >> 6 & 3)

		self._write_byte(checksum)

		# Send the 3 colors
		self._write_byte(b)
		self._write_byte(g)
		self._write_byte(r)

#########################################################################
# MAIN
#########################################################################
def main():
        ''' Ask the user repeatedly for LED brightness setting '''

	# Construct the object
	ledDriver = P9813(11, 15)

	# Create led (R,G,B) list
	leds = [ [0,0,0] ]

	# Ask the user repeatedly for LED brightness setting
	try:
		while (True):
			str     = raw_input("Input R, G, B [Enter] or Ctrl-C to quit. R, G, B range from 0 - 255: ")
			leds[0] = list(map(int, str.split(",")))
			print(leds[0])
			ledDriver[0] = leds[0]
			ledDriver.write()
	except KeyboardInterrupt:
		print("\r")
	except:
		print(str)

	# Turn off LEDs before we quit
	leds[0]      = [0, 0, 0]
	ledDriver[0] = leds[0]
	ledDriver.write()

if __name__ == '__main__':
	main()
