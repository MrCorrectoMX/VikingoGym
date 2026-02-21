from biometrico import LectorBiometrico
import random

class LectorSimulado(LectorBiometrico):

    def capturar(self):
        return str(random.randint(1000, 9999))

    def identificar(self, huella):
        return huella