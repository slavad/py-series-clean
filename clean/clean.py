from helpers.common_imports import *
import clean.matrix_builder as mb
import clean.iterator as itr
import clean.restorer as rst

def clean(time_grid_and_values, khi, treshold, max_iterations, harmonic_share, use_aver):
    """do clean"""
    time_grid = time_grid_and_values[0]
    values = time_grid_and_values[1]
    max_freq = mb.estimate_max_freq(time_grid, use_aver)
    number_of_freq_estimations = mb.calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )

    iterator = itr.Iterator(
        treshold,
        harmonic_share, number_of_freq_estimations,
        time_grid, values, max_freq
    )

    super_resultion_vector, iterations = iterator.iterate(max_iterations)
    restorer = rst.Restorer(
        super_resultion_vector, iterations,
        number_of_freq_estimations, time_grid, max_freq
    )
    if iterations != 0:
       uniform_time_grid = restorer.uniform_time_grid
       freq_vector = restorer.freq_vector
       freqs, amplitudes, phases = restorer.restore_fap()
       clean_spectrum, correlogram, uniform_series = restorer.restore_ccs()
       return iterations, uniform_time_grid, clean_spectrum, correlogram, uniform_series, freq_vector, freqs, amplitudes, phases
    else:
        return None
