import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Vikingo Gym")
app.geometry("900x520")
app.resizable(False, False)


# TOP BAR 
topbar = ctk.CTkFrame(app, height=60)
topbar.pack(fill="x", side="top")

titulo = ctk.CTkLabel(topbar, text="Vikingo Gym Control", font=("Arial", 22, "bold"))
titulo.pack(pady=15)


# MAIN CONTAINER 
container = ctk.CTkFrame(app)
container.pack(fill="both", expand=True)


# SIDE MENU 
menu = ctk.CTkFrame(container, width=200)
menu.pack(fill="y", side="left")


# WORK AREA 
workspace = ctk.CTkFrame(container)
workspace.pack(fill="both", expand=True, side="right")


# SCREENS 
pantallas = {}

def mostrar(nombre):
    for p in pantallas.values():
        p.pack_forget()
    pantallas[nombre].pack(fill="both", expand=True)


# Pantalla inicio
inicio = ctk.CTkFrame(workspace)
lbl = ctk.CTkLabel(inicio, text="Bienvenido al sistema", font=("Arial", 24))
lbl.pack(expand=True)

pantallas["inicio"] = inicio


# Pantalla socios
from database import crear_tablas, registrar_socio
from biometrico_simulado import LectorSimulado

crear_tablas()
lector = LectorSimulado()

socios = ctk.CTkFrame(workspace)

titulo_socios = ctk.CTkLabel(socios, text="Registro de Socio", font=("Arial", 22))
titulo_socios.pack(pady=20)

nombre = ctk.CTkEntry(socios, placeholder_text="Nombre completo", width=300)
nombre.pack(pady=5)

telefono = ctk.CTkEntry(socios, placeholder_text="Teléfono", width=300)
telefono.pack(pady=5)

vencimiento = ctk.CTkEntry(socios, placeholder_text="Fecha vencimiento (YYYY-MM-DD)", width=300)
vencimiento.pack(pady=5)

estado = ctk.CTkLabel(socios, text="")
estado.pack(pady=10)


def registrar():
    n = nombre.get()
    t = telefono.get()
    v = vencimiento.get()

    if not n or not v:
        estado.configure(text="Faltan datos", text_color="red")
        return

    estado.configure(text="Escanee la huella...")
    huella = lector.registrar()

    registrar_socio(n, t, v, huella)

    estado.configure(text=f"Socio registrado | ID Huella: {huella}", text_color="green")

    nombre.delete(0, "end")
    telefono.delete(0, "end")
    vencimiento.delete(0, "end")


btn_guardar = ctk.CTkButton(socios, text="Registrar socio", command=registrar)
btn_guardar.pack(pady=20)

from database import obtener_socios, actualizar_vencimiento

lista_frame = ctk.CTkFrame(socios)
lista_frame.pack(pady=20, fill="both", expand=True)

lista = ctk.CTkTextbox(lista_frame, height=150)
lista.pack(fill="both", expand=True, padx=10, pady=10)

seleccion = ctk.CTkEntry(socios, placeholder_text="ID del socio a renovar")
seleccion.pack(pady=5)

nueva_fecha = ctk.CTkEntry(socios, placeholder_text="Nueva fecha (YYYY-MM-DD)")
nueva_fecha.pack(pady=5)


def cargar_socios():
    lista.delete("1.0", "end")
    for s in obtener_socios():
        lista.insert("end", f"ID:{s[0]} | {s[1]} | {s[2]} | vence:{s[3]}\n")


def renovar():
    try:
        actualizar_vencimiento(seleccion.get(), nueva_fecha.get())
        estado.configure(text="Membresía actualizada", text_color="green")
        cargar_socios()
    except:
        estado.configure(text="Error al actualizar", text_color="red")


btn_lista = ctk.CTkButton(socios, text="Mostrar socios", command=cargar_socios)
btn_lista.pack(pady=5)

btn_renovar = ctk.CTkButton(socios, text="Renovar membresía", command=renovar)
btn_renovar.pack(pady=10)



pantallas["socios"] = socios


# Pantalla accesos
from database import buscar_por_huella, registrar_asistencia
from datetime import datetime

accesos = ctk.CTkFrame(workspace)

titulo_acc = ctk.CTkLabel(accesos, text="Control de Acceso", font=("Arial", 22))
titulo_acc.pack(pady=20)

mensaje = ctk.CTkLabel(accesos, text="Coloque su dedo en el lector", font=("Arial", 18))
mensaje.pack(pady=20)


def escanear():
    mensaje.configure(text="Escaneando huella...")

    huella = lector.identificar()

    socio = buscar_por_huella(huella)

    if not socio:
        mensaje.configure(text="Socio no registrado", text_color="red")
        return

    venc = datetime.strptime(socio[2], "%Y-%m-%d")

    if venc < datetime.now():
        mensaje.configure(text=f"{socio[1]} - Membresía vencida", text_color="orange")
        return

    registrar_asistencia(socio[0])
    mensaje.configure(text=f"Bienvenido {socio[1]}", text_color="green")


btn_scan = ctk.CTkButton(accesos, text="Escanear huella", command=escanear, height=50, width=200)
btn_scan.pack(pady=40)


pantallas["accesos"] = accesos


# MENU BUTTONS 
ctk.CTkButton(menu, text="Inicio", command=lambda: mostrar("inicio")).pack(pady=10, padx=10)
ctk.CTkButton(menu, text="Socios", command=lambda: mostrar("socios")).pack(pady=10, padx=10)
ctk.CTkButton(menu, text="Accesos", command=lambda: mostrar("accesos")).pack(pady=10, padx=10)


mostrar("inicio")

app.mainloop()
