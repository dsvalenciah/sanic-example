# bultin library
import datetime
import os

# external libraries
from pony.converting import str2datetime    #noqa
import pony.orm as pony


basedir = os.path.abspath(os.path.dirname(__file__))
PONY_DATABASE_URI = os.path.join(basedir, 'pony.db')


def default_expires():
    return datetime.datetime.now() + datetime.timedelta(seconds=60)

database = pony.Database(
    "sqlite",
    PONY_DATABASE_URI,
    create_db=True
)


class User(database.Entity):
    email = pony.Required(str, unique=True)
    name = pony.Required(str, unique=True)
    password = pony.Required(str)
    sessions = pony.Set('Session')


class Session(database.Entity):
    user = pony.Required(User)
    token = pony.Required(str, unique=True)
    expires = pony.Required(datetime.datetime,
                            default=default_expires)


pony.sql_debug(True)
database.generate_mapping(create_tables=True)
