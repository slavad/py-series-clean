import numpy as np
import py_series_clean.matrix_builder as mb
import pdb

def restore(super_resultion_vector, iterations, number_of_freq_estimations, time_grid, max_freq):
    """restores clean spectrum, algorithm steps 18 to 21 ref 2"""
    # if nothing was detected:
    if iterations == 0:
        return None
    else:
        clean_window_vector = build_clean_window_vector(
            number_of_freq_estimations, time_grid, max_freq
        )
        clean_spectrum = build_clean_spectrum(
            clean_window_vector, super_resultion_vector, number_of_freq_estimations
        )

def build_uniform_time_grid(time_grid):
    """eq 158 ref 2"""
    step_size = (time_grid[-1][0] - time_grid[0][0])/(time_grid.shape[0] - 1)
    start = 0
    stop = step_size*time_grid.shape[0]
    result = np.arange(start,stop,step_size).reshape(-1,1)
    return result

def build_clean_spectrum(clean_window_vector, super_resultion_vector, number_of_freq_estimations):
    """eq 159 ref 2"""
    number_of_rows = super_resultion_vector.shape[0]
    array = []
    for index in range(0, number_of_rows):
        #TODO: check correctness of the index shifts:
        min_index = 2*number_of_freq_estimations - index
        max_index = 4*number_of_freq_estimations + 1 - index
        subvector = clean_window_vector[min_index:max_index]
        array.append(np.matmul(super_resultion_vector.T, subvector)[0][0])
    result = np.array(array).reshape(-1,1)
    return result

def build_clean_window_vector(number_of_freq_estimations, time_grid, max_freq):
    """eq 157 ref 2"""
    uniform_time_grid = build_uniform_time_grid(time_grid)
    clean_window_vector = mb.calculate_window_vector(
        uniform_time_grid, number_of_freq_estimations, max_freq
    )
    return clean_window_vector