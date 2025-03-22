from frontend.io_dataclass import *
from frontend.service.heating_fuel_service import HeatingFuelService
from frontend.service.municipality_service import MunicipalityService
from frontend.service.needed_energy_service import NeededEnergyService

HEATING_BREAK_COEFFICIENT = 0.85
HOURS_IN_DAY = 24
WATTS_IN_KILOWATTS = 1000
CENTIMETERS_IN_METER = 100

class BoilerComponent:
    def __init__(self):
        self.output_data: OutputData = OutputData()
        self.user_home_info: UserHomeInfo = None
        self.boiler_info: BoilerInfo = None
        self.db_data: BoilerDBData = BoilerDBData()

        self.municipality_service = MunicipalityService()
        self.needed_energy_service = NeededEnergyService()
        self.heating_fuel_service = HeatingFuelService()

    def calculate_output_data(
        self,
        user_home_info: UserHomeInfo,
        boiler_info: BoilerInfo
    ) -> OutputData:
        self.set_input_info(user_home_info, boiler_info)
        self.load_db_data()
        self.start_calculation()
        return self.output_data
    
    def set_input_info(
            self,
            user_home_info: UserHomeInfo,
            boiler_info: BoilerInfo
    ):
        self.user_home_info = user_home_info
        self.boiler_info = boiler_info

    def load_db_data(self):
        self.load_hdd()
        self.load_needed_energy()
        self.load_heating_fuel_parameters()
        self.load_new_heating_fuel_parameteres()

    def load_hdd(self):
        service = self.municipality_service

        municipality = self.user_home_info.municipality.value

        hdd = service.get_hdd_by_municipality(municipality)

        self.db_data.hdd = hdd

    def load_needed_energy(self):
        service = self.needed_energy_service

        construction_period = self.user_home_info.construction_period.value
        dwelling_type = self.user_home_info.dwelling_type
        dwelling_type_str = dwelling_type.value

        if dwelling_type == DwellingType.APARTMENT:
            building_type_str = self.user_home_info.building_type.value
            dwelling_type_str += " " + building_type_str

        needed = service.get_needed(construction_period, dwelling_type_str)
        
        self.db_data.needed_energy_per_m2 = needed

    def load_heating_fuel_parameters(self):
        service = self.heating_fuel_service

        heating_fuel_type = self.user_home_info.heating_fuel_type.value
        heating_system_type = self.user_home_info.heating_system_type.value

        heating_fuel = service.get_heating_fuel_parameters(
                                    heating_fuel_type, heating_system_type
                               )

        self.db_data.heating_fuel = heating_fuel

    def load_new_heating_fuel_parameteres(self):
        service = self.heating_fuel_service

        heating_fuel_type = self.boiler_info.new_heating_fuel_type.value
        heating_system_type = self.user_home_info.heating_system_type.value

        heating_fuel = service.get_heating_fuel_parameters(
                                    heating_fuel_type, heating_system_type
                               )

        self.db_data.new_heating_fuel = heating_fuel

    def start_calculation(self):
        investment_cost = self.boiler_info.investment_cost
        annual_cost_savings = self.annual_cost_savings()

        payback_period = investment_cost / annual_cost_savings

        self.output_data.payback_period = payback_period

        co2_em_old = self.co2_emission_old()
        co2_em_new = self.co2_emission_new()

        co2_em_red = co2_em_old - co2_em_new

        self.output_data.co2_emission_reduction = co2_em_red
        self.output_data.annual_final_energy_savings = \
            self.final_energy_old() * self.real_consumption_coef() - self.final_energy_new()

        
    def annual_cost_savings(self):
        fin_en_old = self.final_energy_old()
        real_cons_coef = self.real_consumption_coef()
        fuel_cons_kWh_old = self.db_data.heating_fuel.consumption_per_kWh
        fuel_cost_unit_old = self.user_home_info.fuel_cost_per_unit
        annual_cost_new = self.annual_cost_new()

        annual_cost_old = fin_en_old * real_cons_coef * fuel_cons_kWh_old * fuel_cost_unit_old

        cost_savings = annual_cost_old - annual_cost_new

        self.output_data.annual_cost_savings = cost_savings

        return cost_savings
    
    def annual_cost_new(self):
        fin_en_new = self.final_energy_new()
        fuel_cons_new = self.db_data.new_heating_fuel.consumption_per_kWh
        fuel_cost_new = self.boiler_info.new_fuel_cost_per_unit

        cost_new = fin_en_new * fuel_cons_new * fuel_cost_new

        return cost_new

    def total_efficiency(self):
        fuel_eff = self.db_data.heating_fuel.efficiency.heating_fuel
        pipe_sys_eff = self.db_data.heating_fuel.efficiency.pipe_system
        pipe_reg_eff = self.db_data.heating_fuel.efficiency.pipe_regulation

        total_eff = fuel_eff * pipe_sys_eff * pipe_reg_eff

        return  total_eff
    
    def real_consumption_coef(self):
        real_fuel_cons = self.real_fuel_consumption()
        calc_fuel_cons = self.calculated_fuel_consumption()

        real_cons_coef = real_fuel_cons / calc_fuel_cons

        return real_cons_coef
    
    def real_fuel_consumption(self):
        user_fuel_cons = self.user_home_info.annual_fuel_consumption
        calc_fuel_cons = self.calculated_fuel_consumption()

        real_fuel_cons = user_fuel_cons if user_fuel_cons else calc_fuel_cons

        return  real_fuel_cons
    
    def calculated_fuel_consumption(self):
        final_energy = self.final_energy_old()
        fuel_cons_per_kWh = self.db_data.heating_fuel.consumption_per_kWh

        calc_fuel_cons = final_energy / fuel_cons_per_kWh

        return calc_fuel_cons
    
    def final_energy_old(self):
        needed_energy_old = self.needed_energy_old()
        total_eff = self.total_efficiency()

        final_energy_old = needed_energy_old / total_eff

        return final_energy_old
    
    def needed_energy_old(self):
        needed_en_m2 = self.db_data.needed_energy_per_m2
        hdd = self.db_data.hdd
        hdd_average = 2665.56
        floor_area = self.user_home_info.floor_area

        needed_energy_old = needed_en_m2 * (hdd / hdd_average) * floor_area

        return needed_energy_old
    
    def co2_emission_old(self):
        prim_en_old = self.primary_energy_old()
        fuel_co2_em = self.db_data.heating_fuel.co2_emission
        real_cons_coef = self.real_consumption_coef()

        co2_em_old = prim_en_old * fuel_co2_em * real_cons_coef

        return co2_em_old
    
    def primary_energy_old(self):
        final_en_old = self.final_energy_old()
        prim_en_conv_factor = self.db_data.heating_fuel.prim_en_conv_factor

        prim_en_old = final_en_old * prim_en_conv_factor

        return prim_en_old

    def co2_emission_new(self):
        prim_en_new = self.primary_energy_new()
        fuel_co2_em = self.db_data.heating_fuel.co2_emission
        real_cons_coef = self.real_consumption_coef()

        co2_em_new = prim_en_new * fuel_co2_em * real_cons_coef

        return co2_em_new
    
    def primary_energy_new(self):
        final_en_new = self.final_energy_new()
        prim_en_conv_factor = self.db_data.new_heating_fuel.prim_en_conv_factor

        prim_en_new = final_en_new * prim_en_conv_factor

        return prim_en_new
    
    def final_energy_new(self):
        efficiency_new = self.total_efficiency_new()
        needed_en_old = self.needed_energy_old()
        real_cons_coef = self.real_consumption_coef()
        delta1 = 0
        delta2 = 0

        fin_en_new = (needed_en_old * real_cons_coef - (delta1 + delta2)) / efficiency_new
    
        return fin_en_new

    def total_efficiency_new(self):
        fuel_eff = self.boiler_info.new_fuel_efficiency
        pipe_system_eff = 0.98 if self.boiler_info.pipe_system_change else self.db_data.heating_fuel.efficiency.pipe_system
        pipe_reg_eff = 0.95 if self.boiler_info.thermostat_installation else self.db_data.heating_fuel.efficiency.pipe_regulation

        total_eff_new = fuel_eff * pipe_system_eff * pipe_reg_eff

        return total_eff_new