import requests
from json import *
import flask

API_KEY = "ICSSxjsJtHPvR1JaDcBWSQW7pig6mAKf "
LAT, LON = 55.7558, 37.6173

location_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
params = {
    "apikey": API_KEY,
    "q": f"{LAT},{LON}",
    "details": "true"
}
response = requests.get(location_url, params=params)
#print(response.status_code)
data = response.json()
location_key = data["Key"]
forecast_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
#print(f"Ключ локации: {location_key}")
def basic_weather(weather_url, params):
    response = requests.get(weather_url, params=params)
    weather_data = response.json()
    #print(weather_data)
    return f"Текущая погода: {weather_data[0]['WeatherText']}, {weather_data[0]['Temperature']['Metric']['Value']}{weather_data[0]['Temperature']['Metric']['Unit']}\n\
Относительная влажность: {weather_data[0]["RelativeHumidity"]} %\n Скорость ветра: {weather_data[0]["Wind"]["Speed"]["Metric"]["Value"]} {weather_data[0]["Wind"]["Speed"]["Metric"]["Unit"]}\n"

def precipitation_probab(params, forecast_url):

    response = requests.get(forecast_url, params=params)
    forecast_data = response.json()
    daily_forecast = forecast_data["DailyForecasts"][0]
    precipitation_probability = daily_forecast["Day"]["PrecipitationProbability"]
    return f"Вероятность осадков сегодня: {precipitation_probability}%\n"

print(basic_weather(weather_url, params), precipitation_probab(params, forecast_url))