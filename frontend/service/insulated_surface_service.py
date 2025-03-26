from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters
from backend.controller.insulated_surface_controller import InsulatedSurfaceController

class InsulatedSurfaceService:
    def __init__(self):
        self.controller = InsulatedSurfaceController()

    def get_insulated_surface_parameters(
        self,
        insulated_surface_type: str,
        construciton_period: str
    ) -> InsulatedSurfaceParameters:
        return self.controller.get_insulated_surface_parameters(
                                insulated_surface_type,
                                construciton_period
                               )