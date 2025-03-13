from backend.repository.municipality_repository import MunicipalityRepository

class MunicipalityController:
    def __init__(self):
        self.repository = MunicipalityRepository()