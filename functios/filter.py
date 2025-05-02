from flask_login import current_user
from sqlalchemy import text


def get_items_by_filter_main(color, season, db_sess):
    if color == [] and season == []:
        query = text(
            "SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id")
        return db_sess.execute(query, {'user_id': current_user.get_id()}).fetchall()

    if color != [] and season == []:
        color = tuple(color)
        if len(color) == 1:
            print(color)
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND color_id = :color")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'color': color[0]}).fetchall()
        else:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND color_id IN {color}")
            items = db_sess.execute(query, {'user_id': current_user.get_id()}).fetchall()
        return items

    if color == [] and season != []:
        season = tuple(season)
        if len(season) == 1:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season LIKE :season")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0]}).fetchall()
        else:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season IN {season}")
            items = db_sess.execute(query, {'user_id': current_user.get_id()}).fetchall()
        return items
    if color != [] and season != []:
        color = tuple(color)
        season = tuple(season)
        if len(color) == 1:
            if len(season) == 1:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"LIKE :season AND color_id = :color")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                                'color': color[0]}).fetchall()
            else:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"IN {season} AND color_id = :color")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'color': color[0]}).fetchall()
        else:
            if len(season) == 1:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"LIKE :season AND color_id IN {color}")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0]}).fetchall()
            else:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"IN {season} AND color_id IN {color}")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0]}).fetchall()
        return items


def get_items_by_filter_category(color, season, category_id, db_sess):
    if color == [] and season == []:
        query = text(
            "SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND category_id = :category_id")
        return db_sess.execute(query, {'user_id': current_user.get_id(), 'category_id': category_id}).fetchall()

    if color != [] and season == []:
        color = tuple(color)
        if len(color) == 1:
            print(color)
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND color_id = :color"
                f" AND category_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'color': color[0],
                                            'category_id': category_id}).fetchall()
        else:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND color_id IN {color} "
                f"AND category_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'category_id': category_id}).fetchall()
        return items

    if color == [] and season != []:
        season = tuple(season)
        if len(season) == 1:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season LIKE :season "
                f"AND category_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                            'category_id': category_id}).fetchall()
        else:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season IN {season} "
                f"AND category_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'category_id': category_id}).fetchall()
        return items
    if color != [] and season != []:
        color = tuple(color)
        season = tuple(season)
        if len(color) == 1:
            if len(season) == 1:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"LIKE :season AND color_id = :color AND category_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                                'color': color[0], 'category_id': category_id}).fetchall()
            else:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"IN {season} AND color_id = :color AND category_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'color': color[0],
                                                'category_id': category_id}).fetchall()
        else:
            if len(season) == 1:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"LIKE :season AND color_id IN {color} AND category_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                                'category_id': category_id}).fetchall()
            else:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"IN {season} AND color_id IN {color} AND category_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                                'category_id': category_id}).fetchall()
        return items


def get_items_by_filter_subcategory(color, season, subcategory_id, db_sess):
    if color == [] and season == []:
        query = text(
            "SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND subcategory_id = :category_id")
        return db_sess.execute(query, {'user_id': current_user.get_id(), 'category_id': subcategory_id}).fetchall()

    if color != [] and season == []:
        color = tuple(color)
        if len(color) == 1:
            print(color)
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND color_id = :color"
                f" AND subcategory_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'color': color[0],
                                            'category_id': subcategory_id}).fetchall()
        else:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND color_id IN {color} "
                f"AND subcategory_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'category_id': subcategory_id}).fetchall()
        return items

    if color == [] and season != []:
        season = tuple(season)
        if len(season) == 1:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season LIKE :season "
                f"AND subcategory_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                            'category_id': subcategory_id}).fetchall()
        else:
            query = text(
                f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season IN {season} "
                f"AND subcategory_id = :category_id")
            items = db_sess.execute(query, {'user_id': current_user.get_id(), 'category_id': subcategory_id}).fetchall()
        return items
    if color != [] and season != []:
        color = tuple(color)
        season = tuple(season)
        if len(color) == 1:
            if len(season) == 1:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"LIKE :season AND color_id = :color AND subcategory_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                                'color': color[0], 'category_id': subcategory_id}).fetchall()
            else:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"IN {season} AND color_id = :color AND subcategory_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'color': color[0],
                                                'category_id': subcategory_id}).fetchall()
        else:
            if len(season) == 1:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"LIKE :season AND color_id IN {color} AND subcategory_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                                'category_id': subcategory_id}).fetchall()
            else:
                query = text(
                    f"SELECT id, name, img_url FROM wardrobeitems WHERE user_id = :user_id AND season "
                    f"IN {season} AND color_id IN {color} AND subcategory_id = :category_id")
                items = db_sess.execute(query, {'user_id': current_user.get_id(), 'season': season[0],
                                                'category_id': subcategory_id}).fetchall()
        return items
