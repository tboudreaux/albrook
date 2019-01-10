from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


from app import models, interfaces
