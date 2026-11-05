import os
import re
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")
LOG_PATH = os.path.join(BASE_DIR, "eventos.log")

app = Flask(__name__)


@app.route("/")
def inicio():
    return "Laboratorio de Ciberseguridad"


def validar_usuario(usuario):
    return re.fullmatch(r"[A-Za-z0-9_]{4,20}", usuario) is not None


def validar_correo(correo):
    return re.fullmatch(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        correo
    ) is not None


def validar_password(password):
    return len(password) >= 8


def registrar_evento(tipo, usuario):
    # Se sanitiza el nombre de usuario para evitar inyección de registros en el log (CWE-117)
    usuario_seguro = re.sub(r"[^A-Za-z0-9_]", "_", usuario)[:50]
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_PATH, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},{tipo},{usuario_seguro}\n")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")

        if not validar_usuario(usuario):
            return "Usuario inválido"

        if not validar_correo(correo):
            return "Correo electrónico inválido"

        if not validar_password(password):
            return "La contraseña debe contener al menos 8 caracteres"

        conexion = sqlite3.connect(DB_PATH)
        try:
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT id FROM usuarios WHERE usuario = ? OR correo = ?",
                (usuario, correo)
            )

            if cursor.fetchone():
                return "El usuario o correo ya está registrado"

            password_hash = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)",
                (usuario, correo, password_hash)
            )

            conexion.commit()
        finally:
            conexion.close()

        return "Usuario registrado"

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        conexion = sqlite3.connect(DB_PATH)
        try:
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT password FROM usuarios WHERE usuario = ?",
                (usuario,)
            )

            resultado = cursor.fetchone()
        finally:
            conexion.close()

        if resultado and check_password_hash(resultado[0], password):
            registrar_evento("LOGIN_CORRECTO", usuario)
            return "Inicio de sesión correcto"

        registrar_evento("LOGIN_FALLIDO", usuario)
        return "Credenciales incorrectas"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
