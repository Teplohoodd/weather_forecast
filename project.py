import requests
import asyncio
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
async def basic_weather(weather_url, params):
    response = requests.get(weather_url, params=params)
    weather_data = response.json()
    discription = weather_data[0]['WeatherText']
    temp = weather_data[0]['Temperature']['Metric']['Value']
    humidity = weather_data[0]["RelativeHumidity"]
    wind_speen = weather_data[0]["Wind"]["Speed"]["Metric"]["Value"]
    #print(weather_data)
    return [discription, temp, humidity, wind_speen]

async def precipitation_probab(params, forecast_url):

    response = requests.get(forecast_url, params=params)
    forecast_data = response.json()
    daily_forecast = forecast_data["DailyForecasts"][0]
    precipitation_probability = daily_forecast["Day"]["PrecipitationProbability"]
    return precipitation_probability


def check_bad_weather(weather, precipitation):
    bad = False

    if weather[1] >= 60 or weather[1] <= -50:
        print("Нереалистичное значение температуры")
        return 5

    else:
        if weather[1] < -10 or weather[1] > 30:
            bad = True

    if weather[2] > 100 or weather[2] < 0:
        print("Нереалистичное значение влажности")
        return 5
    else:
        if weather[2] < 20 or weather[2] > 70:
            bad = True

    if weather[3] < 0 or weather[3] > 100:
        print("Нереалистичное значение скорости ветра")
        return 5
    else:
        if weather[3] > 30:
            bad = True

    if precipitation < 0 or precipitation > 100:
        print("Нереалистичное значение вероятности осадков")
        return 5
    else:
        if precipitation > 40:
            bad = True
    return bad




async def main():
    weather = await basic_weather(weather_url, params)
    precipitation = await precipitation_probab(params, forecast_url)

    is_bad = check_bad_weather(weather, precipitation)
    if is_bad == False:
        print("Текущая погода: ", weather[0])
        print("Текущая температура: ", weather[1])
        print("Относительная влажность: ", weather[2])
        print("Скорость ветра: ", weather[3])
        print("Вероятность осадков сегодня:", precipitation, "%\n")
        print("Погодные условия - супер!")
    elif is_bad == 5:
        ...
    else:
        print("Текущая погода: ", weather[0])
        print("Текущая температура: ", weather[1])
        print("Относительная влажность: ", weather[2])
        print("Скорость ветра: ", weather[3])
        print("Вероятность осадков сегодня:", precipitation, "%\n")
        print("Брат, посиди дома, не испытывай судьбу..")

asyncio.run(main())


