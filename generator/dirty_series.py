from helpers.common_imports import *

class DirtySeries(object):
    """generates time grid and noisy observations"""
    def __init__(self, time_grid_length, max_time_value, frequencies, amplitudes, phases, sigma):
        self.__time_grid_length = time_grid_length
        self.__max_time_value = max_time_value
        # all args should be in the same units: e.g. secs
        # can be both scalars or vectors, but the must be of
        # the same shape: (n,1)
        reshaping_result = self.__check_and_reshape_arguments(frequencies, amplitudes, phases)
        self.__frequnecies = reshaping_result['frequencies']
        self.__amplitudes = reshaping_result['amplitudes']
        self.__phases = reshaping_result['phases']
        self.__sigma = sigma

    def generate(self):
        time_grid = self.__generate_random_time_grid()
        series = self.__generate_dirty_periodical_series(time_grid)
        return time_grid, series

    def __check_and_reshape_arguments(self, frequencies, amplitudes, phases):
        """reshapes arguments and check their shape"""
        new_frequencies = self.__reshape_one_value(frequencies)
        new_amplitudes = self.__reshape_one_value(amplitudes)
        new_phases = self.__reshape_one_value(phases)
        if (new_phases.shape != new_amplitudes.shape) or (new_frequencies.shape != new_phases.shape):
            raise ValueError("frequencies, amplitudes and phases must be scalars or must have the same shape")
        else:
            result = {
                'frequencies': new_frequencies,
                'amplitudes': new_amplitudes,
                'phases': new_phases
            }
            return result

    def __reshape_one_value(self, value):
        """converting to vectors if needed and reshaping"""
        if np.isscalar:
            return np.array(value).reshape(-1,1)
        else:
            return value.reshape(-1,1)

    def __generate_random_time_grid(self):
        """generates random time grid for test series"""
        result = np.sort(np.random.ranf(self.__time_grid_length)).reshape(-1,1)
        return result*self.__max_time_value

    def __generate_periodical_series(self, time_grid):
        """generates periodical series"""
        # broadcasting of time grid will be done automatically
        # after we add multiply it by circular_frequnecies.
        # the new shape will be (n,m)
        # where m is the height of time_grid.reshape(-1,1)
        # and n is the length of both self.__phases, self.__amplitudes and self.__frequencies
        current_phases = np.pi*2*self.__frequnecies*time_grid.T + self.__phases
        result = np.cos(current_phases)*self.__amplitudes
        return np.sum(result, axis=0).reshape(-1,1)

    def __generate_noise(self, shape):
        """generates noise to add to time grid"""
        return np.random.normal(loc=0.0, scale=self.__sigma, size=shape).reshape(-1, 1)

    def __generate_dirty_periodical_series(self, time_grid):
        # all args should be in the same units: e.g. secs
        """adds some random noise to the series"""
        result = self.__generate_periodical_series(time_grid)
        if self.__sigma != 0:
            result += self.__generate_noise(time_grid.shape)
        return result
