from spec.spec_helper import *
import clean.threshold as thrs

with description(thrs.Threshold) as self:
    with before.all:
        self.time_grid_and_values = (
            np.load("./spec/fixtures/time_grid_1.pickle"),
            np.load("./spec/fixtures/series_1.pickle")
        )
        self.sigma = 2.5
        self.khi = 4
        self.number_of_random_series = 1000
        self.time_grid = self.time_grid_and_values[0]
        self.values = self.time_grid_and_values[1]
        self.max_attemtps = 10
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
            self.generated_probability = self.estimator._Threshold__find_max_counts_and_relation(
                random_series_array, self.values
            )
            self.expected_probability = 0.63
        with it('finds correct value'):
            expect(self.generated_probability).to(equal(self.expected_probability))

        with it('generates differnt value with other random set'):
            for i in range(self.max_attemtps):
                # sometimes result is not different, let's try one more time
                random_series_array = self.estimator._Threshold__generate_random_series(
                    self.number_of_random_series
                )
                new_generated_probability = self.estimator._Threshold__find_max_counts_and_relation(
                    random_series_array, self.values
                )
                result = self.generated_probability == new_generated_probability
                if result == False:
                    break
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

        with description('#estimate'):
            with before.all:
                self.expected_probability_min = 0.5
                self.expected_probability_max = 0.7
            with before.each:
                self.generated_probability = self.estimator.estimate(
                    self.number_of_random_series
                )
            with it('fits to the range'):
                expect(self.generated_probability).to(be_below_or_equal(self.expected_probability_max))
                expect(self.generated_probability).to(be_above_or_equal(self.expected_probability_min))

            with it('is always different'):
                for i in range(self.max_attemtps):
                    # sometimes result is not different, let's try one more time
                    new_generated_probability = self.estimator.estimate(
                        self.number_of_random_series
                    )
                    result = self.generated_probability == new_generated_probability
                    if result == False:
                        break
                expect(result).to(equal(False))

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