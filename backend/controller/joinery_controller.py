from backend.repository.joinery_repository import JoineryRepository


class JoineryController:
    def __init__(self):
        self.repository = JoineryRepository()

    def get_air_changes_per_hour(self, wind_exp: str, airtghtnss: str) -> float:
        return self.repository.get_air_changes_per_hour(wind_exp, airtghtnss)
    
    def get_window_U_old(self, window_material: str, glazing: str) -> float:
        return self.repository.get_window_U_old(window_material, glazing)
    
    def get_door_U_old(self, door_material: str) -> float:
        return self.repository.get_door_U_old(door_material)