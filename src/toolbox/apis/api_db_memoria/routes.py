from flask import jsonify, Blueprint, request
from api_db_memoria.models import Request
import json

api = Blueprint("api", __name__)
sql = Request()

@api.route("/", methods=["GET"])
def home():
    return jsonify({"message": "La API Funciona correctamente"})

@api.route("/summary", methods=["POST"])
def summary():
    data = request.get_json()
    summary = data.get("summary")
    messages = json.dumps(data.get("messages"))
    try:
        sql.summary(summary, messages)
        return jsonify({"": "","": "" }), 200
    except Exception as e:
        print(e)
        return jsonify({"": "","": "" }), 400

@api.route("/summary/count", methods=["GET"])
def count():
    count = sql.summary_count()
    return jsonify({"message": "Total de resumenes", "count": count[0][0] }), 200