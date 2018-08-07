import numpy as np
import pdb
#TODO: write tests
#TODO: move to the py_series_clean dir?
def generate_dirty_periodical_series_with_random_time_grid(time_grid_length, max_time_value, frequencies, amplitudes,phases, sigma):
    """generates time grid and noisy observations"""
    time_grid = generate_random_time_grid(time_grid_length, max_time_value)
    series = generate_dirty_periodical_series(time_grid, frequencies, amplitudes,phases, sigma)
    return time_grid, series

def generate_random_time_grid(time_grid_length, max_time_value):
    """generates random time grid for test series"""
    result = np.sort(np.random.ranf(time_grid_length)).reshape(-1,1)
    return result*max_time_value

def generate_periodical_series(time_grid, frequencies, amplitudes,phases):
    """generates periodical series"""
    # all args should be in the same units: e.g. secs
    # can be both scalars or vectors, but the must be of
    # the same shape: (n,1)
    new_frequencies, new_amplitudes, new_phases = check_and_reshape_arguments(frequencies, amplitudes, phases)
    circular_frequnecies = 2*np.pi*new_frequencies
    # broadcasting of time grid will be done automatically
    # after we add divide it by circular_frequnecies.
    # the new shape will be (n,m)
    # where m is the height of time_grid.reshape(-1,1)
    # and n is the length of both new_phases, new_amplitudes and new_frequencies
    current_phases = time_grid.T/circular_frequnecies + new_phases
    result = np.cos(current_phases)*new_amplitudes
    return np.sum(result, axis=0).reshape(-1,1)

def generate_dirty_periodical_series(time_grid, frequencies, amplitudes,phases, sigma):
    # all args should be in the same units: e.g. secs
    """adds some random noise to the series"""
    noise = np.random.normal(loc=0.0, scale=sigma, size=time_grid.shape)
    result = noise + generate_periodical_series(time_grid, frequencies, amplitudes,phases)
    return result

def check_and_reshape_arguments(frequencies, amplitudes,phases):
    """reshapes arguments and check their shape"""
    shape_error = "both phases and shapes must be scalars or have the same shape"
    new_frequencies = reshape_one_value(frequencies)
    new_amplitudes = reshape_one_value(amplitudes)
    new_phases = reshape_one_value(phases)
    if (new_phases.shape != new_amplitudes.shape) or (new_frequencies.shape != new_phases.shape):
        raise ValueError("phases amplitudes and phases must be scalars or have the same shape")
    else:
        return new_frequencies, new_amplitudes, new_phases

def reshape_one_value(value):
    """converting to vectors if needed and reshaping"""
    if np.isscalar:
        return np.array(value).reshape(-1,1)
    else:
        return value.reshape(-1,1)