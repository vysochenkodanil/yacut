from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

from . import models, error_handlers, views, api_views

error_handlers.register_error_handlers(app)