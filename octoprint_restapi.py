import pycurl                         #sudo apt-get install libgnutls28-dev && sudo apt-get install libcurl4-gnutls-dev && sudo pip install pycurl
import yaml                           #sudo pip install pyyaml
import ast
import json
import os
import sys
from StringIO import StringIO
from argparse import ArgumentParser

#########################################################################
#  Usage Examples
#########################################################################

# 1. HTTP GET from local host
  #sudo python octoprint_restapi.py get -c 'api/job'

# 2. HTTP GET with options
  #sudo python octoprint_restapi.py get -c 'api/printer' -o 'history=true&limit=2'

# 3. HTTP POST with post data
  #sudo python octoprint_restapi.py post -c 'api/printer/printhead' -d '{ "command": "home", "axes": ["x", "y"] }'

# 4. Get API Key
  #sudo python octoprint_restapi.py getkey

# 5. Get API Key of specified user
  #sudo python octoprint_restapi.py getkey -u username

# 6. HTTP GET from a different machine on the network
  #sudo python octoprint_restapi.py get -a 'http://192.168.1.234:80/' -c 'api/job' -k 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# 7. Sequence to reset the SD Card
  #sudo python octoprint_restapi.py post -c 'api/printer/sd' -d '{ "command": "release" }'
  #sudo python octoprint_restapi.py post -c 'api/printer/sd' -d '{ "command": "init" }'

#########################################################################
#  Globals
#########################################################################

# Network address of octoprint
OCTOPRINT_ADDRESS = 'http://localhost:5000/'

# Octoprint user account
USERNAME = 'pi'

#########################################################################
#  Functions
#########################################################################

def READ_API_KEY(username = None):
	''' Get the api key for the given user name. The api key is needed to communicate with octoprint using the REST API. '''

	# Use default name if none is supplied
	if (username is None):
		username = USERNAME

	# Get path of config.yaml file that contains the API KEY
	path = '/home/' + username + '/.octoprint/config.yaml'

	if (os.path.exists(path) == False):
		print("Could not find /.octoprint/config.yaml for user " + username)
		sys.exit()

	# Open the file and extract the API KEY using a yaml parser
	with open(path, 'r') as stream:
		try:
			yaml_data = yaml.load(stream)
			api_key   = yaml_data['api']['key']
		except yaml.YAMLError as exc:
			print(exc)
			sys.exit()

	# Return the api key
	return api_key

def HTTP_GET(address, header = None, verbose = None):
	''' Send a HTTP GET request to the server address and return the response as a string. '''

	# Create a buffer to write the response to and get Curl object
	buffer = StringIO()
	c      = pycurl.Curl()

	# Configure the address
	c.setopt(c.URL, address)

	# Optionally add a header
	if (header is not None):
		c.setopt(c.HTTPHEADER, header)

	# Optionally add verbose option
	if ((verbose is not None) and (verbose is not False)):
		c.setopt(c.VERBOSE, True)

	# Configure the result buffer, send the GET request, get the response code and close the object
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	responseCode = c.getinfo(pycurl.RESPONSE_CODE)
	c.close()

	# Return the responseCode as int and result as string
	return responseCode, buffer.getvalue()

def HTTP_POST(address, postData, header = None, verbose = None):
	''' Send a HTTP POST request to the server address and return the response as a string. '''

	# Create a buffer to write the response to and get Curl object
	buffer = StringIO()
	c      = pycurl.Curl()

	# Configure the address
	c.setopt(c.URL, address)

	# Add the post data
	c.setopt(c.POSTFIELDS, json.dumps(postData))

	# Optionally add a header
	if (header is not None):
		c.setopt(c.HTTPHEADER, header)

	# Optionally add verbose option
	if ((verbose is not None) and (verbose is not False)):
		c.setopt(c.VERBOSE, True)

	# Configure the result buffer, send the POST request, get the response code and close the object
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	responseCode = c.getinfo(pycurl.RESPONSE_CODE)
	c.close()

	# Return the responseCode as int and result as string
	return responseCode, buffer.getvalue()

