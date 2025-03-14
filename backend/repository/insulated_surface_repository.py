from frontend.model.insulated_surface_parameters_model import InsulatedSurfaceParameters

class InsulatedSurfaceRepository:
    def get_insulated_surface_parameters(
        self,
        insulated_surface_type: str,
        construction_period: str
    ) -> InsulatedSurfaceParameters:
        insulated_surface_document = self.collection.find_one({"type": insulated_surface_type})
        U = insulated_surface_document["U"][construction_period]
        fxi = insulated_surface_document["fxi"]
        return {U, fxi}