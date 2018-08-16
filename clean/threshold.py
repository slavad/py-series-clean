from helpers.common_imports import *
import clean.matrix_builder as mb
import clean.schuster as sch

class Threshold(object):
    """estimate treshold for the given params"""

    def __init__(self, time_grid_and_values, sigma, khi):
        """estimate treshold for the given params"""
        self.__time_grid = time_grid_and_values[0]
        self.__values = time_grid_and_values[1]
        self.__sigma = sigma
        self.__khi = khi
        self.__max_freq = mb.estimate_max_freq(self.__time_grid)
        self.__number_of_freq_estimations = mb.calculate_estimations_vector_size(
            self.__max_freq, self.__time_grid, self.__khi
        )

    def estimate(self, number_of_random_series):
        """estimates the treshold"""
        random_series = self.__generate_random_series(number_of_random_series)
        threshold = self.__find_max_counts_and_relation(
            random_series, self.__values
        )
        return threshold

    def __generate_random_series(self, number_of_random_series):
        """generates an array of random normal values (time_grid_len,number_of_series)"""
        time_grid_len = self.__time_grid.shape[0]
        result = np.random.normal(loc=0.0, scale=self.__sigma, size=(time_grid_len, number_of_random_series))
        return result

    def __find_max_counts_and_relation(self, random_series, values):
        """
            Finds the number of maximun counts in the
            Schuster periodorgrams for the random series
            that are > than the average
            count in the Schuster periodorgram for the examined observation,
            then calculates the relation of the number above
            to the total number of the random series.
        """
        number_of_random_series = random_series.shape[1]
        max_counts_random = sch.calc_schuster_counts(random_series, method_flag='max')
        average_count_series = sch.calc_schuster_counts(values, method_flag='average')[0]
        # extract ids that fit to our condition
        ids_list = np.where(max_counts_random >= average_count_series)
        count_of_items = ids_list[0].shape[0]
        # the probabilty that the examined series contain noise only:
        relation = count_of_items/number_of_random_series
        # the probabilty that the examined series contain also signal:
        return 1 - relation
