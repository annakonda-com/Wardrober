import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class WardrobeItem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'wardrobeitems'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("users.id"))
    img_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer)
    # храним idшники поэтому int
    subcategory_id = sqlalchemy.Column(sqlalchemy.Integer)
    season = sqlalchemy.Column(sqlalchemy.String)
    color_id = sqlalchemy.Column(sqlalchemy.Integer)

    user = orm.relationship('User')
