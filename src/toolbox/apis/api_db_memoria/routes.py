from flask import jsonify, Blueprint, request
from api_db_memoria.models import Request
import json
from memoria.long_memory import LongMemory

api = Blueprint("api", __name__)
sql = Request()
memory = LongMemory()

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
        return jsonify({"message": "resumen guardado"}), 200
    except Exception as e:
        print(e)
        return jsonify({"messages": "no se guardo el resumen"}), 400

@api.route("/summary/count", methods=["GET"])
def count():
    count = sql.summary_count()
    return jsonify({"message": "Total de resumenes", "count": count[0][0] }), 200

@api.route("/experience", methods=["POST"])
def experience():
    data = request.get_json()
    old_summarys = data.get("old_summarys")
    experience = memory.experience_memory(old_summarys)
    sql.experience_post(experience, old_summarys)
    return jsonify({"message": "Experiencia creada", "summaris": old_summarys, "experience": experience}), 200