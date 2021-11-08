from flask import Flask
# from flask_mysqldb import MySQL
import sqlalchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/project'


# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
# app.config['MYSQL_DB'] = 'project'

# init MySQL
def init_connection_engine():
    pool = sqlalchemy.create_engine('mysql://root:123456@localhost/project')

        # sqlalchemy.engine.url.URL(
        #     drivername='mysql',
        #     username='root',
        #     password='123456',
        #     database='project',
        #     host='localhost'
        # )
    #)

    return pool


db = init_connection_engine()

# if __name__ == '__main__':
#     app.run(debug=True)
