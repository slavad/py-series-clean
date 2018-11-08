from spec.spec_helper import *

with description(contains_non_zero_vals) as self:
    with shared_context('zero array mamcher checker'):
        with description('is not an ndarray'):
            with before.all:
                self.actual = 123
            with before.each:
                self.action = lambda: contain_non_zero_vals(self.precision)._match(self.actual)
            with it('raises error'):
                expect(self.action).to(
                    raise_error(ValueError, 'actual is not an ndarray')
                )
        with description('valid input'):
            with before.each:
                self.actual_result = contain_non_zero_vals(self.precision)._match(self.actual)
            with description('zeroes only'):
                with before.all:
                    self.actual = self.all_zeroes_array
                with it('returns False'):
                    expect(self.actual_result).to(equal((False, ['array contains zeroes'])))

            with description('non zeroes'):
                with before.all:
                    self.actual = self.non_zero_array
                with it('returns True'):
                    expect(self.actual_result).to(equal((True, ['array does not contain zeroes'])))

    with description('no precision'):
        with before.all:
            self.precision = None # default value
            self.all_zeroes_array = np.array([[0,0,0],[0,0,0]])
            self.non_zero_array = np.array([[0 + 0j,0 + 0j,0 + 0j],[0 + 0j,0 + 0j,0 + 1j]])
        with included_context('zero array mamcher checker'):
            pass

    with description('precision'):
        with before.all:
            self.precision = 2 # two digits after the decimal sign
            self.all_zeroes_array = np.array([[0.0,0.0,0.001],[0.0,0.0,0.0]])
            self.non_zero_array = np.array([[0.0 + 0.0j,0 + 0.0j,0.0 + 0.0j],[0.0 + 0.0j,0.0 + 0.0j,0.0 + 0.01j]])
        with included_context('zero array mamcher checker'):
            pass