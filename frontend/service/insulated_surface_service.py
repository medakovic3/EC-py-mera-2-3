from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters

class InsulatedSurfaceService:
    def get_insulated_surface_parameters(
        self,
        insulated_surface_type: str,
        construciton_period: str
    ) -> InsulatedSurfaceParameters:
        return self.controller.get_insulated_surface_parameters(
            insulated_surface_type,
            construciton_period
        )