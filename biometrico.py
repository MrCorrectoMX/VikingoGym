class LectorBiometrico:
    def capturar(self):
        raise NotImplementedError

    def identificar(self, huella):
        raise NotImplementedError