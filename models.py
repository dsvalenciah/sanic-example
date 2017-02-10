# bultin library
import os

# external libraries
import pony.orm as pony
import json

basedir = os.path.abspath(os.path.dirname(__file__))
PONY_DATABASE_URI = os.path.join(basedir, 'pony.db')

database = pony.Database(
    "sqlite",
    PONY_DATABASE_URI,
    create_db=True
)


class User(database.Entity):

    name = pony.Required(str, unique=True)
    password = pony.Required(str)

    def __repr__(self):
        # return 'User(name={}, password={})'.format...
        return json.dumps(
            {
                "name": self.name,
                "password": self.password,
            }
        )

# enciende el debug
pony.sql_debug(True)

# crea la tabla si no existe
database.generate_mapping(create_tables=True)
