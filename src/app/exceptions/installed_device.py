class InstalledDeviceNotFound(Exception):
    def __init__(self):
        super().__init__("Dispositivo instalado no encontrado")
