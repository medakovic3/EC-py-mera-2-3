from enum import Enum

class DwellingType(Enum):
	APARTMENT = "Apartment"
	DETACHED_HOUSE = "Detached House"
	SEMI_DETACHED_HOUSE = "Semi-Detached or Row House"

class BuildingType(Enum):
    DETACHED = "Detached"
    BLOCK = "Block"
    HIGH_RISE = "High-Rise"

class HeatingSystemType(Enum):
    CENTRAL = "Central Heating"
    INDIVIDUAL = "Individual Heating"
    LOCAL = "Local Heating"
