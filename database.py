import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_db():
    db_path = os.getenv("DATABASE_PATH", "database.db")
    return sqlite3.connect(db_path, check_same_thread=False)

def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            valor REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nombre TEXT,
            api_key TEXT UNIQUE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conn.commit()
    conn.close()

def registrar_usuario(nombre, correo, password):
    conn = conectar_db()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
        (nombre, correo, password_hash)
    )
    conn.commit()
    conn.close()

def login_usuario(correo, password):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, password FROM usuarios WHERE correo=?",
        (correo,)
    )
    row = cursor.fetchone()
    user = None
    if row and check_password_hash(row[2], password):
        user = (row[0], row[1])
    conn.close()
    return user

def guardar_consumo(usuario_id, valor):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO consumo (usuario_id, valor) VALUES (?, ?)",
        (usuario_id, valor)
    )
    conn.commit()
    conn.close()

def obtener_consumos(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT valor, fecha FROM consumo WHERE usuario_id=? ORDER BY fecha DESC",
        (usuario_id,)
    )
    datos = cursor.fetchall()
    conn.close()
    return datos

def crear_dispositivo(usuario_id, nombre, api_key):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dispositivos (usuario_id, nombre, api_key) VALUES (?, ?, ?)",
        (usuario_id, nombre, api_key)
    )
    conn.commit()
    conn.close()

def obtener_usuario_por_api_key(api_key):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT usuario_id FROM dispositivos WHERE api_key=?",
        (api_key,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def listar_dispositivos_usuario(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, api_key FROM dispositivos WHERE usuario_id=?",
        (usuario_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows