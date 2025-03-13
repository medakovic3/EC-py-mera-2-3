class NeededEnergyService:
    def get_needed(
        self,
        construction_period: str,
        insulated_construction_type: str
    ) -> float:
        return self.controller.get_needed(
            construction_period,
            insulated_construction_type
        )
