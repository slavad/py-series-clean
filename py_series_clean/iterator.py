import numpy as np
import py_series_clean.schuster as sch
import py_series_clean.matrix_builder as mb
import pdb

def calc_normalized_detection_treshold(schuster_count, treshold):
    """eq 152 in ref 2"""
    result = schuster_count*treshold
    return result

def calculate_complex_amplitude(dirty_vector, window_vector, number_of_freq_estimations, max_count_index):
    """eq 154 ref 2"""
    max_count_value = dirty_vector[number_of_freq_estimations:][max_count_index][0]
    window_value = window_vector[2*number_of_freq_estimations:][2*max_count_index][0]
    nominator = max_count_value + np.conj(max_count_value)*window_value
    denominator = 1 - sch.squared_abs(window_value)
    return nominator/denominator

def extract_data_from_dirty_spec(dirty_vector, window_vector, super_resultion_vector, number_of_freq_estimations, max_count_index, harmonic_share, complex_amplitude):
    """eq 155 ref 2"""
    min_index = number_of_freq_estimations
    max_index = number_of_freq_estimations + 2*number_of_freq_estimations + 1
    window_vector_left_shift = window_vector[
        min_index - max_count_index:max_index - max_count_index
    ]
    window_vector_right_shift = window_vector[
        min_index + max_count_index:max_index + max_count_index
    ]
    difference = complex_amplitude*window_vector_left_shift + np.conj(complex_amplitude)*window_vector_right_shift
    result = dirty_vector - harmonic_share*difference
    return result

def add_data_to_super_resultion_vector(number_of_freq_estimations, super_resultion_vector,max_count_index, complex_amplitude, harmonic_share):
    """eq 156 ref 2"""
    vector_to_add = mb.build_super_resultion_vector(number_of_freq_estimations)
    vector_to_add[number_of_freq_estimations + max_count_index] = harmonic_share*complex_amplitude
    vector_to_add[number_of_freq_estimations - max_count_index] = harmonic_share*np.conj(complex_amplitude)
    result = vector_to_add + super_resultion_vector
    return result

def one_step(dirty_vector, window_vector, super_resultion_vector, number_of_freq_estimations, normalized_detection_treshold, harmonic_share):
    """one step of the iteration process"""
    dirty_subvector_wo_zero = dirty_vector[number_of_freq_estimations+1:]
    # we need to add 1 to the index, because our dirty_vector index has different indexing:
    # from -number_of_freq_estimations to number_of_freq_estimations
    max_count_index = sch.calc_schuster_counts(dirty_subvector_wo_zero, method_flag='argmax')[0] + 1
    max_count_value = dirty_subvector_wo_zero[max_count_index - 1][0]
    if sch.squared_abs(max_count_value) >= normalized_detection_treshold:
        # eq 154 ref 2
        complex_amplitude = calculate_complex_amplitude(dirty_vector, window_vector, number_of_freq_estimations, max_count_index)
        dirty_vector = extract_data_from_dirty_spec(
            dirty_vector, window_vector, super_resultion_vector,
            number_of_freq_estimations, max_count_index, harmonic_share,
            complex_amplitude
        )
        super_resultion_vector = add_data_to_super_resultion_vector(
            number_of_freq_estimations, super_resultion_vector,max_count_index,
            complex_amplitude, harmonic_share
        )
        return dirty_vector, super_resultion_vector
    else:
        return None


def iterate(dirty_vector, window_vector, treshold, max_iterations, harmonic_share, number_of_freq_estimations):
    """iterator: steps 7 to 17 pp 51-52 ref 2"""
    #TODO: check if vector shifts are ok here and above and below
    super_resultion_vector = mb.build_super_resultion_vector(number_of_freq_estimations)
    dirty_subvector = dirty_vector[number_of_freq_estimations:]
    schuster_counts = sch.calc_schuster_counts(dirty_subvector, method_flag='average')
    normalized_detection_treshold = calc_normalized_detection_treshold(
        schuster_counts[0], treshold
    )
    current_step = 0

    while current_step <= max_iterations:
        result = one_step(dirty_vector, window_vector,super_resultion_vector, number_of_freq_estimations, normalized_detection_treshold, harmonic_share)
        if not result:
            break
        else:
            dirty_vector, super_resultion_vector = result
            current_step += 1
    return super_resultion_vector, current_step