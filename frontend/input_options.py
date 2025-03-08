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

class HeatingFuelType(Enum):
    WOOD = "Wood"
    COAL = "Coal"
    LIQUID_FUEL = "Liquid Fuel"
    ELECTRICITY = "Electricity"
    GAS = "Gas"
    PELLET = "Pellet"
    HEAT_PUMP = "Heat Pump"
    DISTRICT_HEATING = "District Heating"