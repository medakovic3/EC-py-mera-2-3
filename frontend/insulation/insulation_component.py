from frontend.insulation.insulation_dataclasses import *
from frontend.io_dataclass import *
from frontend.service.heating_fuel_service import HeatingFuelService
from frontend.service.municipality_service import MunicipalityService
from frontend.service.needed_energy_service import NeededEnergyService
from frontend.service.insulated_surface_service import InsulatedSurfaceService

HEATING_BREAK_COEFFICIENT = 0.85
HOURS_IN_DAY = 24
WATTS_IN_KILOWATTS = 1000
CENTIMETERS_IN_METER = 100
ISOLATED_PIPE_SYSTEM_EFFICIENCY = 0.98
HDD_AVERAGE = 2665.56

class InsulationComponent:
    def __init__(self):
        self.output_data: OutputData = OutputData()
        self.user_home_info: UserHomeInfo = None
        self.insulation_info: InsulationInfo = None
        self.db_data: InsulationDBData = InsulationDBData()

        self.municipality_service = MunicipalityService()
        self.needed_energy_service = NeededEnergyService()
        self.insulated_surface_service = InsulatedSurfaceService()
        self.heating_fuel_service = HeatingFuelService()

    def calculate_output_data(
        self,
        user_home_info: UserHomeInfo,
        insulation_info: InsulationInfo
    ) -> OutputData:
        self.set_input_info(user_home_info, insulation_info)
        self.load_db_data()
        self.start_calculation()
        return self.output_data
    
    def set_input_info(
        self,
        user_home_info: UserHomeInfo,
        insulation_info: InsulationInfo
    ):
        self.user_home_info = user_home_info
        self.insulation_info = insulation_info

    # ==========================================================================
    # Load data from database
    # ==========================================================================

    def load_db_data(self):
        self.load_hdd()
        self.load_needed_energy()
        self.load_insulated_surface_parameters()
        self.load_heating_fuel_parameters()

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

    def load_insulated_surface_parameters(self):
        service = self.insulated_surface_service

        ins_surf_type = self.insulation_info.insulated_surface_type.value
        construction_period = self.user_home_info.construction_period.value

        insulated_surface = service.get_insulated_surface_parameters(
                                ins_surf_type, construction_period
                           )

        self.db_data.insulated_surface = insulated_surface

    def load_heating_fuel_parameters(self):
        service = self.heating_fuel_service

        heating_fuel_type = self.user_home_info.heating_fuel_type.value
        heating_system_type = self.user_home_info.heating_system_type.value

        heating_fuel = service.get_heating_fuel_parameters(
                                    heating_fuel_type, heating_system_type
                               )

        self.db_data.heating_fuel = heating_fuel

    # ==========================================================================
    # Do the calculation
    # ==========================================================================

    def start_calculation(self):
        payback_period = self.payback_period()
        self.output_data.payback_period = payback_period

        co2_em_red = self.co2_emission_reduction()
        self.output_data.co2_emission_reduction = co2_em_red

    def payback_period(self):
        investment_cost = self.insulation_info.investment_cost
        annual_cost_savings = self.annual_cost_savings()

        payback_period = investment_cost / annual_cost_savings

        return payback_period
        
    def annual_cost_savings(self):
        fuel_unit_cost = self.user_home_info.fuel_cost_per_unit
        fuel_cons_kWh = self.db_data.heating_fuel.consumption_per_kWh
        fin_en_savings = self.annual_final_energy_savings()

        cost_savings = fin_en_savings * fuel_cons_kWh * fuel_unit_cost

        self.output_data.cost_savings = cost_savings
        return cost_savings
    
    def annual_final_energy_savings(self):
        total_eff = self.total_efficiency()
        nd_en_savings = self.needed_energy_savings()

        fin_en_savings = nd_en_savings / total_eff

        self.output_data.final_energy_savings = fin_en_savings
        return fin_en_savings

    def total_efficiency(self):
        iso = self.user_home_info.pipe_system_isolated

        fuel_eff = self.db_data.heating_fuel.efficiency.heating_fuel
        pipe_sys_eff = ISOLATED_PIPE_SYSTEM_EFFICIENCY if iso \
                        else self.db_data.heating_fuel.efficiency.pipe_system
        pipe_reg_eff = self.db_data.heating_fuel.efficiency.pipe_regulation

        total_eff = fuel_eff * pipe_sys_eff * pipe_reg_eff

        return  total_eff

    def needed_energy_savings(self):
        heating_break_coef = HEATING_BREAK_COEFFICIENT
        hours = HOURS_IN_DAY
        W_in_kW = WATTS_IN_KILOWATTS
        area = self.insulation_info.insulated_area
        fxi = self.db_data.insulated_surface.fxi
        U_old = self.db_data.insulated_surface.U
        hdd = self.db_data.hdd
        U_new = self.U_new()
        real_cons_coef = self.real_consumption_coef()

        U_diff = U_old - U_new
        nd_en_savings_W = heating_break_coef * fxi * area * U_diff * hdd * hours
        nd_en_savings = nd_en_savings_W / W_in_kW
        nd_en_savings_real = nd_en_savings * real_cons_coef

        return nd_en_savings_real
    
    def U_new(self):
        R_new = self.R_new()

        U_new = 1 / R_new

        return U_new
    
    def R_new(self):
        ins_thickness_cm = self.insulation_info.insulation_thickness
        ins_thermal_cond = self.insulation_info.insulation_thermal_conductivity
        R_old =self.R_old()

        ins_thickness_m = ins_thickness_cm / CENTIMETERS_IN_METER
        R_new = R_old + (ins_thickness_m / ins_thermal_cond)

        return R_new

    def R_old(self):
        U_old = self.db_data.insulated_surface.U

        R_old = 1 / U_old

        return R_old
    
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
        fuel_cons_per_kWh = self.db_data.heating_fuel.consumption_per_kWh
        final_energy = self.final_energy_old()

        calc_fuel_cons = final_energy / fuel_cons_per_kWh

        return calc_fuel_cons
    
    def final_energy_old(self):
        needed_energy_old = self.needed_energy_old()
        total_eff = self.total_efficiency()

        final_energy_old = needed_energy_old / total_eff

        return final_energy_old
    
    def needed_energy_old(self):
        hdd_average = HDD_AVERAGE
        floor_area = self.user_home_info.floor_area
        needed_en_m2 = self.db_data.needed_energy_per_m2
        hdd = self.db_data.hdd

        needed_energy_old = needed_en_m2 * (hdd / hdd_average) * floor_area

        return needed_energy_old

    def co2_emission_reduction(self):
        fuel_co2_em = self.db_data.heating_fuel.co2_emission
        prim_en_savings = self.primary_energy_savings()

        co2_em_red = prim_en_savings * fuel_co2_em

        return co2_em_red
    
    def primary_energy_savings(self):
        conv_factor = self.db_data.heating_fuel.final_to_primary_conversion_factor
        fin_en_savings = self.annual_final_energy_savings()

        prim_en_savings = fin_en_savings * conv_factor

        return prim_en_savings