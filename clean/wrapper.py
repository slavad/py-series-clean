from helpers.common_imports import *
import clean.matrix_builder as mb
import clean.iterator as itr
import clean.restorer as rst
class Wrapper(object):
    """
        wraps Iterator, Restorer and DetectionTreshold classes
    """
    def __init__(self, time_grid, khi, use_aver):
        self.__time_grid = time_grid
        self.__use_aver = use_aver
        self.__max_freq = mb.estimate_max_freq(self.__time_grid, self.__use_aver)
        self.__number_of_freq_estimations = mb.calculate_estimations_vector_size(
            self.__max_freq, self.__time_grid, khi
        )

    def clean(self, values, false_alarm_probability, max_iterations, harmonic_share):
        """do clean"""
        iterator = itr.Iterator(
            false_alarm_probability,
            harmonic_share, self.__number_of_freq_estimations,
            self.__time_grid, values, self.__max_freq
        )

        iterations_result = iterator.iterate(max_iterations)
        restorer = rst.Restorer(
            iterations_result['super_resultion_vector'], iterations_result['iterations'],
            self.__number_of_freq_estimations, self.__time_grid, self.__max_freq
        )

        restoration_result = restorer.restore()

        return restoration_result
