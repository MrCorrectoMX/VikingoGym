from database import crear_tablas
from ui import App

# preparar base de datos
crear_tablas()

# iniciar interfaz
app = App()
app.mainloop()  