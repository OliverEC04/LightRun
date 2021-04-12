import requests
from grovepi import *
from grove_rgb_lcd import *
import time
from datetime import datetime

OPENAPIKEY = "99d1537201baa36962b6e12ec162c1fa"
WORLDAPIKEY = "4ad5b246ce7c4c2fb36132316200312"
COORDS = [
	["klitmoller", [57.051461, 8.453151], [[0, 60], [180, 250]], 6],
	["hanstholm", [57.121621, 8.584584], [[230, 310], [45, 90]], 3],
	["agger", [56.738567, 8.206832], [[135, 200]], 8],
	["hvide sande", [55.990050, 8.068257], [[135, 160], [300, 359]], 7],
	["fornæs", [56.444765, 11.009998], [[160, 350]], 4],
	["bornholm", [55.053853, 15.162707], [[45, 135]], 5]
]

def getOpenWeather(coords):
	response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + str(coords[0]) + "&lon=" + str(coords[1]) + "&appid=" + OPENAPIKEY)
	return response.json()

def getWorldWeather(coords):
	response = requests.get("http://api.worldweatheronline.com/premium/v1/marine.ashx?key=" + WORLDAPIKEY + "&format=json&q=" + str(coords[0]) + "," + str(coords[1]))
	return response.json()

for x in COORDS:
	print(x[0] + ": ")
	print(getOpenWeather(x[1])["current"]["wind_speed"])

setText("Hello world LCD test")
setRGB(0,128,64)

led = 8

pinMode(led,"OUTPUT")
#pinMode(2, "INPUT")
digitalWrite(led, 1)
#print(digitalRead(2))
time.sleep(10)
#digitalWrite(led, 0)

while True:
	print("Updated")
	for location in COORDS:
		openWeather = getOpenWeather(location[1])
		worldWeather = getWorldWeather(location[1])

		hour = datetime.now().hour
		i = 0
		for h in range(0, 2400, 300):
			i += 1
			if hour > h:
				swellHeight = worldWeather["data"]["weather"][0]["hourly"][i]

		windSpeed = openWeather["current"]["wind_speed"]
		windDeg = openWeather["current"]["wind_deg"]

		print(windSpeed)
		if windSpeed > 1:
			digitalWrite(location[3], 1)
			for degRange in location[2]:
				if degRange[0] < windDeg and windDeg < degRange[1]:
					digitalWrite(location[3], 1)
				else:
					print("hej")
					#digitalWrite(location[3], 0)

	time.sleep(300)