class LectorBiometrico:

    def registrar(self):
        """Devuelve un ID de huella"""
        raise NotImplementedError

    def identificar(self):
        """Devuelve ID de huella detectada"""
        raise NotImplementedError
