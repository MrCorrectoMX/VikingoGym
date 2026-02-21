import sqlite3

DB = "gym_v2.db"

def conectar():
    db = sqlite3.connect(DB)
    # Esto permite que SQLite use llaves foráneas (importante)
    db.execute("PRAGMA foreign_keys = ON")
    return db

def crear_tablas():
    db = conectar()
    c = db.cursor()

    # 1. Tabla de Socios (Datos maestros)
    c.execute("""
    CREATE TABLE IF NOT EXISTS socios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        huella TEXT UNIQUE,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        activo INTEGER DEFAULT 1
    )
    """)

    # 2. Tabla de Membresías
    c.execute("""
    CREATE TABLE IF NOT EXISTS membresias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        socio_id INTEGER,
        fecha_inicio DATE NOT NULL,
        fecha_vencimiento DATE NOT NULL,
        monto_pagado REAL,
        FOREIGN KEY (socio_id) REFERENCES socios(id) ON DELETE CASCADE
    )
    """)

    # 3. Tabla de Asistencias
    c.execute("""
    CREATE TABLE IF NOT EXISTS asistencias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        socio_id INTEGER,
        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (socio_id) REFERENCES socios(id) ON DELETE CASCADE
    )
    """)

    db.commit()
    db.close()
    print(f"¡Éxito! La base de datos '{DB}' ha sido creada o actualizada.")

def obtener_estado_socio(huella):
    db = conectar()
    c = db.cursor()
    query = """
    SELECT s.id, s.nombre, m.fecha_vencimiento 
    FROM socios s
    LEFT JOIN membresias m ON s.id = m.socio_id
    WHERE s.huella = ?
    ORDER BY m.fecha_vencimiento DESC LIMIT 1
    """
    c.execute(query, (huella,))
    dato = c.fetchone()
    db.close()
    return dato

# --- ESTA ES LA PARTE QUE DEBES AGREGAR ---
if __name__ == "__main__":
    # Al ejecutar este archivo directamente, se crearán las tablas
    crear_tablas()