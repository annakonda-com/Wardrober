from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired


class AddItemInLook(FlaskForm):
    look = SelectField('Выберите образ', coerce=str, validators=[DataRequired()])
    newlookname = StringField('Название')
    submit = SubmitField('Добавить')

    def __init__(self, look_choices=None):
        super(AddItemInLook, self).__init__()
        if look_choices is not None:
            self.look.choices = look_choices
