import numpy as np
import py_series_clean.matrix_builder as mb
import py_series_clean.iterator as itr
import py_series_clean.restorer as rst
import pdb

def clean(time_grid_and_values, khi, treshold, max_iterations, harmonic_share):
    """do clean"""
    time_grid = time_grid_and_values[0]
    values = time_grid_and_values[1]
    max_freq = mb.estimate_max_freq(time_grid)
    number_of_freq_estimations = mb.calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )

    super_resultion_vector, iterations = itr.iterate(
        treshold, max_iterations,
        harmonic_share, number_of_freq_estimations,
        time_grid, values, max_freq
    )
    restoration_result = rst.restore(
        super_resultion_vector, iterations,
        number_of_freq_estimations, time_grid, max_freq
    )
    if restoration_result:
       uniform_time_grid, clean_spectrum, correlogram, uniform_series = restoration_result
       return iterations, uniform_time_grid, clean_spectrum, correlogram, uniform_series
    else:
        return None
