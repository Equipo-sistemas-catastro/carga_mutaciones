class ArchivoDuplicadoException(Exception):
    def __init__(self, mensaje: str):
        self.mensaje = mensaje

class CargaFallidaException(Exception):
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
