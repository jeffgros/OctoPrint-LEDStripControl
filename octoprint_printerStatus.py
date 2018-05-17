import octoprint_restapi
import copy
import json
import time
from argparse import ArgumentParser

#########################################################################
#  Usage Example
#########################################################################

# sudo python octoprint_printerStatus.py -a 'http://192.168.1.234:80/' -k 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#########################################################################
#  CLASSES
#########################################################################

class PrinterStatus:
	''' Parse printer status from input data. '''

	def __init__(self, address = None, api_key = None, options = None, verbose = None):
		''' Save input options and call update routine '''

		# Save input options
		self.address = address
		self.api_key = api_key
		self.options = options
		self.verbose = verbose

		# Update internal veriables by performing GET requests
		self.update()

	def update(self):
		''' Update internal variables by performing GET requests '''

		# Get the printer status
		self.apiJobResponseCode    , self.apiJobResult     = octoprint_restapi.REST_API_GET('api/job'    , self.address, self.api_key, self.options, self.verbose)
		self.apiPrinterResponseCode, self.apiPrinterResult = octoprint_restapi.REST_API_GET('api/printer', self.address, self.api_key, self.options, self.verbose)

		# Create job result dictionary from result string
		if (self.apiJobResult[0] == '{'): self.apiJobResultDictionary = json.loads(self.apiJobResult)
		else                            : self.apiJobResultDictionary = None

		# Create printer result dictionary from result string
		if (self.apiPrinterResult[0] == '{'): self.apiPrinterResultDictionary = json.loads(self.apiPrinterResult)
		else                                : self.apiPrinterResultDictionary = None

	def getApiJobResponseCode(self):
		''' Return apiJob response code '''
		return self.apiJobResponseCode

	def getApiJobResultString(self):
		''' Return apiJob result string '''
		return self.apiJobResult

	def getApiJobResultDictionary(self):
		''' Return apiJob result dictionary '''
		return copy.deepcopy(self.apiJobResultDictionary)

	def getApiPrinterResponseCode(self):
		''' Return apiPrinter response code '''
		return self.apiPrinterResponseCode

	def getApiPrinterResultString(self):
		''' Return apiPrinter result string '''
		return self.apiPrinterResult

	def getApiPrinterResultDictionary(self):
		''' Return apiPrinter result dictionary '''
		return copy.deepcopy(self.apiPrinterResultDictionary)

	def getErrorState(self):
		''' Get the error state string '''

		if (self.apiJobResponseCode     !=  200): return None
		if (self.apiJobResultDictionary is None): return None

		if (('state' in self.apiJobResultDictionary)                 == False): return None
		if (self.apiJobResultDictionary['state'].startswith("Error") == False): return None

		return self.apiJobResultDictionary['state'].replace("Error: ", "")

	def isPrinterConnected(self):
		''' Return printerConnected? as True/False '''

		if (self.apiJobResponseCode     !=  200): return False
		if (self.apiJobResultDictionary is None): return False

		if (('state' in self.apiJobResultDictionary) == False): return False

		return (self.apiJobResultDictionary['state'].startswith("Offline") == False)

	def isPrintActive(self):
		''' Return printActive? as True/False '''

		if (self.isPrinterConnected()       == False): return False
		if (self.apiPrinterResponseCode     !=   200): return False
		if (self.apiPrinterResultDictionary is  None): return False

		if (('state'    in self.apiPrinterResultDictionary                  ) == False): return False
		if (('flags'    in self.apiPrinterResultDictionary['state']         ) == False): return False
		if (('printing' in self.apiPrniterResultDictionary['state']['flags']) == False): return False

		return self.apiPrinterResultDictionary['state']['flags']['printing']

	def getCompletionPercentage(self):
		''' Return completionPercentage or None on error '''

		if (self.isPrinterConnected()   == False): return None
		if (self.apiJobResultDictionary is  None): return None

		if (('progress'   in self.apiJobResultDictionary            ) == False): return None
		if (('completion' in self.apiJobResultDictionary['progress']) == False): return None

		return self.apiJobResultDictionary['progress']['completion']

	def getBedTemperatureDegC(self):
		''' Return bed temperature in degrees C, or None on error '''

		if (self.isPrinterConnected()       == False): return None
		if (self.apiPrinterResponseCode     !=   200): return None
		if (self.apiPrinterResultDictionary is  None): return None

		# After serial connection, octoprint returns an empty dictionary for temperature, so we must test that keys exist
		if (('temperature' in self.apiPrinterResultDictionary                      ) == False): return None
		if (('bed'         in self.apiPrinterResultDictionary['temperature']       ) == False): return None
		if (('actual'      in self.apiPrinterResultDictionary['temperature']['bed']) == False): return None

		return self.apiPrinterResultDictionary['temperature']['bed']['actual']

	def getTool0TemperatureDegC(self):
		''' Return tool0 temperature in degrees C, or None on error '''

		if (self.isPrinterConnected()       == False): return None
		if (self.apiPrinterResponseCode     !=   200): return None
		if (self.apiPrinterResultDictionary is  None): return None

		# After serial connection, octoprint returns an empty dictionary for temperature, so we must test that keys exist
		if (('temperature' in self.apiPrinterResultDictionary                        ) == False): return None
		if (('tool0'       in self.apiPrinterResultDictionary['temperature']         ) == False): return None
		if (('actual'      in self.apiPrinterResultDictionary['temperature']['tool0']) == False): return None

		return self.apiPrinterResultDictionary['temperature']['tool0']['actual']

#########################################################################
# MAIN
#########################################################################
def main():
	''' Get printer status and print to screen '''

	# Declare input arguments
	parser = ArgumentParser()
	parser.add_argument("-a", "--address", dest   = "address"   , help = "OctoPrint IP address if running GET/POST from another device on your network.")
	parser.add_argument("-k", "--key"    , dest   = "api_key"   , help = "API KEY for HTTP GET or POST request.")
	parser.add_argument("-v", "--verbose", action = "store_true", help = "Enable HTTP verbose option.")

	# Parse the arguments
	args         = parser.parse_args()
	args.options = None

	# Pass the data into the printer status class
	printer = PrinterStatus(args.address, args.api_key, args.options, args.verbose)

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
			print("\r")

			# Sleep for a while before trying again
			time.sleep(1)

			# Update the printer status
			printer.update()
	except:
		print("\r")
		print("Printing contents of previous result...")
		print("Job Response Code: "     + `printer.getApiJobResponseCode()`    )
		print("Printer Response Code: " + `printer.getApiPrinterResponseCode()`)
		print("Job result string:")
		print(printer.getApiJobResultString())
		print("Printer result string:")
		print(printer.getApiPrinterResultString())

if __name__ == '__main__':
	main()