def REST_API_GET(command, address = None, api_key = None, options = None, verbose = None):
	''' Send a HTTP GET request to the octprint server using the given command, api_key and option. Response is a dictionary. '''

	# Ensure command parameter is present
	if (command is None):
		print("Command is a required parameter for REST_API_GET")
		sys.exit()

	# Get the user's API_KEY (if not supplied) so that we can send a GET request to octoprint
	if (api_key is None):
		api_key = READ_API_KEY(USERNAME)
	api_key = 'X-Api-Key: ' + api_key

	# If address is not specified then use default
	if (address is None):
		address = OCTOPRINT_ADDRESS

	# Ensure that the command can be appended to the address
	if (address.endswith("/") == False):
		address = address + "/"

	# Trim off the starting slash since we forced it on the address
	if ((command.startswith("/") == True) and (len(command) > 1)):
		command = command[1:]

	# Trim off the ending slash, as it is added automatically if options are present
	if (command.endswith("/") == True):
		command = command[:-1]

	# Add options if there are any
	address = address + command
	if (options is not None):
		address = address + "/?" + options

	# Prepare the header
	header = [api_key]

	# Send the GET request and get the result
	return HTTP_GET(address, header, verbose)

def REST_API_POST(command, postData, address = None, api_key = None, options = None, verbose = None):
	''' Send a HTTP GET request to the octprint server using the given command, api_key and option. Response is a dictionary. '''

	# Ensure command parameter is present
	if (command is None):
		print("Command is a required parameter for REST_API_POST")
		sys.exit()

	# Ensure postData parameter is present
	if (postData is None):
		print("PostData is a required parameter for REST_API_POST")
		sys.exit()
	# Otherwise translate from string to dictionary
	else:
		postData = ast.literal_eval(postData)

	# Indicate that the postData is in json format
	header = ['Content-Type: application/json']

	# Get the user's API_KEY (if not supplied) so that we can send a POST request to octoprint
	if (api_key is None):
		api_key = READ_API_KEY(USERNAME)
	api_key = 'X-Api-Key: ' + api_key

	# Add the api key to the header data
	header.append(api_key)

	# If address is not specified then use default
	if (address is None):
		address = OCTOPRINT_ADDRESS

	# Ensure that the command can be appended to the address
	if (address.endswith("/") == False):
		address = address + "/"

	# Trim off the starting slash since we forced it on the address
	if ((command.startswith("/") == True) and (len(command) > 1)):
		command = command[1:]

	# Trim off the ending slash, as it is added automatically if options are present
	if (command.endswith("/") == True):
		command = command[:-1]

	# Add options if there are any
	address = address + command
	if (options is not None):
		address = address + '?' + options

	# Send the POST request and get the result
	return HTTP_POST(address, postData, header, verbose)

#########################################################################
#  MAIN
#########################################################################
def main():
	''' Allow user to perform HTTP GET/POST requests with Octoprint REST API. '''

	# Declare input arguments
	parser = ArgumentParser()
	parser.add_argument("-a", "--address" , dest   = "address"   , help = "OctoPrint IP address if running GET/POST from another device on your network.")
	parser.add_argument("-c", "--command" , dest   = "command"   , help = "Octoprint GET/POST REST API command, such as 'api/job'")
	parser.add_argument("-k", "--key"     , dest   = "api_key"   , help = "API KEY for HTTP GET or POST request.")
	parser.add_argument("-o", "--options" , dest   = "options"   , help = "Options for HTTP GET/POST. Make sure to surround it in quotes.")
	parser.add_argument("-d", "--data"    , dest   = "postData"  , help = "Post data for HTTP POST as a dictionary.")
	parser.add_argument("-u", "--username", dest   = "username"  , help = "Username for API KEY request.")
	parser.add_argument("-v", "--verbose" , action = "store_true", help = "Enable HTTP verbose option.")
	parser.add_argument("function", help = "Desired function, such as getkey, get or post")

	# Parse the arguments
	args = parser.parse_args()

	# Perform user function based on arguments
	if (args.function.lower() == 'get'):
		responseCode, result = REST_API_GET(args.command, args.address, args.api_key, args.options, args.verbose)
		print(result)
	elif (args.function.lower() == 'post'):
		responseCode, result = REST_API_POST(args.command, args.postData, args.address, args.api_key, args.options, args.verbose)
		print(result)
	elif (args.function.lower() == 'getkey'):
		result = READ_API_KEY(args.username)
		print(result)
	else:
		print("Invalid argument function")

if __name__ == '__main__':
	main()

