import sqlalchemy
from .db_session import SqlAlchemyBase


class Pictures(SqlAlchemyBase):
    __tablename__ = 'pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.BLOB, nullable=False)
