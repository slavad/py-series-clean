from expects.matchers import Matcher
import numpy as np
import pdb

class contain_non_zero_vals(Matcher):
    def __init__(self, precision = None):
        self.precision = precision

    def _match(self, actual_array):
        if not isinstance(actual_array, np.ndarray):
            raise ValueError('actual is not an ndarray')
        if self.precision:
            array_to_compare = np.round(actual_array, self.precision)
        else:
            array_to_compare = actual_array
        if np.max(np.abs(array_to_compare)) > 0.0:
            return True, ['array does not contain zeroes']
        else:
            return False, ['array contains zeroes']
