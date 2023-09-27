import numpy as np
import scipy

from .enthalpy import calculate_temperatures_from_enthalpy_nparr
from .plot_crystallized_enthalpies import generate_proportion_crystallized_interpolator


class Sim2DWorld:
    def __init__(
        self,
        wax_props,
        cell_size_cm=0.05,
        size_horizontal=200,
        size_vertical=200,
        sim_delta_t=0.1,
        ):
        self.wax_props = wax_props
        self.cell_size_cm = cell_size_cm
        self.sim_delta_t = sim_delta_t
        
        self.size_horizontal = size_horizontal
        self.size_vertical = size_vertical
        
        self.cell_enthalpies_per_area = np.zeros((size_horizontal, size_vertical), dtype=float)
        self.cell_proportions_crystallized = np.zeros((size_horizontal, size_vertical), dtype=float)
        
        self.prop_stable_crystallized = generate_proportion_crystallized_interpolator()
    
    def calculate_temperatures(self):
        return calculate_temperatures_from_enthalpy_nparr(
            self.cell_enthalpies_per_area,
            self.cell_proportions_crystallized,
            self.prop_stable_crystallized,
            self.wax_props["C"],
            self.wax_props["p"],
            self.wax_props["L_a"],
            self.wax_props["T_freeze"],
            self.wax_props["T_onset"],
        )
        
    def do_simulation_step(self):
        enth_before = self.total_enthalpy()
        self.diffuse_heat()
        enth_mid = self.total_enthalpy()
        self.heat_loss_to_environment()
        enth_after = self.total_enthalpy()
        print("Heat diffusion enthalpy difference: {}".format(enth_mid - enth_before))
        print("Heat loss enthalpy difference: {}".format(enth_after - enth_mid))
    
    def propagate_crystallization(self):
        # Crystallization growth rate is proportional to u * (1 - u)  * (a(T) - u), where a
        # is the crystallization label that would be stable at the current temperature T
        u = self.cell_proportions_crystallized
        u * (1 - u) * ()
        # Diffusion
        
        
        # print("Difference in total enthalpy after simulation step, {}".format(enth_after - enth_before))
    
    def heat_loss_to_environment(self):
        cell_temps = self.calculate_temperatures()
        out_temp = self.wax_props["outside_temperature"]
        loss_rate = self.wax_props["loss_rate_watts_per_cm2_deg_kelvin"]
        
        cell_area = self.cell_size_cm ** 2
        
        temp_gradients = out_temp - cell_temps
        cell_loss_rates_watts = loss_rate * temp_gradients * cell_area
        cell_joules_lost = cell_loss_rates_watts * self.sim_delta_t
        
        print("Cell joules lost average: {}".format(np.mean(cell_joules_lost)))
        print("dt: {}".format(self.sim_delta_t))
        
        self.cell_enthalpies_per_area -= cell_joules_lost
        
        
    def diffuse_heat(self):
        cell_temps = self.calculate_temperatures()
        cell_area = self.cell_size_cm ** 2
        
        heat_transfer_kernel = self.wax_props["k_2d"] * np.array([
            [0,1,0],
            [1,-4,1],
            [0,1,0],
        ],dtype=float)
        # Use 'reflect' to pretend that just outside the boundaries, the temps are the same
        # Simulated insulation from otuside
        heat_transfer_rates = scipy.ndimage.convolve(cell_temps, heat_transfer_kernel, mode='reflect')
        print("Heat transfer rates: ", heat_transfer_rates.shape, heat_transfer_rates.dtype)
        print("Average heat transfer rate: {}".format(np.average(heat_transfer_rates * (self.sim_delta_t / cell_area))))
        
        self.cell_enthalpies_per_area += heat_transfer_rates * (self.sim_delta_t / cell_area)
    
    def 
    
    def total_enthalpy(self):
        return np.sum(self.cell_enthalpies_per_area) * ( self.cell_size_cm ** 2  )
        
        
        