import numpy as np
import py_series_clean.matrix_builder as mb
import py_series_clean.schuster as sch
import pdb

def restore(super_resultion_vector, iterations, number_of_freq_estimations, time_grid, max_freq):
    """restores clean spectrum, algorithm steps 18 to 21 ref 2"""
    # if nothing was detected:
    if iterations == 0:
        return None
    else:
        uniform_time_grid = build_uniform_time_grid(time_grid)
        index_vector = mb.generate_index_vector(
            mb.size_of_spectrum_vector(number_of_freq_estimations)
        )
        freq_vector = index_vector*max_freq/number_of_freq_estimations
        clean_window_vector = build_clean_window_vector(
            number_of_freq_estimations, uniform_time_grid, max_freq
        )
        freqs, amplitudes, phases = restore_amplitude_and_phase(super_resultion_vector, freq_vector)
        clean_spectrum = build_clean_spectrum(
            clean_window_vector, super_resultion_vector, number_of_freq_estimations
        )
        correlogram = build_correlogram(
            clean_spectrum, freq_vector, uniform_time_grid, number_of_freq_estimations
        )
        uniform_series = build_uniform_series(
            clean_spectrum, freq_vector, uniform_time_grid, number_of_freq_estimations
        )
        return uniform_time_grid, clean_spectrum, correlogram, uniform_series, freq_vector, freqs, amplitudes, phases

def restore_amplitude_and_phase(super_resultion_vector, freq_vector):
    """req 143 and 144 ref 2"""
    non_zeroes = np.extract(np.abs(super_resultion_vector) != 0,super_resultion_vector)
    freqs = np.extract(np.abs(super_resultion_vector) != 0,freq_vector)
    amplitudes = 2*np.abs(non_zeroes)
    phases = np.arctan2(np.imag(non_zeroes),np.real(non_zeroes))
    return freqs.reshape(-1,1), amplitudes.reshape(-1,1), phases.reshape(-1,1)

def build_uniform_time_grid(time_grid):
    """eq 158 ref 2"""
    step_size = (time_grid[-1][0] - time_grid[0][0])/(time_grid.shape[0] - 1)
    start = 0
    stop = step_size*time_grid.shape[0]
    result = np.arange(start,stop,step_size).reshape(-1,1)
    return result

def build_clean_spectrum(clean_window_vector, super_resultion_vector, number_of_freq_estimations):
    """eq 159 ref 2"""
    number_of_rows = super_resultion_vector.shape[0]
    array = []
    for index in range(0, number_of_rows):
        #TODO: check correctness of the index shifts:
        # probably shifts here are wrong.
        # maybe reverse the array here?
        # in eq 159 B[j-k]
        # here j == index,
        # but in our formula [k-j]!
        # probably the subvector should also be flipped
        max_index = index + 2*number_of_freq_estimations
        min_index = max_index - 2*number_of_freq_estimations
        subvector = clean_window_vector[min_index:max_index+1]
        array.append(np.matmul(super_resultion_vector.T, np.flip(subvector, axis=0))[0][0])
    result = np.array(array).reshape(-1,1)
    return result

def build_clean_window_vector(number_of_freq_estimations, uniform_time_grid, max_freq):
    """eq 157 ref 2"""
    clean_window_vector = mb.calculate_window_vector(
        uniform_time_grid, number_of_freq_estimations, max_freq
    )
    return clean_window_vector

def build_correlogram(clean_spectrum, freq_vector, uniform_time_grid,number_of_freq_estimations):
    """eq 160 ref 2"""
    values = sch.squared_abs(clean_spectrum)
    result = build_correlogram_or_uniform_series(
        values, freq_vector, uniform_time_grid,number_of_freq_estimations
    )
    return result

def build_uniform_series(clean_spectrum, freq_vector, uniform_time_grid, number_of_freq_estimations):
    """eq 161 ref 2"""
    result = build_correlogram_or_uniform_series(
        clean_spectrum, freq_vector, uniform_time_grid,number_of_freq_estimations
    )
    return result

def build_correlogram_or_uniform_series(values, freq_vector, uniform_time_grid,number_of_freq_estimations):
    """eq 160 and 161 ref 2"""
    result = mb.build_exp_matrix(
        uniform_time_grid, values, freq_vector,number_of_freq_estimations, 'inverse'
    )
    return result