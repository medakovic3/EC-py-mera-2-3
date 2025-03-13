class NeededEnergyRepository:
    def get_needed(
        self,
        construciton_period: str,
        insulated_surface_type: str
    ) -> float:
        needed_energy_document = collection.find_one({"construction_period": construciton_period})
        return needed_energy_document[insulated_surface_type]