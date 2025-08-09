from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)

from . import models, error_handlers, views, api_views
from flask_migrate import Migrate
migrate = Migrate(app, db)
app.register_blueprint(views.bp, url_prefix='/')
app.register_blueprint(api_views.bp_api)
error_handlers.register_error_handlers(app)