import random
import string
import requests

def generate_token(length=32):
    chars = string.ascii_letters + string.digits  # Включает буквы и цифры
    return ''.join(random.choice(chars) for _ in range(length))
def check_status(token):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"

    try:
        response = requests.get(url,params={"apikey": token})
        if response.status_code == 200:
            print(f"Запрос успешен для токена: {token}")
            return True
        else:
            print(f"Ошибка {response.status_code} для токена: {token}")
            return False
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return False

valid_tokens = []
for _ in range(50):
    token = generate_token()
    if check_status(token):
        valid_tokens.append(token)
print(f"Сгенерированные и проверенные токены: {valid_tokens}")