import numpy as np
import pdb

def clean(time_grid_and_values, khi, treshold):
    """do clean"""
    time_grid = time_grid_and_values[0]
    values = time_grid_and_values[1]
    max_freq = estimate_max_freq(time_grid)
    number_of_freq_estimations = calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )
    dirty_vector = calculate_dirty_vector(
        time_grid, values, number_of_freq_estimations, max_freq
    )
    weights_vector = calculate_weights_vector(
        time_grid, values, number_of_freq_estimations, max_freq
    )
    super_resultion_vector = build_super_resultion_vector(number_of_freq_estimations)
    dirty_subvector = dirty_vector[number_of_freq_estimations:]
    normalized_detection_treshold = calc_normalized_detection_treshold(
        dirty_subvector, number_of_freq_estimations, treshold
    )

def estimate_max_freq(time_grid, use_min=True):
    """estimates maximum frequency that can be found"""
    """if use_min is True, then minimum delta T is used"""
    """otherwise average delta T is used"""
    """eq 146 in ref 2"""
    reshaped_time_grid = time_grid.reshape(1,-1)
    distance_vector = reshaped_time_grid[0][1:] - reshaped_time_grid[0][:-1]
    if use_min:
        delta = distance_vector.min()
    else:
        delta = np.average(distance_vector)
    return 1/(2*delta)

def calculate_estimations_vector_size(max_freq, time_grid, khi):
    """eq 147 in ref 2"""
    result = khi*max_freq*(time_grid[-1][0] - time_grid[0][0])
    return int(np.ceil(result))

def calculate_current_freq(max_freq, index, number_of_freq_estimations):
    """calculates frequency for eq 148 and 149 in ref 2"""
    return index*max_freq/number_of_freq_estimations

def generate_index_vector(vector_size):
    """generates index vector: from -max_index to max_index"""
    if vector_size % 2 == 0:
        raise ValueError("matrix_size must be odd")
    max_index = (vector_size - 1)/2
    index_vector = np.arange(-max_index, max_index + 1, 1).reshape(-1,1)
    return index_vector

def build_exp_matrix(time_grid, values, index_vector, number_of_freq_estimations, max_freq):
    """builds (index_vector.shape[0])xN exp matrix for usage in eq 148 and 149 ref 2"""
    # see eq 150 in ref 2
    freq_vector = index_vector*max_freq/number_of_freq_estimations
    # the result will be a rectangular matrix:
    matrix_for_exp = (-1j*2*np.pi*freq_vector)*time_grid.T
    exp_vector = np.exp(matrix_for_exp)
    result = np.matmul(exp_vector, values)/values.shape[0]
    return result

def calculate_dirty_vector(time_grid, values, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    index_vector = generate_index_vector(2*number_of_freq_estimations + 1)
    result = build_exp_matrix(
        time_grid, values, index_vector, number_of_freq_estimations, max_freq
    )
    return result

def calculate_weights_vector(time_grid, values, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    index_vector = generate_index_vector(4*number_of_freq_estimations + 1)
    values = np.ones((values.shape[0],1))
    result = build_exp_matrix(
        time_grid, values, index_vector, number_of_freq_estimations, max_freq
    )
    return result

def build_super_resultion_vector(number_of_freq_estimations):
    """eq 151 in ref 2"""
    vector_size = 2*number_of_freq_estimations + 1
    return np.ones((vector_size,1))

def calc_normalized_detection_treshold(dirty_vector, number_of_freq_estimations, treshold):
    """eq 152 and 153 in ref 2"""
    drirty_vector_norm = np.power(
        np.abs(dirty_vector), 2
    ).sum()/(number_of_freq_estimations + 1)
    result = drirty_vector_norm*treshold
    return result