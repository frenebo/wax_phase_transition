import numpy as np
from matplotlib import pyplot as plt
import scipy

def sigmoid_func(x,b,c):
    return 1 / (1 + np.exp(-b*(x-c)))

def unnormalized_latent_heat_curve(x):
    return sigmoid_func(x,0.13,93) * sigmoid_func(x,-2.22,65.7)

def normalization_const_for_latent_heat_curve():
    integral, err = scipy.integrate.quad(unnormalized_latent_heat_curve, 0, 75)
    return 1 / integral

def generate_proportion_crystallized_interpolator():
    A_norm = normalization_const_for_latent_heat_curve()
    normalized_lat_heat_curve = lambda t: A_norm * unnormalized_latent_heat_curve(t)
    test_T = np.linspace(-100,200,1000)
    
    test_props_crystallized = [scipy.integrate.quad(normalized_lat_heat_curve, temp, 200) for temp in test_T]
    test_props_crystallized = np.array(test_props_crystallized)
    
    interpolator = scipy.interpolate.RegularGridInterpolator((test_T,),test_props_crystallized)
    
    return interpolator

# def proportion_crystallized(temp):
#     A_norm = normalization_const_for_latent_heat_curve()
#     normalized_lat_heat_curve = lambda t: A_norm * unnormalized_latent_heat_curve(t)
    
#     # assert temp 
#     if temp > 75:
#         return 0
#     if temp < 0:
#         return 1
    
#     scipy.integrate(normalized_lat_heat_curve, temp, 75)

# if __name__ == "__main__":
#     t = np.linspace(0,75,300)
#     # A_norm = normalization_const_for_latent_heat_curve()
#     # l = A_norm * unnormalized_latent_heat_curve(t)
    
#     example_int = generate_proportion_crystallized_interpolator()
#     plt.plot(t,example_int(t))
#     plt.show()

# def latent_heat_per_deg_kelvin()
