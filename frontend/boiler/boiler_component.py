from frontend.boiler.boiler_dataclasses import *
from frontend.io_dataclass import *
from frontend.service.heating_fuel_service import HeatingFuelService
from frontend.service.municipality_service import MunicipalityService
from frontend.service.needed_energy_service import NeededEnergyService

class BoilerComponent:
    def __init__(self, j_nd_save: float, i_nd_save: float):
        self.output_data: OutputData = OutputData()
        self.user_home_info: UserHomeInfo = None
        self.boiler_info: BoilerInfo = None
        self.db_data: BoilerDBData = BoilerDBData()

        self.municipality_service = MunicipalityService()
        self.needed_energy_service = NeededEnergyService()
        self.heating_fuel_service = HeatingFuelService()

        self.joinery_nd_savings = j_nd_save
        self.insulation_nd_savings = i_nd_save

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

    # ==========================================================================
    # Load data from database
    # ==========================================================================

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

    # ==========================================================================
    # Do the calculation
    # ==========================================================================

    def start_calculation(self):
        payback_period = self.payback_period()
        self.output_data.payback_period = payback_period

        fin_en_savings = self.final_energy_savings()
        self.output_data.annual_final_energy_savings = fin_en_savings

        co2_em_red = self.co2_emission_reduction()
        self.output_data.co2_emission_reduction = co2_em_red

    def payback_period(self):
        investment_cost = self.boiler_info.investment_cost
        annual_cost_savings = self.annual_cost_savings()

        payback_period = investment_cost / annual_cost_savings

        return payback_period

    def annual_cost_savings(self):
        old_cost = self.annual_cost_old()
        new_cost = self.annual_cost_new()

        cost_savings = old_cost - new_cost

        self.output_data.cost_savings = cost_savings
        return cost_savings
    
    def annual_cost_old(self):
        old_fuel_cost_unit = self.user_home_info.fuel_cost_per_unit
        old_fuel_cons_kWh = self.db_data.heating_fuel.consumption_per_kWh
        old_fin_en = self.final_energy_old()

        old_cost = old_fin_en * old_fuel_cons_kWh * old_fuel_cost_unit

        return old_cost
    
    def final_energy_old(self):
        needed_en = self.needed_energy()
        old_total_eff = self.old_total_efficiency()

        old_fin_en = needed_en / old_total_eff

        return old_fin_en
    
    def needed_energy(self):
        needed_en_pure = self.needed_energy_pure()
        needed_savings = self.insulation_joinery_needed_energy_savings()

        needed_en = needed_en_pure - needed_savings

        return needed_en
    
    def needed_energy_pure(self):
        user_ann_fuel_cons = self.user_home_info.annual_fuel_consumption

        if user_ann_fuel_cons:
            needed_en_pure = self.user_needed_energy()
        else:
            needed_en_pure = self.db_needed_energy()

        return needed_en_pure
    
    def user_needed_energy(self):
        user_ann_fuel_cons = self.user_home_info.annual_fuel_consumption
        old_fuel_cons_kWh = self.db_data.heating_fuel.consumption_per_kWh
        old_total_eff = self.old_total_efficiency()

        user_needed_en = user_ann_fuel_cons * old_fuel_cons_kWh * old_total_eff

        return user_needed_en

    def old_total_efficiency(self):
        iso = self.user_home_info.pipe_system_isolated

        fuel_eff = self.db_data.heating_fuel.efficiency.heating_fuel
        pipe_sys_eff = 0.98 if iso else self.db_data.heating_fuel.efficiency.pipe_system
        pipe_reg_eff = self.db_data.heating_fuel.efficiency.pipe_regulation

        total_eff = fuel_eff * pipe_sys_eff * pipe_reg_eff

        return  total_eff
    
    def db_needed_energy(self):
        hdd_average = 2665.56
        floor_area = self.user_home_info.floor_area
        needed_en_m2 = self.db_data.needed_energy_per_m2
        hdd = self.db_data.hdd

        db_needed_energy = needed_en_m2 * (hdd / hdd_average) * floor_area

        return db_needed_energy
    
    def insulation_joinery_needed_energy_savings(self):
        joinery_savings = self.joinery_nd_savings
        insulation_savings = self.insulation_nd_savings

        needed_en_savings = joinery_savings + insulation_savings

        return needed_en_savings
    
    def annual_cost_new(self):
        new_fuel_cost_unit = self.boiler_info.new_fuel_cost_per_unit
        new_fuel_cons_kWh = self.db_data.new_heating_fuel.consumption_per_kWh
        new_fin_en = self.final_energy_new()

        old_cost = new_fin_en * new_fuel_cons_kWh * new_fuel_cost_unit

        return old_cost
    
    def final_energy_new(self):
        new_total_eff = self.total_efficiency_new()
        needed_en = self.needed_energy()

        fin_en_new = needed_en / new_total_eff
    
        return fin_en_new

    def total_efficiency_new(self):
        iso = self.user_home_info.pipe_system_isolated
        change = self.boiler_info.pipe_system_change
        ti = self.boiler_info.thermostat_installation

        fuel_eff = self.boiler_info.new_fuel_efficiency
        pipe_system_eff = 0.98 if change or iso else self.db_data.heating_fuel.efficiency.pipe_system
        pipe_reg_eff = 0.95 if ti else self.db_data.heating_fuel.efficiency.pipe_regulation

        total_eff_new = fuel_eff * pipe_system_eff * pipe_reg_eff

        return total_eff_new
    
    def final_energy_savings(self):
        old_fin_en = self.final_energy_old()
        new_fin_en = self.final_energy_new()

        fin_en_savings = old_fin_en - new_fin_en

        return fin_en_savings
    
    def co2_emission_reduction(self):
        old_co2_em = self.co2_emission_old()
        new_co2_em = self.co2_emission_new()

        co2_em_red = old_co2_em - new_co2_em

        return co2_em_red
    
    def co2_emission_old(self):
        fuel_co2_em = self.db_data.heating_fuel.co2_emission
        prim_en_old = self.primary_energy_old()

        co2_em_old = prim_en_old * fuel_co2_em

        return co2_em_old
    
    def primary_energy_old(self):
        prim_en_conv_factor = self.db_data.heating_fuel.prim_en_conv_factor
        final_en_old = self.final_energy_old()

        prim_en_old = final_en_old * prim_en_conv_factor

        return prim_en_old

    def co2_emission_new(self):
        fuel_co2_em = self.db_data.new_heating_fuel.co2_emission
        prim_en_new = self.primary_energy_new()

        co2_em_new = prim_en_new * fuel_co2_em

        return co2_em_new
    
    def primary_energy_new(self):
        prim_en_conv_factor = self.db_data.new_heating_fuel.prim_en_conv_factor
        final_en_new = self.final_energy_new()

        prim_en_new = final_en_new * prim_en_conv_factor

        return prim_en_new