# bultin library

# external libraries
from pony.orm import select
import pony.orm as pony
from models import User
from pprint import pprint
import hashlib


SALT = 'aslkdfjlaskdjflkhlñwerhl1234khl2kjrlkjlkejrlkwjer'


def hash_password(password):
    return hashlib.md5((SALT + password).encode('utf-8')).hexdigest()


@pony.db_session
def add_user(name, password):
    new_user = User(
        name=name,
        password=hash_password(password),
    )
    return new_user


@pony.db_session
def find_user(name, password):
    user = select(
        u for u in User
        if u.name == name and u.password == hash_password(password)
    ).first()
    pprint(user)
    return user

# encoding alternativo
