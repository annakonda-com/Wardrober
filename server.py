import os

from flask import render_template, Flask, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import text
from uuid import uuid4

from data import db_session
from data.complect import Complect
from data.users import User
from data.news import News
from data.wardrobe_items import WardrobeItem
from forms.add_item_in_look import AddItemInLook
from forms.add_wardrobe_item import AddWardrobeItemForm
from functios.fashion_news import fill_db_with_news

from forms.login import LoginForm
from forms.register import RegisterForm
from functios.filter import get_items_by_filter_main, get_items_by_filter_category, get_items_by_filter_subcategory

app = Flask(__name__)
app.config['VK_APIKEY'] = 'YJYrGlxEqNSv2B5CjYUy'
app.config['VK_SERVICEKEY'] = 'd7838b4cd7838b4cd7838b4c41d4acc841dd783d7838b4cb078efc3eb7a1bdd2bfce598'
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/wardrober.db")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user_id = db_sess.query(User).get(user_id)
    db_sess.close()
    return user_id


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect("/")
        db_sess.close()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def index():
    fill_db_with_news(app.config['VK_SERVICEKEY'])
    return render_template('index.html', path=request.path)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_repeat.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            login=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/advices')
def advices():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    data = []
    for new in news:
        data.append(new.to_dict())
    db_sess.close()
    return render_template('advices.html', data=data, path=request.path)


@app.route('/advice/<int:id>')
def advice(id):
    db_sess = db_session.create_session()
    new = db_sess.query(News).filter(News.id == id).first().to_dict()
    db_sess.close()
    return render_template('advice.html', page_title=new['title'][:10] + '...', new=new, path=request.path)


@app.route('/wardrobe', methods=['GET', 'POST'])
def wardrobe():
    item_id = request.args.get('id')
    db_sess = db_session.create_session()
    if item_id:
        query = text(f"DELETE FROM complect_items WHERE wardrobe_item_id={item_id}")
        db_sess.execute(query)
        query = text(f"DELETE FROM wardrobeitems WHERE id={item_id}")
        db_sess.execute(query)
        db_sess.commit()
    query = text("SELECT id, name FROM colors")
    colors = db_sess.execute(query).fetchall()
    color = list(map(int, request.args.getlist('color')))
    season = request.args.getlist('season')
    db_sess.close()
    return render_template('wardrobe.html', path=request.path,
                           items=get_items_by_filter_main(color, season, db_sess), colors=colors)


@app.route('/wardrobe/card_of_thing/<int:item_id>')
def card_of_thing(item_id):
    db_sess = db_session.create_session()
    query = text(
        f"SELECT name, color_id, category_id, subcategory_id, season, img_url FROM wardrobeitems WHERE id = {item_id}")
    items = db_sess.execute(query).fetchone()
    itt = [items[0]]
    query = text(f"SELECT name FROM colors WHERE id = {items[1]}")
    itt.append(db_sess.execute(query).fetchone()[0].lower())
    query = text(f"SELECT name FROM categories WHERE id = {items[2]}")
    itt.append(db_sess.execute(query).fetchone()[0])
    if items[3] != -1:
        query = text(f"SELECT name FROM subcategories WHERE id = {items[3]}")
        itt.append(db_sess.execute(query).fetchone()[0])
    else:
        itt.append(-1)
    itt.append(items[-2].lower())
    itt.append(items[-1].lower())
    db_sess.close()
    return render_template('card_of_thing.html', path=request.path, item=itt, item_id=item_id)


@app.route('/wardrobe/<int:category>')
def categories(category):
    db_sess = db_session.create_session()
    query = text("SELECT id, name FROM colors")
    colors = db_sess.execute(query).fetchall()
    color = list(map(int, request.args.getlist('color')))
    season = request.args.getlist('season')
    db_sess.close()
    return render_template('categories.html', items=get_items_by_filter_category(color, season, category, db_sess),
                           path=request.path, colors=colors)


