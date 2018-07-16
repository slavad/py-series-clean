import numpy as np
import py_series_clean.clean as pscc
import pdb

def generate_random_series(time_grid_len, number_of_series, sigma):
    """generates an array of random normal values (time_grid_len,number_of_series)"""
    result = np.random.normal(loc=0.0, scale=sigma, size=(time_grid_len, number_of_series))
    return result

def generate_index_vector(vector_size):
    """generates index vector: from 0 to vector_size"""
    index_vector = np.arange(0, vector_size + 1, 1).reshape(-1,1)
    return index_vector

def calculate_dirty_matrix(time_grid, random_series, number_of_freq_estimations, max_freq):
    """caclculates dirty matrix for Schuster periodorgram"""
    index_vector = generate_index_vector(number_of_freq_estimations)
    result = pscc.build_exp_matrix(
        time_grid, random_series, index_vector, number_of_freq_estimations, max_freq
    )
    return result
def find_max_counts(dirty_matrix_for_random_series):
    """max counts in Schuster periodogram"""
    arraq_of_abs = np.abs(dirty_matrix_for_random_series)
    #do we need to take max counts
    result = np.max(arraq_of_abs, axis=0).reshape(-1,1)
    return result

def estimate_threshold(time_grid_and_values, number_of_random_series, sigma, khi):
    """estimate treshold for the given params"""
    time_grid = time_grid_and_values[0]
    values = time_grid_and_values[1]
    max_freq = pscc.estimate_max_freq(time_grid)
    number_of_freq_estimations = pscc.calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )
    random_series = generate_random_series(time_grid.shape[0], number_of_random_series, sigma)
    # we need to calculate schuster periodogram, not this (eq 9 in ref 3):
    dirty_matrix_for_random_series = calculate_dirty_matrix(
        time_grid, random_series, number_of_freq_estimations, max_freq
    )
    max_counts = find_max_counts(dirty_matrix_for_random_series)