from backend.db_connection import get_db
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters

class HeatingFuelRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["HeatingFuel"]

    def get_heating_fuel_parameters(
        self,
        heating_fuel_type: str,
        heating_system_type: str
    ) -> HeatingFuelParameters:
        pass