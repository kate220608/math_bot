import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    last_example_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("example.id"), nullable=True)
    last_example = orm.relationship('Example')
    last_equation_id = sqlalchemy.Column(sqlalchemy.Integer,
                                        sqlalchemy.ForeignKey("equation.id"), nullable=True)
    last_equation = orm.relationship('Equation')