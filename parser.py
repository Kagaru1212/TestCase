import requests
import time
from database.save_in_db import save_vacancy_request


def get_vacancy_count():
    url = "https://api.rabota.ua/vacancy/search"
    headers = {
        'Accept': 'application/json',
    }
    params = {
        'keyWords': 'junior',
        'cityId': 0,  # 0 значит "Вся Украина" согласно документации API
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        total_count = data['total']  # получаем общее число вакансий

        # Сохранение результатов запроса в базу данных
        save_vacancy_request(total_count)
        print("Данные успешно сохранены в базу данных")

        return total_count

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")


if __name__ == "__main__":
    while True:
        get_vacancy_count()
        # Ожидание 1 час (3600 секунд)
        time.sleep(3600)
