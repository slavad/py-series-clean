from expects.matchers import Matcher
import numbers

class equal_with_precision(Matcher):
    def __init__(self, original_expected_number, precision):
        self._precision = precision
        self._original_expected_number = original_expected_number
        if isinstance(original_expected_number, numbers.Number):
            self._rounded_expected_number = round(original_expected_number, self._precision)
            self._message_success = ["numbers are equal with precision {}".format(precision)]
            self._message_failure = ["numbers are not equal with precision {}".format(precision)]

    def _match(self, original_actual_number):
        if not isinstance(self._original_expected_number, numbers.Number):
            return False, ['expected was not a number']

        if  not isinstance(original_actual_number, numbers.Number):
            return False, ['actual was not a number']

        rounded_actual_number = round(original_actual_number, self._precision)

        if self._original_expected_number == rounded_actual_number:
            return True, self._message_success
        else:
            return False, self._message_failure

    def __repr__(self):
        """Returns a string with the description of the matcher."""
        descr = "equal with precision {precision}".format(precision = self._precision)
        return descr

    def _failure_message_general(self, subject, reasons, negated):
        """custom failure message"""
        if negated:
            to_or_not_to = 'not to'
        else:
            to_or_not_to = 'to'
        message = '\nexpected: {subject} {to_or_not_to} {matcher} to {original_expected_number}'.format(
            subject=subject, matcher = self, to_or_not_to = to_or_not_to, original_expected_number=self._original_expected_number)

        if reasons:
            message += '\n     but: {0}'.format('\n          '.join(reasons))

        return message

    def _failure_message(self, subject, reasons):
        """custom failure message"""
        return self._failure_message_general(subject, reasons, False)

    def _failure_message_negated(self, subject, reasons):
        """custom failure message"""
        return self._failure_message_general(subject, reasons, True)