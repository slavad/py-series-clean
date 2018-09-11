from helpers.common_imports import *
import clean.matrix_builder as mb
import clean.iterator as itr
import clean.restorer as rst

def clean(time_grid, values, khi, false_alarm_probability, max_iterations, harmonic_share, use_aver):
    """do clean"""
    max_freq = mb.estimate_max_freq(time_grid, use_aver)
    number_of_freq_estimations = mb.calculate_estimations_vector_size(
        max_freq, time_grid, khi
    )

    iterator = itr.Iterator(
        false_alarm_probability,
        harmonic_share, number_of_freq_estimations,
        time_grid, values, max_freq
    )

    iterations_result = iterator.iterate(max_iterations)
    restorer = rst.Restorer(
        iterations_result['super_resultion_vector'], iterations_result['iterations'],
        number_of_freq_estimations, time_grid, max_freq
    )

    restoration_result = restorer.restore()

    return restoration_result
