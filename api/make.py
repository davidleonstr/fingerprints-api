from flask import Flask
from api.config import Config, DB
from api.v1.models import *
from flask_cors import CORS

from api.v1 import v1BP

def make() -> Flask:
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(v1BP, url_prefix='/v1')
    app.config.from_object(Config)

    DB.init_app(app)

    return app