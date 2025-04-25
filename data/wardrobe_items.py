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
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    # храним idшники поэтому int
    subcategory = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subcategories.id"))
    season = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("colors.id"))
