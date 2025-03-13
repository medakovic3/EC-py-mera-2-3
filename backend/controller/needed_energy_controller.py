from backend.repository.needed_energy_repository import NeededEnergyRepository

class NeededEnergyController:
    def __init__(self):
        self.needed_energy_repository = NeededEnergyRepository()

    def get_needed(
        self,
        construction_period: str,
        dwelling_type: str
    ) -> float:
        return self.needed_energy_repository.get_needed(
            construction_period,
            dwelling_type
        )