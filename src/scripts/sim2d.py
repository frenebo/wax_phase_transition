import numpy as np
import scipy

from .enthalpy import calculate_temperatures_from_enthalpy_nparr


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
        self.cell_crystallization_status = np.zeros((size_horizontal, size_vertical), dtype=bool)
    
    def calculate_temperatures(self):
        return calculate_temperatures_from_enthalpy_nparr(
            self.cell_enthalpies_per_area,
            self.cell_crystallization_status,
            # **self.wax_props
            self.wax_props["C"],
            self.wax_props["p"],
            self.wax_props["L_a"],
            self.wax_props["T_freeze"],
            self.wax_props["T_onset"],
        )
        
    def diffuse_heat(self):
        cell_temps = self.calculate_temperatures()
        
        heat_transfer_kernel = self.wax_props["k_2d"] * np.array([
            [0,1,0],
            [1,-4,1],
            [0,1,0],
        ],dtype=float)
        # Use 'reflect' to pretend that just outside the boundaries, the temps are the same
        # Simulated insulation from otuside
        heat_transfer_rates = scipy.ndimage.convolve(cell_temps, heat_transfer_kernel, mode='reflect')
        
        cell_area = self.cell_size_cm ** 2
        self.cell_enthalpies_per_area += heat_transfer_rates * (self.sim_delta_t / cell_area)
    
    def total_enthalpy(self):
        return np.sum(self.cell_enthalpies_per_area) * ( self.cell_size_cm ** 2  )
        
        
        