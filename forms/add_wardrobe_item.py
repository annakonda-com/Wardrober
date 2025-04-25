from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired


class AddWardrobeItemForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    image = FileField('Загрузить фото', validators=[DataRequired()])
    category = SelectField('Выберите категорию', choices=['обувь', 'комбинезоны', 'низ',
                                                          'платья', 'верх', 'аксессуары'], coerce=str)
    subcategory = SelectField('Выберите подкатегорию', choices=['шорты', 'юбки', 'спортивные штаны', 'брюки', 'джинсы',
                                                                'повседневные', 'вечерние', 'свитера', 'топы',
                                                                'футболки', 'водолазки', 'пиджаки',
                                                                'рубашки и блузки', 'толстовки', 'жилетки',
                                                                'верхняя одежда', 'серьги', 'подвески', 'браслеты',
                                                                'очки', 'головной убор', 'туфли', 'демисезонная',
                                                                'зимняя', 'летняя'], coerce=str)
    season = SelectField('Выберите сезон', choices=['зима', 'весна', 'лето', 'осень', ], coerce=str)
    colors = SelectField('Выберите цвет', choices=['Белый', 'Чёрный', 'Коричневый', 'Красный', 'Розовый', 'Зелёный',
                                                   'Синий', 'Оранжевый', 'Фиолетовый', 'Серый', 'Жёлтый', 'Бежевый',
                                                   'Разноцветное'], coerce=str)
    submit = SubmitField('Добавить')
