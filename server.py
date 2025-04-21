from flask import render_template, Flask, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.users import User
from functios.fashion_news import fill_db_with_news

from forms.login import LoginForm
from forms.register import RegisterForm

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
    return render_template('advices.html', path=request.path)


@app.route('/wardrobe')
def wardrobe():
    return render_template('wardrobe.html', path=request.path)


@app.route('/look')
def look():
    return render_template('look.html', path=request.path)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
