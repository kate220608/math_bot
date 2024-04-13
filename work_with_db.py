from data import db_session
from data.users import User
from data.example import Example
from data.equation import Equation


def add_user(user_id, name):
    db_sess = db_session.create_session()
    if user_not_first_time(user_id):
        return "С возвращением."
    else:
        user = User()
        user.id = user_id
        user.name = name
        user.last_example_id = 0
        user.last_equation_id = 0
        db_sess.add(user)
        db_sess.commit()
        return "Я бот, помогающий решать математические задачи."


def delete_user(user_id):
    db_sess = db_session.create_session()
    db_sess.query(User).filter(User.id == user_id).delete()
    db_sess.commit()


def user_not_first_time(user_id):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == user_id).first():
        return True
    else:
        return False


def last_example_to_user(user_id, type_example):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    example_find = db_sess.query(Example).filter(Example.type == type_example).first()
    if example_find:
        user.last_example_id = example_find.id
    else:
        user.last_example_id = 0
    db_sess.commit()


def last_equation_to_user(user_id, type_equation):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    equation_find = db_sess.query(Equation).filter(Equation.type == type_equation).first()
    if equation_find:
        user.last_equation_id = equation_find.id
    else:
        user.last_equation_id = 0
    db_sess.commit()


def last_example_from_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user.last_example_id != 0:
        return (db_sess.query(Example).filter(Example.id == user.last_example_id).first().type,
                db_sess.query(Example).filter(Example.id == user.last_example_id).first().tasks)
    else:
        return False


def last_equation_from_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user.last_equation_id != 0:
        return (db_sess.query(Equation).filter(Equation.id == user.last_equation_id).first().type,
                db_sess.query(Equation).filter(Equation.id == user.last_equation_id).first().tasks)

    else:
        return False


def all_equations_names():
    db_sess = db_session.create_session()
    return [el.type for el in db_sess.query(Equation).all()]


def all_examples_names():
    db_sess = db_session.create_session()
    return [el.type for el in db_sess.query(Example).all()]


def tasks_for_equation(equation):
    db_sess = db_session.create_session()
    return db_sess.query(Equation).filter(Equation.type == equation).first().tasks


def tasks_for_example(example):
    db_sess = db_session.create_session()
    return db_sess.query(Example).filter(Example.type == example).first().tasks
