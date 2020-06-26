from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object("config.ProductionConfig")
db = SQLAlchemy(app)


from app.routes import *