import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

from werkzeug.security import generate_password_hash, check_password_hash


class WardrobeItem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'wardrobeitems'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("users.id"))
    img_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer)#, sqlalchemy.ForeignKey("categories.id"))
    # храним idшники поэтому int
    subcategory_id = sqlalchemy.Column(sqlalchemy.Integer)#, sqlalchemy.ForeignKey("subcategories.id"))
    season = sqlalchemy.Column(sqlalchemy.String)#, nullable=True)
    color_id = sqlalchemy.Column(sqlalchemy.Integer)#, sqlalchemy.ForeignKey("colors.id"))

    user = orm.relationship('User')
