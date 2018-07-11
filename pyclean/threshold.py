import numpy as np

def generate_random_seq(time_grid_len, number_of_seq, sigma):
    """generates an array of random normal values (time_grid_len,number_of_seq)"""
    return np.random.normal(loc=0.0, scale=sigma, size=(time_grid_len, number_of_seq))
