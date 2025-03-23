from backend.db_connection import get_db

class JoineryRepository:
    def __init__(self):
        self.db = get_db()
        self.air_changes_collection = self.db["AirChangesPerHour"]
        self.window_U_collection = self.db["WindowU"]
        self.door_U_collection = self.db["DoorU"]

    def get_air_changes_per_hour(self, wind_exp: str, airtghtnss: str) -> float:
        collection = self.air_changes_collection

        air_chngs_doc = collection.find_one({"wind_exposure": wind_exp})

        air_changes_per_hour = air_chngs_doc[airtghtnss]

        return air_changes_per_hour
    
    def get_window_U_old(self, window_material: str, glazing: str) -> float:
        collection = self.window_U_collection

        window_U_doc = collection.find_one({"material": window_material})

        window_U_old = window_U_doc[glazing]

        return window_U_old
    
    def get_door_U_old(self, door_material: str) -> float:
        collection = self.door_U_collection

        door_U_doc = collection.find_one({"material": door_material})

        door_U_old = door_U_doc["U"]

        return door_U_old