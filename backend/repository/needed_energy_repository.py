from backend.db_connection import get_db

class NeededEnergyRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["NeededEnergyPerM2"]

    def get_needed(
        self,
        construciton_period: str,
        insulated_surface_type: str
    ) -> float:
        needed_energy_document = self.collection.find_one({"construction_period": construciton_period})
        return needed_energy_document[insulated_surface_type]