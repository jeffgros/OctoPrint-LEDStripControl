import octoprint_restapi
from argparse import ArgumentParser

#########################################################################
#  Usage Example
#########################################################################

# sudo python octoprint_restartSD.py -a 'http://192.168.1.234:80/' -k 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

#########################################################################
#  MAIN
#########################################################################
def main():
        ''' Refresh the SD card contents. '''

        # Declare input arguments
        parser = ArgumentParser()
        parser.add_argument("-a", "--address" , dest   = "address"    , help = "OctoPrint IP address if running GET/POST from another device on your network.")
        parser.add_argument("-k", "--key"     , dest   = "api_key"    , help = "API KEY for HTTP GET or POST request.")
        parser.add_argument("-v", "--verbose" , action = "store_true" , help = "Enable HTTP verbose option.")

        # Parse the arguments
        args         = parser.parse_args()
	args.options = None

	# Refresh the SD Card contents
	apiPrinterSDResponseCode1, apiPrinterResult1 = octoprint_restapi.REST_API_POST('api/printer/sd', '{ "command": "release" }', args.address, args.api_key, args.options, args.verbose)
	apiPrinterSDResponseCode2, apiPrinterResult2 = octoprint_restapi.REST_API_POST('api/printer/sd', '{ "command": "init" }'   , args.address, args.api_key, args.options, args.verbose)

	print("Release Response Code: " + `apiPrinterSDResponseCode1`)
	print("Init    Response Code: " + `apiPrinterSDResponseCode2`)

if __name__ == '__main__':
        main()
