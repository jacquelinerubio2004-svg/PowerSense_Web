from flask import Flask, render_template, request, redirect, session, jsonify
from database import *
import uuid
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "powersense_secret_dev")

ALERTA_CONSUMO = 800  # ⚠️ consumo alto

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        user = login_usuario(correo, password)
        if user:
            session["user_id"] = user[0]
            session["nombre"] = user[1]
            return redirect("/dashboard")
        else:
            return "Correo o contraseña incorrectos"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        registrar_usuario(
            request.form["nombre"],
            request.form["correo"],
            request.form["password"]
        )
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    consumos = obtener_consumos(session["user_id"])
    consumo_actual = consumos[0][0] if consumos else 0

    alerta = consumo_actual >= ALERTA_CONSUMO

    return render_template(
        "dashboard.html",
        nombre=session["nombre"],
        consumo=consumo_actual,
        alerta=alerta,
        historial=consumos
    )


@app.route("/devices")
def devices():
    if "user_id" not in session:
        return redirect("/")
    dispositivos = listar_dispositivos_usuario(session["user_id"])
    return render_template("devices.html", dispositivos=dispositivos)


@app.route("/devices/add", methods=["POST"])
def add_device():
    if "user_id" not in session:
        return redirect("/")
    nombre = request.form.get("nombre", "Mi dispositivo")
    api_key = str(uuid.uuid4())
    crear_dispositivo(session["user_id"], nombre, api_key)
    return redirect("/devices")


@app.route("/api/consumo", methods=["POST"])
def api_consumo():
    # Accept JSON or form data: {"api_key": "...", "valor": 123}
    data = request.get_json(silent=True) or request.form
    api_key = data.get("api_key")
    valor = data.get("valor")
    if not api_key or valor is None:
        return jsonify({"ok": False, "error": "api_key y valor requeridos"}), 400

    try:
        valor = float(valor)
    except Exception:
        return jsonify({"ok": False, "error": "valor inválido"}), 400

    usuario_id = obtener_usuario_por_api_key(api_key)
    if not usuario_id:
        return jsonify({"ok": False, "error": "api_key no registrado"}), 403

    guardar_consumo(usuario_id, valor)
    return jsonify({"ok": True})

@app.route("/add_consumo")
def add_consumo():
    if "user_id" in session:
        guardar_consumo(session["user_id"], 650)
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    crear_tablas()
    host = os.getenv("HOST", "127.0.0.1")
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(host=host, debug=debug)
