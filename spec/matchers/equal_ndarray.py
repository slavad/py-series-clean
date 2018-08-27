from expects.matchers import Matcher
import numpy as np

class equal_ndarray(Matcher):
    def __init__(self, original_expected_array, precision = False):
        self._precision = precision
        self._original_expected_array = original_expected_array
        if type(original_expected_array).__name__ == 'ndarray':
            if self._precision:
                self._rounded_expected_array = np.around(original_expected_array, self._precision)
                self._message_success = ["arrays are equal with precision {}".format(precision)]
                self._message_failure = ["arrays are not equal with precision {}".format(precision)]
            else:
                self._rounded_expected_array = original_expected_array
                self._message_success = ["arrays are equal"]
                self._message_failure = ["arrays are not equal"]

    def _match(self, original_actual_array):
        if type(self._original_expected_array).__name__ != 'ndarray':
            return False, ['expected was not an ndarray']

        if type(original_actual_array).__name__ != 'ndarray':
            return False, ['actual was not an ndarray']

        if self._precision:
            rounded_actual_array = np.around(original_actual_array, self._precision)
        else:
            rounded_actual_array = original_actual_array

        if self._same_shape(rounded_actual_array) and self._all_equal(rounded_actual_array):
            return True, self._message_success
        else:
            return False, self._message_failure

    def _same_shape(self, rounded_actual_array):
        """check if both expected and actual have the same shape"""
        return rounded_actual_array.shape == self._rounded_expected_array.shape

    def _all_equal(self, rounded_actual_array):
        """checks if arrays are all equal"""
        return np.all(rounded_actual_array == self._rounded_expected_array)


    def __repr__(self):
        """Returns a string with the description of the matcher."""
        if self._precision:
            descr = "equal with precision {precision}".format(precision = self._precision)
        else:
            descr = "equal"
        return descr

    def _failure_message_general(self, subject, reasons, negated):
        """custom failure message"""

        if negated:
            to_or_not_to = 'not to'
        else:
            to_or_not_to = 'to'
        message = '\nexpected:\n{subject!r}\n{to_or_not_to} {matcher} to\n{original_expected_array!r}'.format(
            subject=subject, matcher = self, to_or_not_to = to_or_not_to, original_expected_array=self._original_expected_array)

        if reasons:
            message += '\n     but: {0}'.format('\n          '.join(reasons))

        return message

    def _failure_message(self, subject, reasons):
        """custom failure message"""
        return self._failure_message_general(subject, reasons, False)

    def _failure_message_negated(self, subject, reasons):
        """custom failure message"""
        return self._failure_message_general(subject, reasons, True)