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

def find_max_counts_and_relation(random_series, values):
    """
        Finds the number of maximun counts in the
        Schuster periodorgrams for the random series
        that are > than the average
        count in the Schuster periodorgram for the examined observation,
        then calculates the relation of the number above
        to the total number of the random series.
    """
    number_of_random_series = random_series.shape[1]
    max_counts_random = pscc.calc_schuster_counts(random_series, method_flag='max')
    average_count_series = pscc.calc_schuster_counts(values, method_flag='average')[0]
    # extract ids that fit to our condition
    ids_list = np.where(max_counts_random >= average_count_series)
    count_of_items = ids_list[0].shape[0]
    # the probabilty that the examined series contain noise only:
    relation = count_of_items/number_of_random_series
    # the probabilty that the examined series contain also signal:
    return 1 - relation

def estimate_threshold(time_grid_and_values, number_of_random_series, sigma, khi):
    """estimate treshold for the given params"""
    time_grid = time_grid_and_values[0]
    values = time_grid_and_values[1]
    max_freq = pscc.estimate_max_freq(time_grid)
    number_of_freq_estimations = pscc.calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )
    random_series = generate_random_series(time_grid.shape[0], number_of_random_series, sigma)
    threshold = find_max_counts_and_relation(
        random_series, values
    )
    return threshold