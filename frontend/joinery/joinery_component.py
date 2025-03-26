from frontend.io_dataclass import *
from frontend.joinery.joinery_dataclasses import *
from frontend.service.heating_fuel_service import HeatingFuelService
from frontend.service.municipality_service import MunicipalityService
from frontend.service.needed_energy_service import NeededEnergyService
from frontend.service.joinery_service import JoineryService

HEATING_BREAK_COEFFICIENT = 0.85
HOURS_IN_DAY = 24
WATTS_IN_KILOWATTS = 1000

class JoineryComponent:
    def __init__(self):
        self.output_data: OutputData = OutputData()
        self.user_home_info: UserHomeInfo = None
        self.joinery_info: JoineryInfo = None
        self.db_data: JoineryDBData = JoineryDBData()

        self.municipality_service = MunicipalityService()
        self.needed_energy_service = NeededEnergyService()
        self.heating_fuel_service = HeatingFuelService()
        self.joinery_service = JoineryService()

    def calculate_output_data(
        self,
        user_home_info: UserHomeInfo,
        joinery_info: JoineryInfo
    ) -> OutputData:
        self.set_input_info(user_home_info, joinery_info)
        self.load_db_data()
        self.start_calculation()
        return self.output_data
    
    def set_input_info(
        self,
        user_home_info: UserHomeInfo,
        joinery_info: JoineryInfo
    ):
        self.user_home_info = user_home_info
        self.joinery_info = joinery_info

    # ==========================================================================
    # Load data from database
    # ==========================================================================

    def load_db_data(self):
        self.load_hdd()
        self.load_needed_energy()
        self.load_heating_fuel_parameters()
        self.load_air_changes_per_hour()
        self.load_window_U_old()
        self.load_door_U_old()

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

    def load_air_changes_per_hour(self):
        service = self.joinery_service

        wind_exp = self.joinery_info.wind_exposure.value
        airtghtnss = self.joinery_info.window_airtightness.value

        air_chngs_hour = service.get_air_changes_per_hour(wind_exp, airtghtnss)

        self.db_data.air_changes_per_hour = air_chngs_hour

    def load_window_U_old(self):
        service = self.joinery_service

        window_mat = self.joinery_info.window_material.value
        glazing = self.joinery_info.window_glazing.value

        window_U_old = service.get_window_U_old(window_mat, glazing)

        self.db_data.window_U_old = window_U_old   

    def load_door_U_old(self):
        service = self.joinery_service

        door_mat = self.joinery_info.door_material.value

        door_U_old = service.get_door_U_old(door_mat)

        self.db_data.door_U_old = door_U_old

    # ==========================================================================
    # Do the calculation
    # ==========================================================================

    def start_calculation(self):
        payback_period = self.payback_period()
        self.output_data.payback_period = payback_period

        co2_em_red = self.co2_emission_reduction()
        self.output_data.co2_emission_reduction = co2_em_red

    def payback_period(self):
        investment_cost = self.joinery_info.investment_cost
        annual_cost_savings = self.annual_cost_savings()

        payback_period = investment_cost / annual_cost_savings

        return payback_period
        
    def annual_cost_savings(self):
        fuel_unit_cost = self.user_home_info.fuel_cost_per_unit
        fuel_cons_kWh = self.db_data.heating_fuel.consumption_per_kWh
        fin_en_savings = self.annual_final_energy_savings()

        cost_savings = fin_en_savings * fuel_cons_kWh * fuel_unit_cost

        self.output_data.annual_cost_savings = cost_savings
        return cost_savings
    
    def annual_final_energy_savings(self):
        total_eff = self.total_efficiency()
        nd_en_savings = self.needed_energy_savings()

        fin_en_savings = nd_en_savings / total_eff

        self.output_data.annual_final_energy_savings = fin_en_savings
        return fin_en_savings

    def total_efficiency(self):
        iso = self.user_home_info.pipe_system_isolated

        fuel_eff = self.db_data.heating_fuel.efficiency.heating_fuel
        pipe_sys_eff = 0.98 if iso else self.db_data.heating_fuel.efficiency.pipe_system
        pipe_reg_eff = self.db_data.heating_fuel.efficiency.pipe_regulation

        total_eff = fuel_eff * pipe_sys_eff * pipe_reg_eff

        return  total_eff

    def needed_energy_savings(self):
        vent_loss_savings = self.ventilation_loss_savings()
        trans_loss_savings = self.transmission_loss_savings()
        real_cons_coef = self.real_consumption_coef()

        needed_en_savings = vent_loss_savings + trans_loss_savings
        needed_en_savings_real = needed_en_savings * real_cons_coef

        return needed_en_savings_real
    
    def ventilation_loss_savings(self):
        heating_break_coef = HEATING_BREAK_COEFFICIENT
        hours = HOURS_IN_DAY
        W_in_kW = WATTS_IN_KILOWATTS
        some_coef = 0.33 # TODO
        air_changes_new = 0.5 # TODO
        hdd = self.db_data.hdd
        air_changes_old = self.db_data.air_changes_per_hour
        heated_vol = self.heated_volume()

        air_chngs_diff = air_changes_old - air_changes_new
        vent_loss_savings_W = heating_break_coef * some_coef * air_chngs_diff \
                                                    * heated_vol * hdd * hours
        vent_loss_savings = vent_loss_savings_W / W_in_kW

        return vent_loss_savings
    
    def heated_volume(self):
        floor_area = self.user_home_info.floor_area
        height = self.user_home_info.height

        heated_volume = floor_area * height

        return heated_volume
    
    def transmission_loss_savings(self):
        heating_break_coef = HEATING_BREAK_COEFFICIENT
        hours = HOURS_IN_DAY
        W_in_kW = WATTS_IN_KILOWATTS
        win_U_new = self.joinery_info.window_U_new
        win_area = self.joinery_info.window_area
        door_U_new = self.joinery_info.door_U_new
        door_area = self.joinery_info.door_area
        win_U_old = self.db_data.window_U_old
        door_U_old = self.db_data.door_U_old
        hdd = self.db_data.hdd

        win_U_diff = (win_U_old - win_U_new) * win_area
        door_U_diff = (door_U_old - door_U_new) * door_area

        trans_loss_savings = heating_break_coef * (win_U_diff + door_U_diff) * \
                                hdd * hours / W_in_kW
        
        return trans_loss_savings

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
        hdd_average = 2665.56
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
        conv_factor = self.db_data.heating_fuel.prim_en_conv_factor
        fin_en_savings = self.annual_final_energy_savings()

        prim_en_savings = fin_en_savings * conv_factor

        return prim_en_savings
