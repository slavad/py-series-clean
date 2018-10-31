from expects.matchers import Matcher
import numpy as np
import pdb

class _contain_non_zero_vals(Matcher):
    def _match(self, actual_array):
        if np.max(np.abs(actual_array)) > 0.0:
            return True, ['array does not contain zeroes']
        else:
            return False, ['array contains zeroes']

contain_non_zero_vals = _contain_non_zero_vals()