from database import crear_tablas, conectar
from biometrico_simulado import LectorSimulado
from datetime import datetime

crear_tablas()
lector = LectorSimulado()

def registrar_socio():
    nombre = input("Nombre: ")
    tel = input("Telefono: ")

    huella = lector.registrar()
    venc = input("Fecha vencimiento YYYY-MM-DD: ")

    db = conectar()
    c = db.cursor()

    c.execute("INSERT INTO socios(nombre,telefono,vencimiento,huella_id) VALUES(?,?,?,?)",
              (nombre,tel,venc,huella))

    db.commit()
    db.close()
    print("Socio registrado con huella:", huella)

def entrada():
    huella = lector.identificar()

    db = conectar()
    c = db.cursor()

    c.execute("SELECT id,nombre,vencimiento FROM socios WHERE huella_id=?", (huella,))
    socio = c.fetchone()

    if not socio:
        print("NO REGISTRADO")
        return

    venc = datetime.strptime(socio[2], "%Y-%m-%d")
    if venc < datetime.now():
        print("MEMBRESIA VENCIDA")
        return

    print("BIENVENIDO", socio[1])

    c.execute("INSERT INTO asistencias(socio_id,fecha) VALUES(?,?)",
              (socio[0], datetime.now()))

    db.commit()
    db.close()

while True:
    op = input("\n1 Registrar\n2 Entrada\n>")
    if op=="1": registrar_socio()
    if op=="2": entrada()



.gitignore
# Python
__pycache__/
*.pyc
*.pyo

# Base de datos local
*.db

# Visual Studio Code
.vscode/

# Windows basura
Thumbs.db
desktop.ini