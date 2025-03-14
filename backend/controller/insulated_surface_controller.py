from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters
from backend.repository.insulated_surface_repository import InsulatedSurfaceRepository


class InsulatedSurfaceController:
    def __init__(self):
        self.repository = InsulatedSurfaceRepository()

    def get_insulated_surface_parameters(
        self,
        insulated_surface_type: str,
        construction_period: str
    ) -> InsulatedSurfaceParameters:
        return self.repository.get_insulated_surface_parameters(
            insulated_surface_type,
            construction_period
        )