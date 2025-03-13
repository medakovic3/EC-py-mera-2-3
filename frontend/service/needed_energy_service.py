from backend.controller.needed_energy_controller import NeededEnergyController

class NeededEnergyService:
    def __init__(self):
        self.controller = NeededEnergyController()

    def get_needed(
        self,
        construction_period: str,
        insulated_surface_type: str
    ) -> float:
        return self.controller.get_needed(
            construction_period,
            insulated_surface_type
        )
