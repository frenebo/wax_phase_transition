import numpy as np
# Model assumes that at onset of freezing, the phase transition starts abruptly, and then stops at freezing temp.
def calculate_temperatures_from_enthalpy_nparr(
    E, # Enthalpies numpy array, J/(cm^2)
    can_crystalize, # Boolean numpy array -  whether to assume it can freeze
    C, # Specific heat capacity, J/(g*K)
    p, # Density, g/(cm^2)
    L_a, # Latent heat of fusion, J/g
    T_freeze, # Temperature at which wax finishes freezing
    T_onset, # Temperature at which wax begins to freeze
    ):
    lam = p*C # heat capacity per cm^2
    L = p*L_a # Latent heat of fusion per cm^2
    
    """
    Using piecewise function for enthalpy change during freezing
    E(T)=lam*T + L*f(T)
    f(T) = {
        0                               if T < T_freeze
        (T-T_freeze)/(T_onset-T_freeze) if T_freeze <= T <= T_onset
        1                               if T  > T_onset
    }
    Reversing gives:
    T(E) = {
        E/lam                           if E < E_freeze
         (E + L*T_f/(T_on - T_f))
        -------------------------       if E_f <= E <= E_on
          (lam + L/(T_on - T_f))
        (E - L)/lam                     if E > E_onset
    }
    """
    
    E_freeze = lam * T_freeze
    E_onset = lam * T_onset + L
    
    # If too hot to crystallize, or not able to crystallize
    uncrystallizable_mask = np.logical_or(E > E_onset, np.logical_not(can_crystalize))
    # If able to crystallize and under freezing enthalpy
    totally_crystallized_mask = np.logical_and(E < E_freeze, can_crystalize)
    # If able to crystalize, and neither under freezing enthalpy nor too hot to crystallize
    within_phase_transition_mask = np.logical_not(np.logical_or(
        uncrystallizable_mask,
        totally_crystallized_mask
    ))
    
    # if E > E_onset or (not can_crystalize):
    uncrystallized_temps =  (E - L) / lam
    # elif E < E_freeze:
    totally_crystallized_temps = E / lam
    # else:
    num =  E + L * T_freeze / (T_onset - T_freeze)
    denom = (lam + L / (T_onset - T_freeze))
    part_crystallized_temps = num / denom

    
    return (
        uncrystallizable_mask * uncrystallized_temps +
        totally_crystallized_mask * totally_crystallized_temps +
        within_phase_transition_mask * part_crystallized_temps
    )
    