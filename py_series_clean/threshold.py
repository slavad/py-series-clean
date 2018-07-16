import numpy as np
import py_series_clean.clean as pscc
import pdb

def generate_random_series(time_grid_len, number_of_series, sigma):
    """generates an array of random normal values (time_grid_len,number_of_series)"""
    result = np.random.normal(loc=0.0, scale=sigma, size=(time_grid_len, number_of_series))
    return result

def estimate_threshold(time_grid_and_values, numbe_of_random_series, sigma, khi):
    """estimate treshold for the given params"""
    time_grid = time_grid_and_values[0]
    values = time_grid_and_values[1]
    max_freq = pscc.estimate_max_freq(time_grid)
    number_of_freq_estimations = pscc.calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )
    random_series = generate_random_series(time_grid.shape[1], numbe_of_random_series, sigma)
    random_dirty_vector = pscc.calculate_dirty_vector(
        time_grid, random_series, number_of_freq_estimations, max_freq, values.shape[1]
    )