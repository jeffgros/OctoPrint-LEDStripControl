import octoprint_printerStatus
import time
from argparse import ArgumentParser
from P9813 import P9813

#########################################################################
#  Usage Example
#########################################################################

# sudo python octoprint_LED_PWM_displayPrinterStatus.py -a 'http://192.168.1.234:80/' -k 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#########################################################################
# MAIN
#########################################################################
def main():
	''' Get printer status and print to screen as well as light the LEDs'''

	# Declare input arguments
	parser = ArgumentParser()
	parser.add_argument("-a", "--address", dest   = "address"   , help = "OctoPrint IP address if running GET/POST from another device on your network.")
	parser.add_argument("-k", "--key"    , dest   = "api_key"   , help = "API KEY for HTTP GET or POST request.")
	parser.add_argument("-v", "--verbose", action = "store_true", help = "Enable HTTP verbose option.")

	# Parse the arguments
	args         = parser.parse_args()
	args.options = None

	# Pass the data into the printer status class
	printer = octoprint_printerStatus.PrinterStatus(args.address, args.api_key, args.options, args.verbose)

	# Construct the object
	ledDriver = P9813(11, 15)

        # Turn off LEDs at start
	leds         = [ [0,0,0] ]
        ledDriver[0] = leds[0]
        ledDriver.write()

	# Define color constants
	#              [           R,            G,            B]
	LED_STRENGTH = 100
	LEDS_OFF     = [           0,            0,            0]
	LEDS_RED     = [LED_STRENGTH,            0,            0]
	LEDS_GREEN   = [           0, LED_STRENGTH,            0]
	LEDS_BLUE    = [           0,            0, LED_STRENGTH]
	LEDS_YELLOW  = [LED_STRENGTH, LED_STRENGTH,            0]
	LEDS_MAGENTA = [LED_STRENGTH,            0, LED_STRENGTH]
	LEDS_CYAN    = [           0, LED_STRENGTH, LED_STRENGTH]
	LEDS_WHITE   = [LED_STRENGTH, LED_STRENGTH, LED_STRENGTH]

	previouslyConnected = False

	# Poll the printer for status
	try:

		while (True):

			# Print out status for debug
			print("Is printer connected? "  + str(printer.isPrinterConnected()     )                                 )
			print("Is print active? "       + str(printer.isPrintActive()          )                                 )
			print("Error state: "           + str(printer.getErrorState()          )                                 )
			print("Completion Percentage: " + str(printer.getCompletionPercentage())                                 )
			print("Bed Temperature: "       + str(printer.getBedTemperatureDegC()  ) + " " + u'\N{DEGREE SIGN}' + "C")
			print("Tool 0 Temperature: "    + str(printer.getTool0TemperatureDegC()) + " " + u'\N{DEGREE SIGN}' + "C")
			print("LEDS: "                  + str(leds[0]                          )                                 )
			print("\r")

			# Set led state based on printer state

			# Only turn yellow if we lose connection unexpectedly
			if ((printer.isPrinterConnected() == False) and (previouslyConnected == True)):
				print("YELLOW")
				leds[0] = LEDS_YELLOW
			# If connected but we have an error, then turn red
			elif (printer.getErrorState() is not None):
				print("RED")
				leds[0] = LEDS_RED
			# If not complete then turn off LEDS
			elif (printer.getCompletionPercentage() != 100):
				print("OFF1")
				leds[0] = LEDS_OFF
			# If connected, complete and below target bed temp, then turn blue
			elif ((printer.getCompletionPercentage() == 100) and (printer.getBedTemperatureDegC() <= 35.0)):
				print("BLUE")
				leds[0] = LEDS_BLUE
			# If connected and complete, then turn green
			elif (printer.getCompletionPercentage() == 100):
				print("GREEN")
				leds[0] = LEDS_GREEN
                        # Catchall (should be invalid state)
                        else:
				print("OFF2")
                                leds[0] = LEDS_OFF

			# Update LEDs
			ledDriver[0] = leds[0]
			ledDriver.write()

			# Keep track of connection status
			if (printer.isPrinterConnected()):
				previouslyConnected = True

			# Sleep for a while before trying again
			time.sleep(1)

			# Update the printer status
			printer.update()
	except KeyboardInterrupt:
		print("\r")
	except:
		pass

	print("Printing contents of previous result...")
	print("Job Response Code: "     + `printer.getApiJobResponseCode()`)
	print("Printer Response Code: " + `printer.getApiPrinterResponseCode()`)
	print("Job result string:")
	print(printer.getApiJobResultString())
	print("Printer result string:")
	print(printer.getApiPrinterResultString())

	# Turn off LEDs before we quit
	leds[0]      = LEDS_OFF
	ledDriver[0] = leds[0]
	ledDriver.write()

if __name__ == '__main__':
	main()
