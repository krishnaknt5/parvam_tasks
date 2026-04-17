import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from config import Config
from models.db import mysql

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

from routes.auth import auth_bp
from routes.dashboard import dash_bp
from routes.student import student_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(student_bp)

if __name__ == "__main__":
    app.run(debug=True)