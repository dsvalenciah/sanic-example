#bultin library

#external libraries
import pony.orm as pony
from models import User
from pprint import pprint
import json

@pony.db_session
def add_user(name, password):
    new_user = User(
        name = name,
        password = password,
    )

@pony.db_session
def find_user(name, password):
    result = User.get(
        name=name,
        password=password,
    )
    pprint(json.loads(str(result)))
    return result

# encoding alternativo