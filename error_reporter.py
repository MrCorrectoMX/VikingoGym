import requests
import traceback
import platform
import datetime
import os

WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1475179699230474515/BUXUUe8fFErtH_WBW3_-P5TNEX8DoDQ0POA2B2ibo14dvBkXUbboxIREnXfWnvbfBj81")  

def enviar_error(error):
    try:
        stacktrace = traceback.format_exc()

        mensaje = {
            "content": f"""
 **ERROR EN GYM APP** 

 Fecha: {datetime.datetime.now()}
Sistema: {platform.system()} {platform.release()}

Tipo: {type(error).__name__}
Mensaje: {str(error)}

```{stacktrace}```
"""
        }

        requests.post(WEBHOOK_URL, json=mensaje)

    except Exception as e:
        print("Error enviando el reporte:", e)