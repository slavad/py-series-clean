from expects.matchers import Matcher
from expects import have_keys
class have_only_keys(have_keys):

    def _match(self, subject):
        expected_keys = self._expected[0]
        has_key, reasons = super()._match(subject)
        if not has_key and 'is not a dict' in reasons:
            return has_key, reasons

        if len(expected_keys) != len(subject.keys()):
            has_key = False
            reasons.append('keys do not match')

        return has_key, reasons