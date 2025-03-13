from backend.db_connection import get_db

class MunicipalityRepository:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["Municipality"]