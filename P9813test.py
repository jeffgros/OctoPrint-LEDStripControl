from P9813 import P9813

#########################################################################
# MAIN
#########################################################################
def main():
	''' Get printer status and print to screen as well as ligth the LEDs'''

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
