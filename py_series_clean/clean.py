import numpy as np
import py_series_clean.matrix_builder as mb
import py_series_clean.iterator as itr

def clean(time_grid_and_values, khi, treshold, max_iterations, harmonic_share):
    """do clean"""
    time_grid = time_grid_and_values[0]
    values = time_grid_and_values[1]
    max_freq = mb.estimate_max_freq(time_grid)
    number_of_freq_estimations = mb.calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )
    dirty_vector = mb.calculate_dirty_vector(
        time_grid, values, number_of_freq_estimations, max_freq
    )
    window_vector = mb.calculate_window_vector(
        time_grid, values, number_of_freq_estimations, max_freq
    )
    super_resultion_vector = itr.iterate(
        dirty_vector, window_vector, treshold,
        max_iterations, harmonic_share, number_of_freq_estimations
    )
