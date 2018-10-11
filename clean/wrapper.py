from helpers.common_imports import *
import clean.matrix_builder as mb
import clean.iterator as itr
import clean.restorer as rst
import clean.detection_treshold as dtr

class Wrapper(object):
    """
        wraps Iterator, Restorer and DetectionTreshold classes
    """
    def __init__(self, time_grid):
        self.__time_grid = time_grid

    def clean(self, values, detection_treshold, max_iterations, harmonic_share, khi, use_aver):
        """restores clean time series and spectrum from durty one"""
        max_freq = mb.estimate_max_freq(self.__time_grid, use_aver)
        number_of_freq_estimations = mb.calculate_estimations_vector_size(
            max_freq, self.__time_grid, khi
        )
        iterator = itr.Iterator(
            detection_treshold,
            harmonic_share, number_of_freq_estimations,
            self.__time_grid, values, max_freq
        )

        iterations_result = iterator.iterate(max_iterations)
        restorer = rst.Restorer(
            iterations_result['super_resultion_vector'], iterations_result['iterations'],
            number_of_freq_estimations, self.__time_grid, max_freq
        )

        restoration_result = restorer.restore()

        return restoration_result

    def estimate_detection_treshold(self, sigma, number_of_random_series, false_alarm_probability):
        """estimates detection treshold for a given time series"""
        estimator = dtr.DetectionTreshold(self.__time_grid, sigma)
        detection_treshold = estimator.estimate(number_of_random_series, false_alarm_probability)
        return detection_treshold
