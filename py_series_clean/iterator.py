import numpy as np
import py_series_clean.schuster as sch
import pdb

def calc_normalized_detection_treshold(schuster_count, treshold):
    """eq 152 in ref 2"""
    result = schuster_count*treshold
    return result

def iterate(dirty_vector, weights_vector, super_resultion_vector, treshold, max_iterations, harmonic_share, number_of_freq_estimations):
    """iterator: steps 7 to 17 pp 51-52 ref 2"""
    dirty_subvector = dirty_vector[number_of_freq_estimations:]
    dirty_subvector_wo_zero = dirty_vector[number_of_freq_estimations+1:]
    schuster_counts = sch.calc_schuster_counts(dirty_subvector, method_flag='average')
    normalized_detection_treshold = calc_normalized_detection_treshold(
        schuster_counts[0], treshold
    )
    current_step = 1
    while current_step <= max_iterations:
        pass