from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)

from flask_migrate import Migrate

from . import api_views, error_handlers, models, views

migrate = Migrate(app, db)
app.register_blueprint(views.bp, url_prefix='/')
app.register_blueprint(api_views.bp_api)
error_handlers.register_error_handlers(app)