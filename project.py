import requests
from json import *
import flask


import requests

API_KEY = "A7fRTF6DALK83u4DCgjEmksOWDzNvkwG "
LAT, LON = 55.7558, 37.6173

location_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
params = {
    "apikey": API_KEY,
    "q": f"{LAT},{LON}",
    "details": "true"
}

response = requests.get(location_url, params=params)
data = response.json()
location_key = data["Key"]
print(f"Ключ локации: {location_key}")

weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"

response = requests.get(weather_url, params=params)
weather_data = response.json()
#print(weather_data)
print(f"Текущая погода: {weather_data[0]['WeatherText']}, {weather_data[0]['Temperature']['Metric']['Value']}{weather_data[0]['Temperature']['Metric']['Unit']}\n\
       Относительная влажность: {weather_data[0]["RelativeHumidity"]} %")
