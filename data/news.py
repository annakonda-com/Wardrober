import sqlalchemy
from .db_session import SqlAlchemyBase

class News(SqlAlchemyBase):
    __tablename__ = 'news'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    img_url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
