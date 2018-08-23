from spec.spec_helper import *
import clean.threshold as thrs

with description(thrs.Threshold) as self:
    with before.all:
        self.time_grid_and_values = (
            np.load("./spec/fixtures/time_grid_1.pickle"),
            np.load("./spec/fixtures/series_1.pickle")
        )
        self.sigma = 2
        self.khi = 4
        self.number_of_random_series = 1000
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
    with shared_context('random series generator'):
        with before.each:
            self.random_series_array = self.estimator._Threshold__generate_random_series(
                self.number_of_random_series
            )
        with it('generates array with correct shape'):
            expected_shape = (self.time_grid_and_values[0].shape[0], self.number_of_random_series)
            expect(self.random_series_array.shape).to(
                equal(expected_shape)
            )
        with it('series are always different'):
            new_random_series_array = self.estimator._Threshold__generate_random_series(
                self.number_of_random_series
            )
            expect(
                np.all(
                    new_random_series_array == self.random_series_array
                )

            ).to(
                equal(False)
            )
        with it('has approx zero mean value'):
            random_series_array = np.load('./spec/fixtures/random_series_array_1.pickle')
            expect(np.around(np.mean(random_series_array), 2)).to(equal(0.00))
    with shared_context('probability generator'):
        with before.each:
            random_series_array = np.load('./spec/fixtures/random_series_array_1.pickle')
            self.time_grid = self.time_grid_and_values[0]
            self.generated_probability = self.estimator._Threshold__find_max_counts_and_relation(
                random_series_array, self.time_grid
            )
            self.expected_probability = 0.5529999999999999
        with it('finds correct value'):
            expect(self.generated_probability).to(equal(self.expected_probability))
        with it('generates differnt value with other random set'):
            random_series_array = self.estimator._Threshold__generate_random_series(
                self.number_of_random_series
            )
            new_generated_probability = self.estimator._Threshold__find_max_counts_and_relation(
                random_series_array, self.time_grid
            )
            expect(self.generated_probability).not_to(equal(new_generated_probability))
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

        with description('#__generate_random_series'):
            with included_context('random series generator'):
                pass

        with description('#__find_max_counts_and_relation'):
            with included_context('probability generator'):
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
        with description('#__generate_random_series'):
            with included_context('random series generator'):
                pass

        with description('#__find_max_counts_and_relation'):
            with included_context('probability generator'):
                pass