from spec.spec_helper import *
import clean.threshold as thrs

with description(thrs.Threshold) as self:
    with before.all:
        self.time_grid_and_values = (
            np.load("./spec/fixtures/time_grid_1.pickle"),
            np.load("./spec/fixtures/series_1.pickle")
        )
        self.sigma = 1
        self.khi = 4
    with before.each:
        self.estimator = thrs.Threshold(self.time_grid_and_values, self.sigma, self.khi, self.use_aver)
    with shared_context('object values setter'):
        with it('sets all values'):
            expect(
                np.all(
                    self.time_grid_and_values[0] == self.estimator._Threshold__time_grid
                )

            ).to(
                equal(True)
            )
            expect(
                np.all(
                    self.time_grid_and_values[1] == self.estimator._Threshold__values
                )

            ).to(
                equal(True)
            )
            expect(
                self.sigma
            ).to(
                equal(self.estimator._Threshold__sigma)
            )
    with description('use_aver is False'):
        with before.all:
            self.use_aver = False
        with description('#__init__'):
            with it('sets number_of_freq_estimations'):
                expected_num_of_freq_estimations = 35934
                expect(
                    expected_num_of_freq_estimations
                ).to(
                    equal(self.estimator._Threshold__number_of_freq_estimations)
                )
            with included_context('object values setter'):
                pass
    with description('use aver is True'):
        with before.all:
            self.use_aver = True
        with description('#__init__'):
            with it('sets number_of_freq_estimations'):
                expected_num_of_freq_estimations = 198
                expect(
                    expected_num_of_freq_estimations
                ).to(
                    equal(self.estimator._Threshold__number_of_freq_estimations)
                )
            with included_context('object values setter'):
                pass