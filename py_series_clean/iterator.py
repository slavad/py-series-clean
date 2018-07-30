import numpy as np

def calc_normalized_detection_treshold(schuster_count, treshold):
    """eq 152 in ref 2"""
    result = schuster_count*treshold
    return result