from flask import Flask, request
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import socket


app = Flask(__name__)
login = LoginManager(app)
app.config.from_object(Config)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
db = SQLAlchemy(app)

from web.utils import clear_user_space
clear_user_space()

from web import routes, models
