import numpy as np
from matplotlib import  pyplot as plt
import matplotlib.animation as animation
import time


from scripts.enthalpy import calculate_temperatures_from_enthalpy_nparr
from scripts.sim2d import  Sim2DWorld


# beeswax heat capacity, J/(g*K). sources seem to vary -
# value from Putra et al section 3.4, assuming the 2084 kJ/kg*K in text was missing decimal
C = 2.084
# Density, g/cm^2. Imagining 0.5 cm thick beeswax, at 0.95 g/cm^3
wax_depth  = 0.5
p = 0.95 * wax_depth
# Latent heat of fusion, J/g - from Putra et al, 2020
L_a = 150
# Temps for western honeybee wax - from Buchwald et al. The thermal properties of beeswax, 2008
# actual values around 40, 67 C - cchoosing 45, 60 for the linear approximation
T_freeze = 45
T_onset = 60
# Buchwald et al 2008 cites Southwick 1985 saying western honeybee beeswax
# heat conductivity is 0.36 * 10^-3 cal / (cm * sec * K)
# Converts to 0.0015 W/cm*K, multiply by wax depth to get heat conductivity in 2d.
k_2d = 0.0015 * wax_depth # units are Watts/Kelvin = power per unit width / kelvin per length temp gradient

# Loss rate to external environment - watts per unit area degree kelvin 
# P = const * Area * temp difference
# Glass conductivity is 1 watt/m*K = 0.01 watts/(cm*K)
# For glass thickness 1 cm, loss rate is  0.01 (W/cm*K) * 1/(1cm) = 0.01 (W/cm^2*K)
# For 0.5 cm, it's 0.02 W/(cm^2*K)
loss_rate_watts_per_cm2_deg_kelvin = 0.01 / 0.5

# Outside temperature to calculate heat loss from - 40 is high for a room temp but this is just an example
outside_temperature = 40

def plot_crystallized_enthalpies():
    fig, ax = plt.subplots()
    
    E = np.linspace(0,200,100)
    T_crystallized = calculate_temperatures_from_enthalpy_nparr(E, np.ones(100), C, p, L_a, T_freeze, T_onset)
    T_uncrystallized = calculate_temperatures_from_enthalpy_nparr(E, np.zeros(100), C, p, L_a, T_freeze, T_onset)
    
    ax.plot(E, T_uncrystallized, '--', label="With no phase transition from liquid")
    ax.plot(E, T_crystallized, label="With crystallization to solid")
    ax.set_xlabel("Enthalpy (J/cm^2)")
    ax.set_ylabel("Temperature ($^\circ$C)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    wax_props = {
        "C": C,
        "p": p,
        "L_a": L_a,
        "T_freeze": T_freeze,
        "T_onset": T_onset,
        "k_2d": k_2d,
        "outside_temperature": outside_temperature,
        "loss_rate_watts_per_cm2_deg_kelvin": loss_rate_watts_per_cm2_deg_kelvin,
    }
    
    w = Sim2DWorld(wax_props)
    
    w.cell_enthalpies_per_area.fill(120)
    
    w.cell_enthalpies_per_area[80:120,80:120] = 150
    
    nframes = 100
    steps_per_frame = 100
    
    temp_history = np.zeros((nframes, w.size_horizontal, w.size_vertical),dtype=float)
    tot_enths = np.zeros(nframes, dtype=float)
    
    t_start = time.time()
    for i in range(nframes):
        for j in range(steps_per_frame):
            w.do_simulation_step()
            # w.diffuse_heat()
        temp_history[i,:,:] = w.calculate_temperatures()
        tot_enths[i] = w.total_enthalpy()
    
    t_end = time.time()
    print("real time elapsed for {} frames = {}".format(nframes, t_end-t_start))
    
    def plottimepoint(temp_map, tot_enth, time_index):
        # Clear the current plot figure
        plt.clf()

        plt.title(f"Temperature at t = {time_index*steps_per_frame*w.sim_delta_t:.3f} seconds, E={tot_enth:.1f}")
        
        plt.pcolormesh(temp_map, cmap=plt.cm.jet, vmin=20, vmax=80)
        plt.colorbar()

        return plt
        
    def animate(k):
        plottimepoint(temp_history[k], tot_enths[k], k)
    
    anim = animation.FuncAnimation(plt.figure(), animate, interval=1, frames=nframes, repeat=False)
    anim.save("animation.gif")
    # plt.show()
    