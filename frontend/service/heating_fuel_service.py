from backend.controller.heating_fuel_controller import HeatingFuelController
from frontend.model.heating_fuel_parameters_model import HeatingFuelParameters

class HeatingFuelService:
    def __init__(self):
        self.controller = HeatingFuelController()

    def get_heating_fuel_parameters(
        self,
        heating_fuel_type: str,
        heating_system_type: str
    ) -> HeatingFuelParameters:
        return self.controller.get_heating_fuel_parameters(
            heating_fuel_type,
            heating_system_type
        )