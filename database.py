import sqlite3

DB = "gym.db"

def conectar():
    return sqlite3.connect(DB)

def crear_tablas():
    db = conectar()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS socios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        vencimiento TEXT NOT NULL,
        huella_id TEXT UNIQUE
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS asistencias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        socio_id INTEGER,
        fecha TEXT
    )
    """)

    db.commit()
    db.close()


def registrar_socio(nombre, telefono, vencimiento, huella):
    db = conectar()
    c = db.cursor()
    c.execute(
        "INSERT INTO socios(nombre,telefono,vencimiento,huella_id) VALUES(?,?,?,?)",
        (nombre, telefono, vencimiento, huella)
    )
    db.commit()
    db.close()

from datetime import datetime

def buscar_por_huella(huella):
    db = conectar()
    c = db.cursor()
    c.execute("SELECT id,nombre,vencimiento FROM socios WHERE huella_id=?", (huella,))
    socio = c.fetchone()
    db.close()
    return socio

def registrar_asistencia(socio_id):
    db = conectar()
    c = db.cursor()
    c.execute("INSERT INTO asistencias(socio_id,fecha) VALUES(?,?)",
              (socio_id, datetime.now()))
    db.commit()
    db.close()


def obtener_socios():
    db = conectar()
    c = db.cursor()
    c.execute("SELECT id,nombre,telefono,vencimiento FROM socios ORDER BY nombre")
    datos = c.fetchall()
    db.close()
    return datos


def actualizar_vencimiento(socio_id, nueva_fecha):
    db = conectar()
    c = db.cursor()
    c.execute("UPDATE socios SET vencimiento=? WHERE id=?", (nueva_fecha, socio_id))
    db.commit()
    db.close()
