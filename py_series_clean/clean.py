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

    iterator = itr.Iterator(
        treshold, max_iterations,
        harmonic_share, number_of_freq_estimations,
        time_grid, values, max_freq
    )

    super_resultion_vector, iterations = iterator.iterate()

    restoration_result = rst.restore(
        super_resultion_vector, iterations,
        number_of_freq_estimations, time_grid, max_freq
    )
    if restoration_result:
       uniform_time_grid, clean_spectrum, correlogram, uniform_series, freq_vector,freqs,amplitudes, phases = restoration_result
       return iterations, uniform_time_grid, clean_spectrum, correlogram, uniform_series, freq_vector, freqs,amplitudes, phases
    else:
        return None
