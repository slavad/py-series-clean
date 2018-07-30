import numpy as np

def calc_schuster_counts(series_array, method_flag):
    """
        calculates max or average value in the periodogram
        eq 153 in ref 2.
        The function chooses either the average or the max count
        depending on the flag.
    """
    schuster_periodogram = np.power(
        np.abs(series_array), 2
    )
    if method_flag == 'average': # let's estimate by average counts
        desired_value = np.average(schuster_periodogram, axis=0)
    elif method_flag == 'max': # by max counts
        desired_value = np.max(schuster_periodogram, axis=0)
    else:
        raise ValueError("unknown method_flag")
    return desired_value
