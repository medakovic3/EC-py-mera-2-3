from backend.db_connection import get_db
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters
from frontend.model.heating_fuel_parameters_model import Efficiency

class HeatingFuelRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["HeatingFuel"]

    def get_heating_fuel_parameters(
        self,
        heating_fuel_type: str,
        heating_system_type: str
    ) -> HeatingFuelParameters:
        heating_fuel_document = self.collection.find_one({"type": heating_fuel_type})
        efficiency_document = heating_fuel_document[heating_system_type]

        efficiency = Efficiency(
            efficiency_document["efficiency_fuel"],
            efficiency_document["efficiency_pipe_system"],
            efficiency_document["efficiency_pipe_regulation"] 
        )
        consumption_per_kWh = heating_fuel_document["consumption_per_kWh"]
        
        return HeatingFuelParameters(efficiency, consumption_per_kWh)
