# yacut/__init__.py
from flask import Flask
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация расширений
db.init_app(app)

# Импорт Blueprint ПОСЛЕ создания app
from yacut.views import bp as views_bp

# Регистрация Blueprint
app.register_blueprint(views_bp)

# Импорт обработчиков ошибок
from yacut import error_handlers
error_handlers.register_error_handlers(app)

from yacut.api_views import bp_api as api_bp
app.register_blueprint(api_bp, url_prefix='/api')