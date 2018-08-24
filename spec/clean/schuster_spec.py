from spec.spec_helper import *
import clean.schuster as sch

with description(sch) as self:
    with before.all:
        self.array_to_test = np.array(
            [
                -0.1 - 10j,
                0.3 - 1j,
                8 - 10j
            ]
        ).reshape((-1,1))

    with description('#calc_schuster_counts'):

        with description('method_flag == "average"'):
            with it('resturns average squared abs'):
                expected_average = (np.power(0.1, 2) + np.power(10, 2) + \
                                   np.power(0.3, 2) + np.power(1, 2) + \
                                   np.power(8, 2) + np.power(10, 2))/3
                expect(
                    sch.calc_schuster_counts(self.array_to_test, 'average')
                ).to(equal(expected_average))

        with description('method_flag == "max"'):
            with it('resturns max squared abs'):
                expected_max = np.power(8, 2) + np.power(10, 2)
                expect(
                    sch.calc_schuster_counts(self.array_to_test, 'max')
                ).to(equal(expected_max))

        with description('method_flag == "argmax"'):
            with it('resturns max squared abs index'):
                expected_index = 2
                expect(
                    sch.calc_schuster_counts(self.array_to_test, 'argmax')
                ).to(equal(expected_index))

        with description('method_flag == "qwerty"'):
            with it('raises error'):
                expect(
                    lambda: sch.calc_schuster_counts(self.array_to_test, 'qwerty')
                ).to(raise_error(ValueError, "unknown method_flag"))

    with description('#squared_abs'):
        with it('returns correct values'):
            expected_result = np.array(
                [
                    np.power(0.1, 2) + np.power(10, 2),
                    np.power(0.3, 2) + np.power(1, 2),
                    np.power(8, 2) + np.power(10, 2)
                ]
            ).reshape((-1,1))
            expect(
                np.all(
                    #it's ok if we round it to the 2nd number after the decimal point
                    #since the expected_result precision is the same
                    np.around(sch.squared_abs(self.array_to_test), 2) == expected_result
                )
            ).to(equal(True))