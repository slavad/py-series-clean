import numpy as np

def generate_periodical_seq(time_grid, period, shift):
    """generates periodical sequence"""
    # all args should be in the same units: e.g. secs
    # there is only one periodical component,
    # TODO: make multiple periodical components
    phases = (time_grid + shift)/period*2*np.pi;
    result =  np.cos(phases)
    return result

def generate_dirty_periodical_seq(time_grid, period, shift, sigma):
    # all args should be in the same units: e.g. secs
    """adds some random noies to the seq"""
    noise = np.random.normal(loc=0.0, scale=sigma, size=time_grid.shape)
    result = noise + generate_periodical_seq(time_grid, period, shift)
    return result