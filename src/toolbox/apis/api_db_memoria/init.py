from flask import Flask
from flask_cors import CORS
from api_db_memoria.routes import api

def app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api)
    return app