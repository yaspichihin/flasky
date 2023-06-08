from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config


# flask-bootstrap для интерфейс и шаблоны похожие на twitter
bootstrap = Bootstrap()

# flask-mail для отправки почты
mail = Mail()

# flask-moment для локализации дат и времени moment.js
moment = Moment()

# flask-sqlalchemy для интеграции с базами данных
db = SQLAlchemy()

# flask-login для управление системой аутентификации
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Регистрация макета main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/")

    # Регистрация макета auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
