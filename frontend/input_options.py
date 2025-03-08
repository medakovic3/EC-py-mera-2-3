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

class InsulatedConstructionType(Enum):
    EXTERNAL_WALL = "External Wall"
    GROUND_FLOOR = "Ground Floor"
    FLOOR_ABOVE_UNHEATED = "Floor Above Unheated Space"
    CEILING_BELOW_UNHEATED = "Ceiling Below Unheated Space"
    ROOF_ABOVE_HEATED = "Roof Above Heated Space"
    
class ConstructionPeriod(Enum):
    BEFORE_1945 = "Before 1945"
    PERIOD_1946_1960 = "1946-1960"
    PERIOD_1961_1970 = "1961-1970"
    PERIOD_1971_1980 = "1971-1980"
    PERIOD_1981_1990 = "1981-1990"
    PERIOD_1991_2012 = "1991-2012"
    AFTER_2012 = "After 2012"