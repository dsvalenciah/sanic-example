# bultin library
from uuid import uuid4
import re

# external libraries
from pony.converting import str2datetime  # noqa
import pony.orm as pony
from models import User, Session
from passlib.hash import pbkdf2_sha256


SALT = "aslkdfjl@@#&/askdjf@@%#$(()(/l2kjrlkjlkejrlkwjer"


def hash_password(password):
    return pbkdf2_sha256.hash(password + SALT)


def check_format(regex, string):
    if string:
        match = re.match(regex, string)
        if match:
            return match.group(0)
    return ""


def valid_data(name, email):
    name = check_format(r"^(\w{4,15})$", name.strip())
    email = check_format(r"^(?P<user>[A-Za-z](\.?[\w\-]+))+@(?P<domain>[A-Za-z0-9](\.?[A-Za-z0-9\-]+)+\.[A-Za-z]{2,})$",
        email.strip())
    return name, email


@pony.db_session
def add_user(email, name, password):
    name, email = valid_data(name, email)
    if name != "" and password != "" and email:
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
        if u.name == email_or_name or u.email == email_or_name
    ).first()
    if not user:
        return None
    if pbkdf2_sha256.verify(
        password + SALT,
        user.password,
    ):
        return user


@pony.db_session
def login_user(password, email_or_name, expires):
    user = find_user(password, email_or_name)

    if not user:
        return None

    session = Session(user=user, token=str(uuid4()), expires=expires)
    return session


@pony.db_session
def get_session_by_token(token):
    session, user_id = pony.select(
        (s, s.user.id) for s in Session
        if s.token == token
    ).first()
    if not session:
        return None
    return session, User[user_id]
