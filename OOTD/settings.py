from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__, instance_relative_config=True)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'project'

# init MySQL
mysql = MySQL(app)