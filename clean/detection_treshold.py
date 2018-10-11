from helpers.common_imports import *
import clean.schuster as sch

class DetectionTreshold(object):
    """estimate false alarm probability for the given params"""

    def __init__(self, time_grid, sigma):
        """estimate false alarm probability for the given params"""
        self.__time_grid = time_grid
        self.__sigma = sigma

    def estimate(self, number_of_random_series, false_alarm_probability):
        """estimates the false alarm probability"""
        if false_alarm_probability <= 0 or false_alarm_probability > 1:
            raise ValueError('false_alarm_probability should be > 0 and < 1')
        random_series = self.__generate_random_series(number_of_random_series)
        detection_treshold = self.__find_detection_treshold(
            random_series, false_alarm_probability
        )
        return detection_treshold

    def __generate_random_series(self, number_of_random_series):
        """generates an array of random normal values (time_grid_len,number_of_series)"""
        time_grid_len = self.__time_grid.shape[0]
        result = np.random.normal(loc=0.0, scale=self.__sigma, size=(time_grid_len, number_of_random_series))
        return result

    def __find_detection_treshold(self, random_series, false_alarm_probability):
        """
            Finds value D_q in eq 152 ref 2.
            1. It calculates a bunch of random series for the same time grid as examined series has
            2. It calcluates Schuster periodogram counts for the random series and time series (D^k_max)
            3. Finds D_q for which N/L <= false_alarm_probability, here L is total number of random series
            and N is number of random series for which D^k_max >= D_q
        """
        number_of_random_series = random_series.shape[1]
        max_counts_random = np.sort(
            sch.calc_schuster_counts(random_series, method_flag='max')
        )
        desired_count_index = int(
            np.ceil(
                false_alarm_probability*number_of_random_series
            )
        ) - 1
        # indexes start with zero, but in the case when false_alarm_probability = 0,
        # we will get first element of the array, which makes no sense
        desired_count =  max_counts_random[desired_count_index]
        return desired_count
