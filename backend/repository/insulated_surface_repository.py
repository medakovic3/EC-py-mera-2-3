from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters
from backend.db_connection import get_db

class InsulatedSurfaceRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["InsulatedSurface"]

    def get_insulated_surface_parameters(
        self,
        insulated_surface_type: str,
        construction_period: str
    ) -> InsulatedSurfaceParameters:
        insulated_surface_document = self.collection.find_one({"type": insulated_surface_type})
        U = insulated_surface_document["U"][construction_period]
        fxi = insulated_surface_document["fxi"]
        return {U, fxi}