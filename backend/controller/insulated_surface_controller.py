from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters


class InsulatedSurfaceController:
    def get_insulated_surface_parameters(
        self,
        insulated_surface_type: str,
        construction_period: str
    ) -> InsulatedSurfaceParameters:
        return self.repository.get_insulated_surface_parameters(
            insulated_surface_type,
            construction_period
        )