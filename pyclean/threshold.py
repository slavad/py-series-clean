import numpy as np

def generate_random_series(time_grid_len, number_of_series, sigma):
    """generates an array of random normal values (time_grid_len,number_of_series)"""
    return np.random.normal(loc=0.0, scale=sigma, size=(time_grid_len, number_of_series))
