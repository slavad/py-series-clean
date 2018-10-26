from helpers.common_imports import *
import clean.matrix_builder as mb
import clean.iterator as itr
import clean.restorer as rst

class Wrapper(object):
    """
        wraps Iterator, Restorer classes
    """
    def __init__(self, time_grid, values):
        self.__time_grid = time_grid
        self.__values = values
        reshaped_time_grid = self.__time_grid.reshape(1,-1)
        self.__distance_vector = reshaped_time_grid[0][1:] - reshaped_time_grid[0][:-1]

    def __estimate_max_freq(self, use_aver):
        """estimates maximum frequency that can be found"""
        """if self.__time_grid is True, then average delta T is used"""
        """otherwise minimum delta T is used"""
        """eq 146 in ref 2"""
        if use_aver:
            delta = np.average(self.__distance_vector)
        else:
            delta = self.__distance_vector.min()
        return 1/(2*delta)

    def __calculate_estimations_vector_size(self, max_freq, khi):
        """eq 147 in ref 2"""
        result = khi*max_freq*(self.__time_grid[-1][0] - self.__time_grid[0][0])
        return int(np.ceil(result))

    def clean(self, detection_treshold, max_iterations, harmonic_share, khi, use_aver):
        """restores clean time series and spectrum from durty one"""
        max_freq = self.__estimate_max_freq(use_aver)
        number_of_freq_estimations = self.__calculate_estimations_vector_size(
            max_freq, khi
        )
        iterator = itr.Iterator(
            detection_treshold,
            harmonic_share, number_of_freq_estimations,
            self.__time_grid, self.__values, max_freq
        )

        iterations_result = iterator.iterate(max_iterations)
        restorer = rst.Restorer(
            iterations_result['super_resultion_vector'], iterations_result['iterations'],
            number_of_freq_estimations, self.__time_grid, max_freq
        )

        restoration_result = restorer.restore()

        return restoration_result
