import sqlalchemy
from .db_session import SqlAlchemyBase


class Equation(SqlAlchemyBase):
    __tablename__ = 'equation'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    tasks = sqlalchemy.Column(sqlalchemy.String, nullable=True)