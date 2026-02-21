import random
from biometrico import LectorBiometrico

class LectorSimulado(LectorBiometrico):

    def registrar(self):
        print("Simulando registro de huella...")
        return "H" + str(random.randint(1000,9999))

    def identificar(self):
        print("Simulando lectura de huella...")
        return input("Escribe el ID de huella: ")
