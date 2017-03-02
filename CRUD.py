# bultin library
from datetime import datetime
from pprint import pprint
from uuid import uuid4


# external libraries
from pony.converting import str2datetime    #noqa
from pony.orm import select
import pony.orm as pony
from models import User, Session
from passlib.hash import pbkdf2_sha256


SALT = "aslkdfjl@@#&/askdjf@@%#$(()(/l2kjrlkjlkejrlkwjer"


def hash_password(password):
    return pbkdf2_sha256.hash(password + SALT)


@pony.db_session
def add_user(email, name, password):
    if name != "" and password != "":
        new_user = User(
            email=email,
            name=name,
            password=hash_password(password),
        )
        return new_user
    else:
        return None


@pony.db_session
def find_user(password, email_or_name):
    user = pony.select(
        u for u in User
        if u.name == email_or_name
        or u.email == email_or_name
    ).first()
    if not user:
        return None
    if pbkdf2_sha256.verify(
        password+SALT,
        user.password,
    ):
        return user


@pony.db_session
def login_user(password, email_or_name):
    user = find_user(password, email_or_name)

    if not user:
        return None

    session = Session(user=user, token=str(uuid4()))
    return session


@pony.db_session
def get_session_by_token(token):
    session, user = pony.select(
        (s, s.user) for s in Session
        if s.token == token and s.user.name
    ).first()
    print(user.name)
    return session, user
