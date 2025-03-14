from backend.repository.heating_fuel_repository import HeatingFuelRepository


class HeatingFuelController:
    def __init__(self):
        self.repository = HeatingFuelRepository()