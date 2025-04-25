from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired



class AddWardrobeItemForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[DataRequired()])
    category = SelectField('Выберите категорию', choices=['Верх', 'Низ', '...'], coerce=str)
    subcategory = SelectField('Выберите подкатегорию', choices=['Шорты','Футболки', '...'], coerce=str)
    season = SelectField('Выберите сезон', choices=['зима', 'весна', 'лето', 'осень',], coerce=str)
    colors = SelectField('Выберите цвет', choices=['red', 'blue', '...'], coerce=str)
    submit = SubmitField('Добавить')
