import numpy as np
import pdb

def clean(time_gird_and_values):
    """do clean"""
    max_freq = estimate_max_freq(time_gird_and_values[0])
    m_arr_size = calculate_estimations_array_size(max_freq, time_gird_and_values[0])
    pdb.set_trace()

def estimate_max_freq(time_gird, use_min=True):
    """estimates maximum frequency that can be found"""
    """if use_min is True, then minimum delta T is used"""
    """otherwise average delta T is used"""
    """eq 146 in ref 2"""
    distance_array = time_gird[0][1:] - time_gird[0][:-1]
    delta = 0
    if use_min:
        delta = distance_array.min()
    else:
        delta = np.average(distance_array)
    return 1/(2*delta)

def calculate_estimations_array_size(max_freq, time_gird, khi=4):
    """eq 147 in ref 2"""
    result = khi*max_freq*(time_gird[0][-1] - time_gird[0][0])
    return int(np.ceil(result))