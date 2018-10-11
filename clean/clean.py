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
    # TODO: refactor detection_treshold.py to accept the same args as
    # iterator.iterate: max_freq and number_of_freq_estimations should be caclulated separtely,
    # not inside detection_treshold.py
    # maybe refactor the current method to a class with two methods: clean and estimate treshold
    # max_freq and number_of_freq_estimations will be calculated in the __init__ method of this class
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
