from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired



class AddWardrobeItemForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[DataRequired()])
    category = SelectField('Выберите категорию', choices=['верх', 'низ', '...'], coerce=str)
    subcategory = SelectField('Выберите подкатегорию', choices=['шорты','футболки', '...'], coerce=str)
    season = SelectField('Выберите сезон', choices=['зима', 'весна', 'лето', 'осень',], coerce=str)
    colors = SelectField('Выберите цвет', choices=['Красный', 'blue', '...'], coerce=str)
    submit = SubmitField('Добавить')
