from flask import Flask
import sqlalchemy

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'cs411'

# login_manager = LoginManager()
# login_manager.init_app(app)

gcached_table = {}

app.config.from_pyfile("ootd.cfg")

# init MySQL
def init_connection_engine():
    host = app.config["HOST"]
    driver_name = app.config["DRIVER_NAME"]
    username = app.config["USERNAME"]
    password = app.config["PASSWORD"]
    database = app.config["DATABASE"]
    ssl_args = app.config["SSL_ARGS"]

    sql_url = sqlalchemy.engine.URL(
        host=host,
        drivername=driver_name,
        username=username,
        password=password,
        database=database
    )
    pool = sqlalchemy.create_engine(sql_url, connect_args=ssl_args)
    return pool


db = init_connection_engine()