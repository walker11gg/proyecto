from flask import Flask, request, jsonify, render_template # para crear la app web y manejar solicitudes
import json # para manejar datos en formato JSON (base de datos)
import os # para manejar rutas de archivos interactuando con el sistema operativo
import bcrypt # para hashear contraseñas
import random # para generar IDs únicos

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"))

#funcion para obtener la ruta completa de un archivo JSON
def ruta_json(nombre):
    return os.path.join(BASE_DIR, "data", nombre)

#funcion para cargar usuarios desde un archivo JSON
def cargar_usuarios():
    try:
        with open("data/usuarios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
#funcion para guardar usuarios en un archivo JSON
def guardar_usuarios(lista):
    with open(ruta_json("usuarios.json"), "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)
    
# funcion para hashear contraseñas
def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

#funcion para verificar contraseñas
def verificar_password(password_plano, password_hash):
    return bcrypt.checkpw(password_plano.encode("utf-8"), password_hash.encode("utf-8"))

#funcion para generar un ID unico
def generar_id_unico(usuarios):
    while True: # Bucle hasta encontrar un ID único
        nuevo_id = str(random.randint(10**9, 10**10 - 1))  # Genera un ID de 10 dígitos
        if not any(u["id"]== nuevo_id for u in usuarios): # Verifica si el ID ya existe
            return nuevo_id # Retorna el ID único


# ==== RUTAS ====
@app.route("/") # RUTA DEL LOGIN
def login_page():
    return render_template("login.html")

@app.route("/registrar") # RUTA DE REGISTRO
def pagina_registro():
    return render_template("register.html")

# ==== API PARA LOGIN ====
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["email"] == email:
            if verificar_password(password, u["password"]):
                return jsonify({
                    "success": True,
                    "mensaje": "Login correcto",
                    "rol": u["rol"]
                })
            else:
                return jsonify({"success": False, "mensaje": "Contraseña incorrecta"})

    return jsonify({"success": False, "mensaje": "Usuario no encontrado"})

# ==== API PARA REGISTRO DE USUARIOS ====
@app.route("/api/registrar", methods=["POST"])
def registrar_usuario():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    rol = data.get("rol", "cliente")  # por defecto el rol será cliente

    if not email or not password:
        return jsonify({"success": False, "message": "Faltan datos obligatorios"}), 400

    usuarios = cargar_usuarios()

    # Verificar si el correo ya está registrado
    for u in usuarios:
        if u["email"].lower() == email.lower():
            return jsonify({"success": False, "message": "El correo ya está registrado"}), 400

    # Crear nuevo ID incremental
    nuevo_id = generar_id_unico(usuarios)
    # Crear usuario
    nuevo_usuario = {
        "id": nuevo_id,
        "email": email,
        "password": hash_password(password),  # ← HASH AQUÍ
        "rol": rol
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)

    return jsonify({"success": True, "message": "Usuario registrado correctamente"})
 
if __name__ == "__main__": # ejecuta la app
    app.run(debug=True)