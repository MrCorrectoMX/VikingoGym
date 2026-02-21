from biometrico_simulado import LectorSimulado

lector = LectorSimulado()

def capturar_huella():
    return lector.capturar()

def identificar_huella():
    huella = capturar_huella()
    return lector.identificar(huella)