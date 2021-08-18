from authlib.integrations.flask_client import OAuth
from flask import Flask

from app.config import Config

oauth = OAuth()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    oauth.init_app(app)

    return app
