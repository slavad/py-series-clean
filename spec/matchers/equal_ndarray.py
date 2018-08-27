from expects.matchers import Matcher
import numpy as np

class equal_ndarray(Matcher):
    def __init__(self, expected_array, precision = False):
        self._precision = precision
        self._original_expected_array = expected_array
        if type(expected_array).__name__ == 'ndarray':
            if self._precision:
                self._expected_array = np.around(expected_array, self._precision)
                self._message_success = ["arrays are equal with precision {}".format(precision)]
                self._message_failure = ["arrays are not equal with precision {}".format(precision)]
            else:
                self._expected_array = expected_array
                self._message_success = ["arrays are equal"]
                self._message_failure = ["arrays are not equal"]

    def _match(self, actual_array):
        if type(self._original_expected_array).__name__ != 'ndarray':
            return False, ['expected was not an ndarray']

        if type(actual_array).__name__ != 'ndarray':
            return False, ['actual was not an ndarray']

        if self._precision:
            actual_array_rounded = np.around(actual_array, self._precision)
        else:
            actual_array_rounded = actual_array

        if self._same_shape(actual_array_rounded) and self._all_equal(actual_array_rounded):
            return True, self._message_success
        else:
            return False, self._message_failure

    def _same_shape(self, actual_array_rounded):
        """check if both expected and actual have the same shape"""
        return actual_array_rounded.shape == self._expected_array.shape

    def _all_equal(self, actual_array_rounded):
        """checks if arrays are all equal"""
        return np.all(actual_array_rounded == self._expected_array)

    def _failure_message_general(self, subject, reasons, negated):
        """custom failure message"""
        if self._precision:
            what = "equal with precision {precision!r}".format(precision = self._precision)
        else:
            what = "equal"
        if negated:
            to_or_not_to = 'not to'
        else:
            to_or_not_to = 'to'
        message = '\nexpected: {subject!r} {to_or_not_to} {what} to {expected_array!r}'.format(
            subject=subject, what = what, to_or_not_to = to_or_not_to, expected_array=self._original_expected_array)

        if reasons:
            message += '\n     but: {0}'.format('\n          '.join(reasons))

        return message

    def _failure_message(self, subject, reasons):
        """custom failure message"""
        return self._failure_message_general(subject, reasons, False)

    def _failure_message_negated(self, subject, reasons):
        """custom failure message"""
        return self._failure_message_general(subject, reasons, True)