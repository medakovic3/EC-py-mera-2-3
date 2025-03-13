class NeededEnergyController:
    def get_needed(
        self,
        construction_period: str,
        insulated_construction_type: str
    ) -> float:
        return self.needed_energy_repository.get_needed(
            construction_period,
            insulated_construction_type
        )