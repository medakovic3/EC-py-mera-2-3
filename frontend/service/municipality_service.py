from backend.controller.municipality_controller import MunicipalityController

class MunicipalityService:
    def __init__(self):
        self.controller = MunicipalityController()

    def get_hdd_by_municipality(self, municipality_name: str) -> float:
        return self.controller.get_hdd_by_municipality(municipality_name)