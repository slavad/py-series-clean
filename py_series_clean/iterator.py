import numpy as np
import py_series_clean.schuster as sch
import py_series_clean.matrix_builder as mb
import pdb

def calc_normalized_detection_treshold(schuster_count, treshold):
    """eq 152 in ref 2"""
    result = schuster_count*treshold
    return result

def calculate_complex_amplitude(cloned_dirty_vector, weights_vector, number_of_freq_estimations, max_count_index):
    """eq 154 ref 2"""
    max_count_value = cloned_dirty_vector[number_of_freq_estimations:][max_count_index][0]
    window_value = weights_vector[2*number_of_freq_estimations:][2*max_count_index][0]
    nominator = max_count_value + np.conj(max_count_value)*window_value
    denominator = 1 - sch.squared_abs(window_value)
    return nominator/denominator

def extract_data_from_dirty_spec(cloned_dirty_vector, weights_vector, super_resultion_vector, number_of_freq_estimations, max_count_index, harmonic_share):
    """extracts data from dirty spectrum, step 10-13 in ref 2"""
    complex_amplitude = calculate_complex_amplitude(cloned_dirty_vector, weights_vector, number_of_freq_estimations, max_count_index)

def one_step(cloned_dirty_vector, weights_vector, super_resultion_vector, number_of_freq_estimations, normalized_detection_treshold, harmonic_share):
    """one step of the iteration process"""
    dirty_subvector_wo_zero = cloned_dirty_vector[number_of_freq_estimations+1:]
    # we need to add 1 to the index, because our cloned_dirty_vector index has different indexing:
    # from -number_of_freq_estimations to number_of_freq_estimations
    max_count_index = sch.calc_schuster_counts(dirty_subvector_wo_zero, method_flag='argmax')[0] + 1
    max_count_value = dirty_subvector_wo_zero[max_count_index - 1][0]
    if sch.squared_abs(max_count_value) >= normalized_detection_treshold:
        extract_data_from_dirty_spec(cloned_dirty_vector, weights_vector, super_resultion_vector, number_of_freq_estimations, max_count_index, harmonic_share)
        return True
    else:
        return False


def iterate(dirty_vector, weights_vector, treshold, max_iterations, harmonic_share, number_of_freq_estimations):
    """iterator: steps 7 to 17 pp 51-52 ref 2"""
    super_resultion_vector = mb.build_super_resultion_vector(number_of_freq_estimations)
    dirty_subvector = dirty_vector[number_of_freq_estimations:]
    schuster_counts = sch.calc_schuster_counts(dirty_subvector, method_flag='average')
    normalized_detection_treshold = calc_normalized_detection_treshold(
        schuster_counts[0], treshold
    )
    current_step = 1

    # dirty_vector will be altered during the process
    # let's clone it then
    cloned_dirty_vector = np.copy(dirty_vector)
    while current_step <= max_iterations:
        if not one_step(cloned_dirty_vector, weights_vector,super_resultion_vector, number_of_freq_estimations, normalized_detection_treshold, harmonic_share):
            break
        current_step += 1
    return super_resultion_vector