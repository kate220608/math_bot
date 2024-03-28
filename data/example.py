import sqlalchemy
from .db_session import SqlAlchemyBase


class Example(SqlAlchemyBase):
    __tablename__ = 'example'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    tasks = sqlalchemy.Column(sqlalchemy.String, nullable=True)