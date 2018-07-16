import numpy as np
import py_series_clean.clean as pscc
import pdb

def generate_random_series(time_grid_len, number_of_series, sigma):
    """generates an array of random normal values (time_grid_len,number_of_series)"""
    return np.random.normal(loc=0.0, scale=sigma, size=(time_grid_len, number_of_series))

def estimate_threshold(time_gird_and_values, number_of_series, sigma, khi):
    """estimate treshold for the given params"""
    time_grid_len = time_gird_and_values[0].shape[1]
    max_freq = pscc.estimate_max_freq(time_gird_and_values[0])
    number_of_freq_estimations = pscc.calculate_estimations_vector_size(
        max_freq, time_gird_and_values[0], khi
    )
    random_series = generate_random_series(time_grid_len, number_of_series, sigma)
    pdb.set_trace()