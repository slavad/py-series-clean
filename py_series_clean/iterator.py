import numpy as np
import py_series_clean.schuster as sch
import py_series_clean.matrix_builder as mb
import pdb

def calc_normalized_detection_treshold(schuster_count, treshold):
    """eq 152 in ref 2"""
    result = schuster_count*treshold
    return result

def extract_data_from_dirty_spec(cloned_dirty_vector, weights_vector, super_resultion_vector, number_of_freq_estimations):
    """extracts data from dirty spectrum, step 10-13 in ref 2"""
    pass

def one_step(cloned_dirty_vector, weights_vector, super_resultion_vector, number_of_freq_estimations, normalized_detection_treshold):
    """one step of the iteration process"""
    dirty_subvector_wo_zero = cloned_dirty_vector[number_of_freq_estimations+1:]
    max_count_index = sch.calc_schuster_counts(dirty_subvector_wo_zero, method_flag='argmax')[0]
    max_count_value = dirty_subvector_wo_zero[max_count_index][0]
    pdb.set_trace()
    if sch.periodogram(max_count_value) >= normalized_detection_treshold:
        extract_data_from_dirty_spec(cloned_dirty_vector, weights_vector, super_resultion_vector, number_of_freq_estimations)
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
        if not one_step(cloned_dirty_vector, weights_vector,super_resultion_vector, number_of_freq_estimations, normalized_detection_treshold):
            break
    return super_resultion_vector