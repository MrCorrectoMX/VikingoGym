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
        nombre TEXT,
        telefono TEXT,
        vencimiento TEXT,
        huella TEXT UNIQUE
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

    c.execute("INSERT INTO socios(nombre,telefono,vencimiento,huella) VALUES(?,?,?,?)",
              (nombre, telefono, vencimiento, huella))

    db.commit()
    db.close()


def buscar_por_huella(huella):
    db = conectar()
    c = db.cursor()

    c.execute("SELECT id,nombre,vencimiento FROM socios WHERE huella=?", (huella,))
    dato = c.fetchone()

    db.close()
    return dato


def registrar_asistencia(socio_id, fecha):
    db = conectar()
    c = db.cursor()

    c.execute("INSERT INTO asistencias(socio_id,fecha) VALUES(?,?)", (socio_id, fecha))

    db.commit()
    db.close()