import customtkinter as ctk
from error_reporter import enviar_error
from lector import capturar_huella, identificar_huella
from database import registrar_socio, buscar_por_huella, registrar_asistencia
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Vikingo Gym")
        self.geometry("900x520")
        self.resizable(False, False)

        # ---------------- TOP BAR ----------------
        topbar = ctk.CTkFrame(self, height=60)
        topbar.pack(fill="x", side="top")

        titulo = ctk.CTkLabel(topbar, text="Vikingo Gym Control", font=("Arial", 22, "bold"))
        titulo.pack(pady=15)

        # ---------------- MAIN CONTAINER ----------------
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        # ---------------- SIDE MENU ----------------
        menu = ctk.CTkFrame(container, width=200)
        menu.pack(fill="y", side="left")

        # ---------------- WORK AREA ----------------
        self.workspace = ctk.CTkFrame(container)
        self.workspace.pack(fill="both", expand=True, side="right")

        # ---------------- SCREENS ----------------
        self.pantallas = {}

        # Inicio
        self.crear_inicio()

        # Socios
        self.crear_socios()

        # Accesos
        self.crear_accesos()

        # Menu botones
        ctk.CTkButton(menu, text="Inicio", command=lambda: self.mostrar("inicio")).pack(pady=10, padx=10)
        ctk.CTkButton(menu, text="Socios", command=lambda: self.mostrar("socios")).pack(pady=10, padx=10)
        ctk.CTkButton(menu, text="Accesos", command=lambda: self.mostrar("accesos")).pack(pady=10, padx=10)

        self.mostrar("inicio")

    # ---------------- CAMBIAR PANTALLA ----------------
    def mostrar(self, nombre):
        for p in self.pantallas.values():
            p.pack_forget()
        self.pantallas[nombre].pack(fill="both", expand=True)

    # ---------------- INICIO ----------------
    def crear_inicio(self):
        inicio = ctk.CTkFrame(self.workspace)
        lbl = ctk.CTkLabel(inicio, text="Bienvenido al sistema", font=("Arial", 24))
        lbl.pack(expand=True)
        self.pantallas["inicio"] = inicio

    # ---------------- SOCIOS ----------------
    def crear_socios(self):
        socios = ctk.CTkFrame(self.workspace)

        titulo = ctk.CTkLabel(socios, text="Registro de Socio", font=("Arial", 22))
        titulo.pack(pady=20)

        self.nombre = ctk.CTkEntry(socios, placeholder_text="Nombre completo", width=300)
        self.nombre.pack(pady=5)

        self.telefono = ctk.CTkEntry(socios, placeholder_text="Teléfono", width=300)
        self.telefono.pack(pady=5)

        self.vencimiento = ctk.CTkEntry(socios, placeholder_text="Fecha vencimiento (YYYY-MM-DD)", width=300)
        self.vencimiento.pack(pady=5)

        self.estado = ctk.CTkLabel(socios, text="")
        self.estado.pack(pady=10)

        btn_guardar = ctk.CTkButton(socios, text="Registrar socio", command=self.registrar_click)
        btn_guardar.pack(pady=20)

        self.pantallas["socios"] = socios

    def registrar_click(self):
        nombre = self.nombre.get()
        telefono = self.telefono.get()
        venc = self.vencimiento.get()

        if not nombre or not venc:
            self.estado.configure(text="Faltan datos", text_color="red")
            return

        self.estado.configure(text="Coloque la huella...")
        self.update()

        huella = capturar_huella()

        registrar_socio(nombre, telefono, venc, huella)

        self.estado.configure(text=f"Socio registrado | ID {huella[:8]}", text_color="green")

        self.nombre.delete(0, "end")
        self.telefono.delete(0, "end")
        self.vencimiento.delete(0, "end")

    # ---------------- ACCESOS ----------------
    def crear_accesos(self):
        accesos = ctk.CTkFrame(self.workspace)

        titulo = ctk.CTkLabel(accesos, text="Control de Acceso", font=("Arial", 22))
        titulo.pack(pady=20)

        self.mensaje = ctk.CTkLabel(accesos, text="Coloque su dedo en el lector", font=("Arial", 18))
        self.mensaje.pack(pady=20)

        btn_scan = ctk.CTkButton(accesos, text="Escanear huella", command=self.scan_click, height=50, width=200)
        btn_scan.pack(pady=40)

        self.pantallas["accesos"] = accesos

    def scan_click(self):
        self.mensaje.configure(text="Escaneando...")
        self.update()

        huella = identificar_huella()
        socio = buscar_por_huella(huella)

        if not socio:
            self.mensaje.configure(text="No registrado", text_color="red")
            return

        venc = datetime.strptime(socio[2], "%Y-%m-%d")

        if venc < datetime.now():
            self.mensaje.configure(text=f"{socio[1]} | Membresía vencida", text_color="orange")
            return

        registrar_asistencia(socio[0], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.mensaje.configure(text=f"Bienvenido {socio[1]}", text_color="green")

    def report_callback_exception(self, exc, val, tb):
        enviar_error(val, tb)
        print("Error en interfaz:", val)