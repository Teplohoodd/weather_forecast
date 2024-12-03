import random
import string
import requests


# Функция генерации случайного токена
def generate_token(length=32):
    chars = string.ascii_letters + string.digits  # Включает буквы и цифры
    return ''.join(random.choice(chars) for _ in range(length))


# Функция для проверки статуса запроса
def check_status(token):
    # Замените на URL API, который вы хотите использовать для проверки
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"

    try:
        response = requests.get(url,params={"apikey": token})

        # Проверка на успешный статус
        if response.status_code == 200:
            print(f"Запрос успешен для токена: {token}")
            return True
        else:
            print(f"Ошибка {response.status_code} для токена: {token}")
            return False
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return False


# Генерация и проверка 20 токенов
valid_tokens = []
for _ in range(50):
    token = generate_token()
    if check_status(token):
        valid_tokens.append(token)

print(f"Сгенерированные и проверенные токены: {valid_tokens}")