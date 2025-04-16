from datetime import datetime
import requests
from data import db_session
from data.news import News


def fill_db_with_news(serverkey):
    db_sess = db_session.create_session()
    today_day = datetime.now().day
    if today_day % 5 == 0 or db_is_clean():  # Новые новости скачиваем каждые 5 дней или в первый раз, когда запустили сервер
        for new in get_news("stylish_way_1", 0, 9, serverkey):
            db_sess.add(new)
            db_sess.commit()


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
        new = News(text=text, title=text.replace('\n', '')[:31]+'...', img_url=photo_url)
        result.append(new)
    return result


def db_is_clean():
    db_sess = db_session.create_session()
    return True if not db_sess.query(News).all() else False