@app.route('/wardrobe/<int:category>/<int:subcategory>')
def subcategories(category, subcategory):
    db_sess = db_session.create_session()
    query = text("SELECT id, name FROM colors")
    colors = db_sess.execute(query).fetchall()
    color = list(map(int, request.args.getlist('color')))
    season = request.args.getlist('season')
    db_sess.close()
    return render_template('subcategories.html',
                           items=get_items_by_filter_subcategory(color, season, subcategory, db_sess),
                           path=request.path, colors=colors)


@app.route('/wardrobe/<int:category>/<int:subcategory>/<int:item_id>')
def item(captegory, subcategory, item_id):
    db_sess = db_session.create_session()
    query = text(
        "SELECT name, img_url FROM wardrobeitems WHERE user_id = :user_id AND id = :item_id")
    items = db_sess.execute(query, {'user_id': current_user.get_id(), 'item_id': item_id}).fetchone()
    db_sess.close()
    return render_template('wardrobe_item.html', path=request.path, name=items[0], url=items[1])


@app.route('/look', methods=['GET', 'POST'])
def look():
    type = request.args.get('type')
    db_sess = db_session.create_session()
    if type:
        query = text(f"DELETE FROM complect_items WHERE complect_id=:look_id")
        db_sess.execute(query, {'look_id': int(type)})
        query = text(f"DELETE FROM complects WHERE id=:look_id")
        db_sess.execute(query, {'look_id': int(type)})
        db_sess.commit()
    query = text(
        "SELECT id, name FROM complects WHERE user_id = :user_id")
    complects = db_sess.execute(query, {'user_id': current_user.get_id()}).fetchall()
    db_sess.close()
    return render_template('look.html', path=request.path, complects=complects)


@app.route('/look/<int:comp_id>', methods=['GET', 'POST'])
def look_items(comp_id):
    type = request.args.get('type')
    db_sess = db_session.create_session()
    if type:
        query = text(f"DELETE FROM complect_items WHERE complect_id=:look_id")
        db_sess.execute(query, {'look_id': int(comp_id)})
        db_sess.commit()
    query = text(
        "SELECT id, name FROM complects WHERE user_id = :user_id")
    complects = db_sess.execute(query, {'user_id': current_user.get_id()}).fetchall()
    query = text(
        "SELECT wardrobeitems.id, wardrobeitems.name, "
        "wardrobeitems.img_url FROM complect_items "
        "JOIN wardrobeitems ON wardrobeitems.id = complect_items.wardrobe_item_id "
        "WHERE complect_items.complect_id = :comp_id")
    items = db_sess.execute(query, {'comp_id': comp_id}).fetchall()
    query = text("SELECT id from complects WHERE user_id = :user_id AND name LIKE 'Сегодняшний образ'")
    today_look_id = db_sess.execute(query, {'user_id': current_user.get_id()}).fetchone()
    db_sess.close()
    return render_template('look.html', path=request.path, items=items, complects=complects,
                           look_id=comp_id, today_look_id=today_look_id[0])


@app.route('/look/card_of_thing/<int:item_id>')
def look_item(item_id):
    look_id = request.args.get('look_id')
    db_sess = db_session.create_session()
    query = text(
        f"SELECT name, color_id, category_id, subcategory_id, season, img_url FROM wardrobeitems WHERE id = {item_id}")
    items = db_sess.execute(query).fetchone()
    itt = [items[0]]
    query = text(f"SELECT name FROM colors WHERE id = {items[1]}")
    itt.append(db_sess.execute(query).fetchone()[0].lower())
    query = text(f"SELECT name FROM categories WHERE id = {items[2]}")
    itt.append(db_sess.execute(query).fetchone()[0])
    if items[3] != -1:
        query = text(f"SELECT name FROM subcategories WHERE id = {items[3]}")
        itt.append(db_sess.execute(query).fetchone()[0])
    else:
        itt.append(-1)
    itt.append(items[-2].lower())
    itt.append(items[-1].lower())
    return render_template('card_of_thing_look.html', item=itt, path=request.path, item_id=item_id, look_id=look_id)


