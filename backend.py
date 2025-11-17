import json 
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

DB_PATH = "database.json"

# Cargar datos
def cargar_datos():
    with open(DB_PATH, "r") as f:
        return json.load(f)

# Guardar datos
def guardar_datos(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Obtener eventos
@app.route("/api/eventos", methods=["GET"])
def obtener_eventos():
    data = cargar_datos()
    return jsonify(data["eventos"])

# Agregar un evento
@app.route("/api/eventos", methods=["POST"])
def agregar_evento():
    data = cargar_datos()
    nuevo_evento = request.get_json()
    nuevo_evento["id"] = len(data["eventos"]) + 1
    data["eventos"].append(nuevo_evento)
    guardar_datos(data)
    return jsonify({"mensaje": "Evento agregado correctamente"}), 201

if __name__ == "__main__":
    app.run(debug=True)