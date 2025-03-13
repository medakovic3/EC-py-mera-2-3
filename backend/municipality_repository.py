from backend.db_connection import get_db

class MunicipalityRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["Municipality"]

    def get_hdd_by_municipality(self, municipality_name: str) -> float:
        municipality_document = self.collection.find_one({"name": municipality_name})
        return municipality_document["hdd"]