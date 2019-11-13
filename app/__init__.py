# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_qrcode import QRcode
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# BD
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)
    QRcode(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "Você deve estar logado para acessar essa página"
    login_manager.login_view = "aute.login"

    migrate = Migrate(app, db)

    from app import models

    from .autenticar import aute as aute_blueprint
    app.register_blueprint(aute_blueprint)

    from .func import func as func_blueprint
    app.register_blueprint(func_blueprint, url_prefix='/func')

    from .compra import compra as compra_blueprint
    app.register_blueprint(compra_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
