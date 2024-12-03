from flask import Flask, render_template, request
import requests
import asyncio
from project import basic_weather, precipitation_probab, check_bad_weather, API_KEY


url = "http://dataservice.accuweather.com/locations/v1/cities/search"
app = Flask(__name__)
#использую новую функцию, поскольку нужно задавать города нужно с клавиатуры
def get_location_key(city_name):
    #объявляем параметры
    params = {"apikey": API_KEY, "q": city_name, "language": "ru-ru", "details":"true"}
    response = requests.get(url, params=params)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["Key"]
    #обрабатываем ошибку
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    #инициализируем переменные, которые будем выводить
    result = None
    error_message = None
    #делаем post-запрос
    if request.method == "POST":
        city1 = request.form.get("city1")
        city2 = request.form.get("city2")
        try:
            key1 = get_location_key(city1)
            key2 = get_location_key(city2)

            if not key1 or not key2:
                raise ValueError("Не удалось найти один из городов")
            weather_url1 = f"http://dataservice.accuweather.com/currentconditions/v1/{key1}"
            forecast_url1 = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{key1}"

            weather_url2 = f"http://dataservice.accuweather.com/currentconditions/v1/{key2}"
            forecast_url2 = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{key2}"
            params = {"apikey": API_KEY, "details": "true"}

            # Берём данные о погоде
            # Используем asyncio, чтобы два запрос обрабатывались одновременно
            async def get_weather_data():
                weather1 = await basic_weather(weather_url1, params)
                precipitation1 = await precipitation_probab(params, forecast_url1)
                weather2 = await basic_weather(weather_url2, params)
                precipitation2 = await precipitation_probab(params, forecast_url2)

                return (weather1, precipitation1), (weather2, precipitation2)
            #Вызываем функции с использование asyncio
            (weather1, precipitation1), (weather2, precipitation2) = asyncio.run(get_weather_data())
            # Получаем результаты о благоприятности погодных условий
            bad_weather1 = check_bad_weather(weather1, precipitation1)
            bad_weather2 = check_bad_weather(weather2, precipitation2)
            # Сравниваем погодные условия в двух городах, чтобы сделать решение о поездке
            if bad_weather1 or bad_weather2:
                result = "Погода плохая, поездку стоит отложить"
            elif bad_weather1 == False and bad_weather2 == False:
                result = "Погода отличная, можно ехать!"
        # Перехватываем все ошибки, чтобы потом отобразить их в случае чего на странице
        except Exception as e:
            error_message = str(e)
    return render_template("index.html", result=result, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)