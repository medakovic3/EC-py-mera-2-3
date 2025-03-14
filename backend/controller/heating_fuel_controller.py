from backend.repository.heating_fuel_repository import HeatingFuelRepository
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters


class HeatingFuelController:
    def __init__(self):
        self.repository = HeatingFuelRepository()

    def get_heating_fuel_parameters(
        self,
        heating_fuel_type: str,
        heating_system_type: str
    ) -> HeatingFuelParameters:
        return self.repository.get_heating_fuel_parameters(
            heating_fuel_type,
            heating_system_type
        )