import numpy as np
import pdb

def clean(time_gird_and_values):
    """do clean"""
    max_freq = estimate_max_freq(time_gird_and_values[0])
    number_of_freq_estimations = calculate_estimations_array_size(max_freq, time_gird_and_values[0])
    calculate_weights_array(time_gird_and_values, number_of_freq_estimations, max_freq)

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

def calculate_current_freq(max_freq, index, number_of_freq_estimations):
    """calculates frequency for eq 148 and 149 in ref 2"""
    return index*max_freq/number_of_freq_estimations

def build_exp_matrix(time_gird, values, matrix_size, number_of_freq_estimations, max_freq):
    """builds (matrix_size)xN exp matrix for usage in eq 148 and 149 ref 2"""
    if matrix_size % 2 == 0:
        raise ValueError("matrix_size must be odd")
    max_index = (matrix_size - 1)/2
    freq_array = np.arange(-max_index, max_index + 1, 1)*max_freq/number_of_freq_estimations
    # the result will be a rectangular matrix:
    array_for_exp = (-1j*2*np.pi*freq_array.reshape(-1,1))*time_gird.reshape(1,-1)
    exp_array = np.exp(array_for_exp)
    result = np.matmul(exp_array, values.reshape(-1,1))/values.shape[1]
    return result

def calculate_dirty_array(time_gird_and_values, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    matrix_size = 2*number_of_freq_estimations + 1
    time_gird = time_gird_and_values[0]
    values = np.ones(time_gird_and_values[1])
    result = build_exp_matrix(time_gird, values, matrix_size, number_of_freq_estimations, max_freq)
    return result

def calculate_weights_array(time_gird_and_values, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    matrix_size = 4*number_of_freq_estimations + 1
    time_gird = time_gird_and_values[0]
    values = np.ones(time_gird_and_values[1].shape[1]).reshape(-1,1)
    result = build_exp_matrix(time_gird, values, matrix_size, number_of_freq_estimations, max_freq)
    return result