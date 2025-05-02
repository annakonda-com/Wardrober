import os

from flask import render_template, Flask, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import text
from uuid import uuid4

from data import db_session
from data.users import User
from data.news import News
from data.wardrobe_items import WardrobeItem
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
    return db_sess.query(User).get(user_id)


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
            return redirect("/")
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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/advices')
def advices():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    data = []
    for new in news:
        data.append(new.to_dict())
    return render_template('advices.html', data=data, path=request.path)


@app.route('/advice/<int:id>')
def advice(id):
    db_sess = db_session.create_session()
    new = db_sess.query(News).filter(News.id == id).first().to_dict()
    return render_template('advice.html', page_title=new['title'][:10] + '...', new=new)


@app.route('/wardrobe')
def wardrobe():
    db_sess = db_session.create_session()
    query = text("SELECT id, name FROM colors")
    colors = db_sess.execute(query).fetchall()
    color = list(map(int, request.args.getlist('color')))
    season = request.args.getlist('season')
    return render_template('wardrobe.html', path=request.path,
                           items=get_items_by_filter_main(color, season, db_sess), colors=colors)


@app.route('/wardrobe/<int:category>')
def categories(category):
    db_sess = db_session.create_session()
    query = text("SELECT id, name FROM colors")
    colors = db_sess.execute(query).fetchall()
    color = list(map(int, request.args.getlist('color')))
    season = request.args.getlist('season')
    return render_template('categories.html', items=get_items_by_filter_category(color, season, category, db_sess),
                           path=request.path, colors=colors)


@app.route('/wardrobe/<int:category>/<int:subcategory>')
def subcategories(category, subcategory):
    db_sess = db_session.create_session()
    query = text("SELECT id, name FROM colors")
    colors = db_sess.execute(query).fetchall()
    color = list(map(int, request.args.getlist('color')))
    season = request.args.getlist('season')
    return render_template('subcategories.html',
                           items=get_items_by_filter_subcategory(color, season, subcategory, db_sess),
                           path=request.path, colors=colors)


@app.route('/wardrobe/<int:category>/<int:subcategory>/<int:item_id>')
def item(captegory, subcategory, item_id):
    db_sess = db_session.create_session()
    query = text(
        "SELECT name, img_url FROM wardrobeitems WHERE user_id = :user_id AND id = :item_id")
    items = db_sess.execute(query, {'user_id': current_user.get_id(), 'item_id': item_id}).fetchone()
    return render_template('wardrobe_item.html', path=request.path, name=items[0], url=items[1])


@app.route('/look')
def look():
    return render_template('look.html', path=request.path)


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
        print(color_id, category_id, subcategory_id, form.image.data)
        f = form.image.data
        filename = f.filename.split('.')
        filename = str(uuid4()) + '.' + filename[1]
        f.save(os.path.join(app.root_path, 'data', 'users_images', filename))
        new_item = WardrobeItem(
            user_id=current_user.get_id(),
            name=form.name.data,
            color_id=color_id,
            category_id=category_id,
            subcategory_id=subcategory_id,
            season=form.season.data,
            img_url=filename,
        )
        db_sess.add(new_item)
        db_sess.commit()
        return redirect("/wardrobe")
    else:
        print(form.errors)
    return render_template('add_wardrobe_item.html', title='Добавление вещи', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
