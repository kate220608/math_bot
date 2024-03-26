from data import db_session
from data.users import User


def add_user(id, name):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == id).first():
        return "С возвращением."
    else:
        user = User()
        user.id = id
        user.name = name
        db_sess.add(user)
        db_sess.commit()
        return "Я бот, помогающий решать математические задачи."


def delete_user(id):
    db_sess = db_session.create_session()
    db_sess.query(User).filter(User.id == id).delete()
    db_sess.commit()



