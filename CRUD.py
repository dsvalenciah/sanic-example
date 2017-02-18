# bultin library
from pprint import pprint
# external libraries
from pony.orm import select
import pony.orm as pony
from models import User
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
        return False


@pony.db_session
def find_user(password, email_or_name):
    user = pony.select(
        u for u in User
        if u.name == email_or_name
        or u.email == email_or_name
    ).first()
    if not user:
        return False
    if pbkdf2_sha256.verify(
        password+SALT,
        user.password,
    ):
        return user
