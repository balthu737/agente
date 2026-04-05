from flask import jsonify, Blueprint
from app.models import Request

api = Blueprint("api", __name__)
sql = Request()

@api.route("/", methods=["GET"])
def home():
    return jsonify({"message": "La API Funciona correctamente"})

