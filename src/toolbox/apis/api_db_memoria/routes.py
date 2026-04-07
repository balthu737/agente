from flask import jsonify, Blueprint, request
import requests
import json
from dotenv import load_dotenv
import os
from memoria.long_memory import LongMemory
from models import Request

load_dotenv()

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
    url = os.getenv("API_URL")
    try:
        sql.summary_post(summary, messages)
        count = sql.summary_count()
        pa = count[0][0] % 2
        if pa == 0 :
            print(f"Disparando experience, count: {count[0][0]}")
            requests.post(url+"/experience", json={"old_summarys": summary})
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
    old_summarys = json.dumps(data.get("old_summarys"))
    experience = memory.experience_memory(old_summarys)
    sql.experience_post(experience, old_summarys)
    return jsonify({"message": "Experiencia creada", "summaris": old_summarys, "experience": experience}), 200