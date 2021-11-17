from flask import Flask
import sqlalchemy


app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'cs411'


# init MySQL
def init_connection_engine():
    pool = sqlalchemy.create_engine('mysql://root:123456@localhost/project')
    return pool


db = init_connection_engine()