@app.route('/add_wardrobe_item', methods=['GET', 'POST'])
def add_wardrobe_item():
    form = AddWardrobeItemForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        query = text("SELECT id FROM colors WHERE name = :color_name")
        color_id = db_sess.execute(query, {'color_name': form.colors.data.title()}).fetchone()[0]
        query = text("SELECT id FROM categories WHERE name = :category_name")
        category_id = db_sess.execute(query, {'category_name': form.category.data.lower()}).fetchone()[0]
        if form.subcategory.data != '-1':
            query = text("SELECT id FROM subcategories WHERE name = :subcategory_name")
            subcategory_id = db_sess.execute(query, {'subcategory_name': form.subcategory.data.lower()}).fetchone()[0]
        else:
            subcategory_id = -1
        f = form.image.data
        filename = f.filename.split('.')
        filename = str(uuid4()) + '.' + filename[-1]
        f.save(os.path.join(app.root_path, 'static', 'users_images', filename))
        if form.season.data == '...':
            season = 'a'
        else:
            season = form.season.data
        new_item = WardrobeItem(
            user_id=current_user.get_id(),
            name=form.name.data,
            color_id=color_id,
            category_id=category_id,
            subcategory_id=subcategory_id,
            season=season,
            img_url=filename,
        )
        db_sess.add(new_item)
        db_sess.commit()
        db_sess.close()
        return redirect("/wardrobe")
    return render_template('add_wardrobe_item.html', title='Добавление вещи', form=form)


@app.route('/add_item_in_look', methods=['GET', 'POST'])
def add_item_in_look():
    item_id = request.args.get('id')
    db_sess = db_session.create_session()
    query = text("SELECT name FROM complects WHERE user_id = :user_id")
    looks = [el[0] for el in list(db_sess.execute(query, {'user_id': current_user.get_id()}).fetchall())]
    look_choices = [('', '...'), ('newlook', 'Новый образ')]
    if not looks:
        new_look = Complect(
            user_id=current_user.get_id(),
            name="Сегодняшний образ",
        )
        db_sess.add(new_look)
        db_sess.commit()
        look_choices.append(('Сегодняшний образ', 'Сегодняшний образ'))
    else:
        for el in looks:
            look_choices.append((el, el))
    form = AddItemInLook(look_choices=look_choices)
    query = text("SELECT name FROM wardrobeitems WHERE id = :item_id")
    item_name = db_sess.execute(query, {'item_id': item_id}).fetchone()[0]
    if form.validate_on_submit():
        if form.look.data == 'newlook':
            if form.newlookname.data in looks:
                return render_template('add_item_in_look.html', title='Добавление вещи в образ',
                                       form=form, message="Образ с таким названием уже есть")
            if form.newlookname.data == '':
                return render_template('add_item_in_look.html', title='Добавление вещи в образ',
                                       form=form, message="Название не может отсутствовать")
            new_look = Complect(
                user_id=current_user.get_id(),
                name=form.newlookname.data,
            )
            db_sess.add(new_look)
            db_sess.commit()
            query = text("SELECT id FROM complects WHERE name = :complect_name AND user_id = :user_id")
            look_id = db_sess.execute(query, {'complect_name': form.newlookname.data,
                                              'user_id': current_user.get_id()}).fetchone()[0]
        else:
            query = text("SELECT id FROM complects WHERE name = :complect_name AND user_id = :user_id")
            look_id = \
                db_sess.execute(query, {'complect_name': form.look.data, 'user_id': current_user.get_id()}).fetchone()[
                    0]
        query = text('INSERT INTO complect_items (complect_id, wardrobe_item_id)  VALUES (:look_id, :item_id);')
        db_sess.execute(query, {'look_id': int(look_id), 'item_id': int(item_id)})
        db_sess.commit()
        db_sess.close()
        return redirect("/wardrobe")
    db_sess.close()
    return render_template('add_item_in_look.html', title='Добавление вещи в образ', form=form,
                           item_name=item_name)


@app.route('/del_item_from_look', methods=['GET', 'POST'])
def del_item_from_look():
    item_id = request.args.get('item_id')
    look_id = request.args.get('look_id')
    db_sess = db_session.create_session()
    query = text(f"DELETE FROM complect_items WHERE wardrobe_item_id=:item_id AND complect_id=:look_id")
    db_sess.execute(query, {'item_id': int(item_id), 'look_id': int(look_id)})
    db_sess.commit()
    db_sess.close()
    return redirect('/look/' + str(look_id))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
