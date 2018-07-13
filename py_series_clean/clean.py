import numpy as np
import pdb

def clean(time_gird_and_values, khi, treshold):
    """do clean"""
    max_freq = estimate_max_freq(time_gird_and_values[0])
    number_of_freq_estimations = calculate_estimations_vector_size(max_freq, time_gird_and_values[0], khi)
    dirty_vector = calculate_dirty_vector(time_gird_and_values, number_of_freq_estimations, max_freq)
    weights_vector = calculate_weights_vector(time_gird_and_values, number_of_freq_estimations, max_freq)
    super_resultion_vector = build_super_resultion_vector(number_of_freq_estimations)
    normalized_detection_treshold = calc_normalized_detection_treshold(dirty_vector, number_of_freq_estimations, treshold)

def estimate_max_freq(time_gird, use_min=True):
    """estimates maximum frequency that can be found"""
    """if use_min is True, then minimum delta T is used"""
    """otherwise average delta T is used"""
    """eq 146 in ref 2"""
    distance_vector = time_gird[0][1:] - time_gird[0][:-1]
    if use_min:
        delta = distance_vector.min()
    else:
        delta = np.average(distance_vector)
    return 1/(2*delta)

def calculate_estimations_vector_size(max_freq, time_gird, khi):
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
    freq_vector = np.arange(-max_index, max_index + 1, 1)*max_freq/number_of_freq_estimations
    # the result will be a rectangular matrix:
    matrix_for_exp = (-1j*2*np.pi*freq_vector.reshape(-1,1))*time_gird.reshape(1,-1)
    exp_vector = np.exp(matrix_for_exp)
    result = np.matmul(exp_vector, values.reshape(-1,1))/values.shape[1]
    return result

def calculate_dirty_vector(time_gird_and_values, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    matrix_size = 2*number_of_freq_estimations + 1
    time_gird = time_gird_and_values[0]
    values = time_gird_and_values[1]
    result = build_exp_matrix(time_gird, values, matrix_size, number_of_freq_estimations, max_freq)
    return result

def calculate_weights_vector(time_gird_and_values, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    matrix_size = 4*number_of_freq_estimations + 1
    time_gird = time_gird_and_values[0]
    values = np.ones(time_gird_and_values[1].shape[1]).reshape(-1,1)
    result = build_exp_matrix(time_gird, values, matrix_size, number_of_freq_estimations, max_freq)
    return result

def build_super_resultion_vector(number_of_freq_estimations):
    """eq 151 in ref 2"""
    vector_size = 2*number_of_freq_estimations + 1
    return np.ones(vector_size).reshape(-1,1)

def calc_normalized_detection_treshold(dirty_vector, number_of_freq_estimations, treshold):
    """eq 152 and 153 in ref 2"""
    drirty_vector_norm = np.power(np.abs(dirty_vector), 2).sum()/(number_of_freq_estimations + 1)
    result = drirty_vector_norm*treshold
    return result