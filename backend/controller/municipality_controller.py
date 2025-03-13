from backend.repository.municipality_repository import MunicipalityRepository

class MunicipalityController:
    def __init__(self):
        self.repository = MunicipalityRepository()

    def get_hdd_by_municipality(self, municipality_name: str) -> float:
        return self.repository.get_hdd_by_municipality(municipality_name)