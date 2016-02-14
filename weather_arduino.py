from time import gmtime, sleep, strftime
import json
import requests
import serial
import sys

## Arduino port given as an argument:
ARDUINO_PORT = sys.argv[1]

## The Weather Company credentials:
TWC_USERNAME = 'YOUR_USERNAME'
TWC_PASSWORD = 'YOUR_PASSWORD'
TWC_HOST = 'twcservice.mybluemix.net'
TWC_PORT = 443
TWC_URL = 'YOUR_URL'
TWC_CURRENT = '/api/weather/v2/observations/current'

## 51 Astor Place longitude and latitude
ASTOR_LAT = 40.73
ASTOR_LONG = -73.99

class ArduinoDisplay:
	def __init__(self):
		self.arduino = serial.Serial(ARDUINO_PORT, 9600)
		## Wipe the display and connect...
		self.arduino.write("                                                                ".encode())
		print('Getting ready...\t3')
		sleep(1)
		print('\t\t\t2')
		sleep(1)
		print('\t\t\t1')
		sleep(1)

	def sendToArduino(self, message):
		self.arduino.write(message.encode())

class Main:
	def __init__(self):
		self._arduino = ArduinoDisplay()
		self._weather = TheWeatherCompany()

	def _formatForArduino(self, currentBlob):
		phraseString = currentBlob['phrase_12char'][0:16]
		phraseString += ' @ Astor'
		if len(phraseString) < 16:
			x = len(phraseString)
			while x < 16:
				phraseString += ' '
				x+=1
		# Only if you're not already getting celsius:
		celsius = (currentBlob['temp'] - 32) * (5 / 9)
		celsius = str(celsius).split('.')
		celsius = celsius[0]
		tempString = str(currentBlob['temp']) + 'F / ' + celsius + 'C'
		return phraseString + tempString

	def start(self):
		x = 0
		while x < 1:
			weatherBlob = self._weather.getCurrentConditions(ASTOR_LAT, ASTOR_LONG)
			displayString = self._formatForArduino(weatherBlob)
			print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
			print(displayString)
			self._arduino.sendToArduino(displayString)
			sleep(200)

class TheWeatherCompany:
	def __init__(self):
		pass

	def _getCurrentPhrase(self, twcBlob):
		return twcBlob['observation']['phrase_12char']

	# def _getCurrentTempC(self, twcBlob):
	# 	return twcBlob['observation']['metric']['temp']

	def _getCurrentTempF(self, twcBlob):
		return twcBlob['observation']['imperial']['temp']

	def _requestLocal(self, latitude, longitude):
		geocodeString = str(ASTOR_LAT) + ',' + str(ASTOR_LONG)
		requestedParams = {
			'units': 'e',
			'geocode': geocodeString,
			'language': 'en-US'
		}
		response = requests.get(TWC_URL + TWC_CURRENT, params=requestedParams)
		response = json.loads(response.text)
		return response

	def getCurrentConditions(self, latitude, longitude):
		twcBlob = self._requestLocal(latitude, longitude)
		responseBlob = {
			'phrase_12char': self._getCurrentPhrase(twcBlob),
			'temp': self._getCurrentTempF(twcBlob)
		}
		return responseBlob

runner = Main()
runner.start()
