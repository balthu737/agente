from flask import Flask
from flask_cors import CORS
import sys
import os
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from routes import api
from models import Request
debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
if not debug:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

sql = Request()

def app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api)
    with app.app_context():
        sql.crear_tablas()
    return app