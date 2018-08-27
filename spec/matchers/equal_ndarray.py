from expects.matchers import Matcher
import numpy as np

class equal_ndarray(Matcher):
    def __init__(self, expected_array, precision = False):
        self._precision = precision
        if self._precision:
            self._expected_array = np.around(expected_array, self._precision)
            self._message_success = ["arrays are equal with precision {}".format(precision)]
            self._message_failure = ["arrays are not equal with precision {}".format(precision)]
        else:
            self._expected_array = expected_array
            self._message_success = ["arrays are equal"]
            self._message_failure = ["arrays are not equal"]

    def _match(self, actual_array):
        if self._precision:
            actual_array_rounded = np.around(actual_array, self._precision)
        else:
            actual_array_rounded = actual_array
        if np.all(actual_array_rounded == self._expected_array):
            return True, self._message_success
        else:
            return False, self._message_failure
