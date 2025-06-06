from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired


class AddWardrobeItemForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[FileRequired()])
    category = SelectField('Выберите категорию', choices=[('', '...'),
                                                          ('обувь', 'Обувь'),
                                                          ('комбинезоны', 'Комбинезоны'),
                                                          ('низ', 'Низ'),
                                                          ('платья', 'Платья'),
                                                          ('верх', 'Верх'),
                                                          ('аксессуары', 'Аксессуары')
                                                          ], coerce=str, validators=[DataRequired()])

    subcategory = SelectField('Выберите подкатегорию',
                              choices=['-1', 'шорты', 'юбки', 'спортивные штаны', 'брюки', 'джинсы',
                                       'повседневные', 'вечерние', 'свитера', 'топы',
                                       'футболки', 'водолазки', 'пиджаки',
                                       'рубашки и блузки', 'толстовки', 'жилетки',
                                       'верхняя одежда', 'серьги', 'подвески', 'браслеты',
                                       'очки', 'головной убор', 'туфли', 'демисезонная',
                                       'зимняя', 'летняя'], coerce=str)
    season = SelectField('Выберите сезон', choices=['...','Зима', 'Весна', 'Лето', 'Осень', ], coerce=str)
    colors = SelectField('Выберите цвет', choices=['Белый', 'Чёрный', 'Коричневый', 'Красный', 'Розовый', 'Зелёный',
                                                   'Синий', 'Оранжевый', 'Фиолетовый', 'Серый', 'Жёлтый', 'Бежевый',
                                                   'Разноцветное'], coerce=str)
    submit = SubmitField('Добавить')
