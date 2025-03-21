from frontend.io_dataclass import *
from frontend.service.heating_fuel_service import HeatingFuelService
from frontend.service.municipality_service import MunicipalityService
from frontend.service.needed_energy_service import NeededEnergyService
from frontend.service.insulated_surface_service import InsulatedSurfaceService

class Component:
    def __init__(self):
        self.output_data: OutputData = OutputData()
        self.user_home_info: UserHomeInfo = None
        self.insulation_info: InsulationInfo = None
        self.db_data: DBData = DBData()

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

    def start_calculation(self):
        investment_cost = self.insulation_info.investment_cost

        payback_period = investment_cost / self.annual_cost_savings()

        self.output_data.payback_period = payback_period
        
    def annual_cost_savings(self):
        fin_en_savings = self.annual_final_energy_savings()
        fuel_cons_kWh = self.db_data.heating_fuel.consumption_per_kWh
        fuel_unit_cost = self.user_home_info.fuel_cost_per_unit

        cost_savings = fin_en_savings * fuel_cons_kWh * fuel_unit_cost

        self.output_data.annual_cost_savings = cost_savings
        return cost_savings
    
    def annual_final_energy_savings(self):
        nd_en_savings = self.needed_energy_savings()
        total_eff = self.total_efficiency()
        real_cons_coef = self.real_consumption_coef()

        fin_en_savings = (nd_en_savings / total_eff) * real_cons_coef

        self.output_data.annual_final_energy_savings = fin_en_savings
        return fin_en_savings

    def total_efficiency(self):
        fuel_eff = self.db_data.heating_fuel.efficiency.heating_fuel
        pipe_sys_eff = self.db_data.heating_fuel.efficiency.pipe_system
        pipe_reg_eff = self.db_data.heating_fuel.efficiency.pipe_regulation

        total_eff = fuel_eff * pipe_sys_eff * pipe_reg_eff

        return  total_eff

    def needed_energy_savings(self):
        heating_break_coef = 0.85
        fxi = self.db_data.insulated_surface.fxi
        area = self.insulation_info.insulated_area
        U_old = self.db_data.insulated_surface.U
        U_new = self.U_new()
        hdd = self.db_data.hdd
        hours = 24
        W_in_kW = 1000

        U_diff = U_old - U_new
        nd_en_savings_W = heating_break_coef * fxi * area * U_diff * hdd * hours
        nd_en_savings = nd_en_savings_W / W_in_kW

        return nd_en_savings
    
    def U_new(self):
        R_new = self.R_new()

        U_new = 1 / R_new

        return U_new
    
    def R_new(self):
        R_old =self.R_old()
        ins_thickness = self.insulation_info.insulation_thickness
        ins_thermal_cond = self.insulation_info.insulation_thermal_conductivity

        R_new = R_old + (ins_thickness / ins_thermal_cond)

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
        final_energy = self.final_energy()
        fuel_cons_per_kWh = self.db_data.heating_fuel.consumption_per_kWh

        calc_fuel_cons = final_energy / fuel_cons_per_kWh

        return calc_fuel_cons
    
    def final_energy(self):
        needed_energy = self.needed_energy()
        total_eff = self.total_efficiency()

        final_energy = needed_energy / total_eff

        return final_energy
    
    def needed_energy(self):
        needed_en_m2 = self.db_data.needed_energy_per_m2
        hdd = self.db_data.hdd
        hdd_average = 2665.56
        floor_area = self.user_home_info.floor_area

        needed_energy = needed_en_m2 * (hdd / hdd_average) * floor_area

        return needed_energy
