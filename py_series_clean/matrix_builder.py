import numpy as np
import pdb
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

def generate_index_vector(vector_size):
    """generates index vector: from -max_index to max_index"""
    if vector_size % 2 == 0:
        raise ValueError("matrix_size must be odd")
    max_index = (vector_size - 1)/2
    index_vector = np.arange(-max_index, max_index + 1, 1).reshape(-1,1)
    return index_vector

def build_exp_matrix(time_grid, values, index_vector, number_of_freq_estimations, max_freq, kind):
    """
        builds (index_vector.shape[0])xN exp matrix
        for usage in eq 148, 149, 160 and 161 ref 2
    """
    # direct or inverse FT
    # see eq 150 in ref 2
    freq_vector = index_vector*max_freq/number_of_freq_estimations
    if kind == 'direct':
        coeff = -1j
        norm = 1/values.shape[0]
    elif kind == 'inverse':
        coeff = 1j
        norm = values.shape[0]/number_of_freq_estimations
    else:
       raise ValueError("unknown kind")
    # the result will be a rectangular matrix:
    matrix_for_exp = (coeff*2*np.pi*freq_vector)*time_grid.T
    exp_vector = np.exp(matrix_for_exp)
    if kind == 'direct':
        exp_vector_for_mult = exp_vector
    elif kind == 'inverse':
        exp_vector_for_mult = exp_vector.T
    result = np.matmul(exp_vector_for_mult, values)*norm
    return result

def size_of_spectrum_vector(number_of_freq_estimations):
    """size of dirty vector"""
    return 2*number_of_freq_estimations + 1

def calculate_dirty_vector(time_grid, values, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    index_vector = generate_index_vector(size_of_spectrum_vector(number_of_freq_estimations))
    result = build_exp_matrix(
        time_grid, values, index_vector, number_of_freq_estimations, max_freq, 'direct'
    )
    return result

def size_of_window_vector(number_of_freq_estimations):
    """size of the window vector"""
    return 4*number_of_freq_estimations + 1

def calculate_window_vector(time_grid, number_of_freq_estimations, max_freq):
    """eq 148 in ref 2"""
    index_vector = generate_index_vector(size_of_window_vector(number_of_freq_estimations))
    values = np.ones((time_grid.shape[0],1))
    result = build_exp_matrix(
        time_grid, values, index_vector, number_of_freq_estimations, max_freq, 'direct'
    )
    return result

def build_super_resultion_vector(number_of_freq_estimations):
    """eq 151 in ref 2"""
    vector_size = 2*number_of_freq_estimations + 1
    return np.zeros((vector_size,1))*(0+0j)