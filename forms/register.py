from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')