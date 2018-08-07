import numpy as np
import pdb
#TODO: write tests
#TODO: move to the py_series_clean dir?
def generate_dirty_periodical_series_with_random_time_grid(time_grid_length, max_time_value, periods, shifts,amplitudes, sigma):
    """generates time grid and noisy observations"""
    time_grid = generate_random_time_grid(time_grid_length, max_time_value)
    series = generate_dirty_periodical_series(time_grid, periods, shifts,amplitudes, sigma)
    return time_grid, series

def generate_random_time_grid(time_grid_length, max_time_value):
    """generates random time grid for test series"""
    result = np.sort(np.random.ranf(time_grid_length)).reshape(-1,1)
    return result*max_time_value

def generate_periodical_series(time_grid, periods, shifts,amplitudes):
    """generates periodical series"""
    # all args should be in the same units: e.g. secs
    # can be both scalars or vectors, but the must be of
    # the same shape: (n,1)
    new_periods, new_shifts, new_amplitudes = check_and_reshape_arguments(periods, shifts, amplitudes)
    # reshaping of time grid will be done automatically
    # after we add new_shifts to it.
    # the new shape will be (m,n)
    # where m is the height of time_grid.reshape(-1,1)
    # and n is the length of both new_periods and new_shifts
    phases = (time_grid.T + new_shifts)/new_periods*2*np.pi
    result = np.cos(phases)*new_amplitudes
    return np.sum(result, axis=0).reshape(-1,1)

def generate_dirty_periodical_series(time_grid, periods, shifts,amplitudes, sigma):
    # all args should be in the same units: e.g. secs
    """adds some random noise to the series"""
    noise = np.random.normal(loc=0.0, scale=sigma, size=time_grid.shape)
    result = noise + generate_periodical_series(time_grid, periods, shifts,amplitudes)
    return result

def check_and_reshape_arguments(periods, shifts,amplitudes):
    """reshapes arguments and check their shape"""
    shape_error = "both periods and shapes must be scalars or have the same shape"
    new_periods = reshape_one_value(periods)
    new_shifts = reshape_one_value(shifts)
    new_amplitudes = reshape_one_value(amplitudes)
    if (new_periods.shape != new_shifts.shape) or (new_periods.shape != new_amplitudes.shape):
        raise ValueError("periods shifts and amplitudes must be scalars or have the same shape")
    else:
        return new_periods, new_shifts, new_amplitudes

def reshape_one_value(value):
    """converting to vectors if needed and reshaping"""
    if np.isscalar:
        return np.array(value).reshape(-1,1)
    else:
        return value.reshape(-1,1)