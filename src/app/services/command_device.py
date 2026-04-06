from app.repository.interfaces import InstalledDeviceRepositoryProtocol


class CommandDevice:
    def __init__(self, repository: InstalledDeviceRepositoryProtocol):
        self.repository = repository
