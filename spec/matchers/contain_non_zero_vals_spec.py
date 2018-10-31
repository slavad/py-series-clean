from spec.spec_helper import *

with description(contains_non_zero_vals) as self:
    with before.each:
        self.actual_result = contain_non_zero_vals._match(self.actual)
    with description('is not an ndarray'):
        with before.all:
            self.actual = 123
        with it('returns False'):
            expect(self.actual_result).to(equal((False, ['is not an ndarray'])))

    with description('zeroes only'):
        with before.all:
            self.actual = np.array([[0,0,0],[0,0,0]])
        with it('returns False'):
            expect(self.actual_result).to(equal((False, ['array contains zeroes'])))

    with description('non zeroes'):
        with before.all:
            self.actual = np.array([[0 + 0j,0 + 0j,0 + 0j],[0 + 0j,0 + 0j,0 + 1j]])
        with it('returns True'):
            expect(self.actual_result).to(equal((True, ['array does not contain zeroes'])))