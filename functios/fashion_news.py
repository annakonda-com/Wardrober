from datetime import datetime
from server import app
import requests


def fill_db_with_news(): # Моя идея в том, чтобы импортировать эту функцию в server.py и запускать каждый раз, когда человек заходит на главную страницу.
    today_day = datetime.now().day

    if today_day % 5 == 0 or db_is_clean():  # Новые новости скачиваем каждые 5 дней или в первый раз, когда запустили сервер
        # Здесь нужно записать инфу полученную с помощью get_news в базу данных. Возможно, get_news должна возвращать сразу объект для базы данных
        print(get_news("stylish_way_1", 0, 2, app.config['VK_SERVICEKEY']))


def get_news(domain, offset, count, service_api_key):
    response = requests.get(
        f"https://api.vk.ru/method/wall.get?access_token={service_api_key}&v=5.199&domain={domain}&offset={offset}&count={count}").json()
    result = list()
    for item in response["response"]["items"]:
        try:
            photo_url = item["attachments"][0]["photo"]["orig_photo"]["url"]
        except Exception:
            photo_url = "/static/img/pass.jpg"
        try:
            text = item["text"]
        except Exception:
            text = ("Мода – это не просто одежда, это яркое проявление культуры и времени. В современном обществе мода "
                    "играет ключевую роль, отражая социальные и культурные тенденции, а также предоставляя средства для "
                    "самовыражения и идентичности. В этом эссе мы исследуем значение моды, анализируя текущие тренды и "
                    "стиль, чтобы понять, как они формируют современную культуру. Мода – это зеркало, в котором "
                    "отражается динамично меняющийся мир, и мы рассмотрим, как она влияет на наше восприятие себя и "
                    "окружающего нас мира. Это путешествие по миру моды поможет нам лучше понять её влияние на культуру "
                    "и общество.")
        info = dict()
        info["img"] = photo_url
        info["text"] = text
        result.append(info)
    return result


def db_is_clean():  # Не хочу пока возиться с базой данных. В этой функции должна проходить проверка на пустоту бд
    return True

fill_db_with_news()
