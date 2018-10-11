from spec.spec_helper import *
import clean.false_alarm_probability as fap

with description(fap.FalseAlarmProbability) as self:
    with before.all:
        self.sigma = 2.5
        self.khi = 4
        self.number_of_random_series = 1000
        self.time_grid = np.load("./spec/fixtures/time_grid_1.pickle")
        self.false_alarm_probability = 0.80
        self.max_attemtps = 10
    with before.each:
        self.estimator = fap.FalseAlarmProbability(self.time_grid, self.sigma, self.khi, self.use_aver)
    with shared_context('object values setter'):
        with it('sets all values'):
            expect(
                self.time_grid

            ).to(
                equal_ndarray(self.estimator._FalseAlarmProbability__time_grid)
            )
            expect(
                self.sigma
            ).to(
                equal(self.estimator._FalseAlarmProbability__sigma)
            )
    with shared_context('random series generator'):
        with before.each:
            self.random_series_array = self.estimator._FalseAlarmProbability__generate_random_series(
                self.number_of_random_series
            )
        with it('generates array with correct shape'):
            expected_shape = (self.time_grid.shape[0], self.number_of_random_series)
            expect(self.random_series_array.shape).to(
                equal(expected_shape)
            )
        with it('series are always different'):
            new_random_series_array = self.estimator._FalseAlarmProbability__generate_random_series(
                self.number_of_random_series
            )
            expect(
                new_random_series_array
            ).not_to(
                equal_ndarray(self.random_series_array)
            )
        with it('has approx zero mean value'):
            random_series_array = np.load('./spec/fixtures/random_series_array_1.pickle')
            equal_with_precision
            expect(np.mean(random_series_array)).to(equal_with_precision(0.00, precision = 2))
    with shared_context('normalized_detection_treshold generator'):
        with before.each:
            random_series_array = np.load('./spec/fixtures/random_series_array_1.pickle')
            self.generated_normalized_detection_treshold = self.estimator._FalseAlarmProbability__find_normalized_detection_treshold(
                random_series_array, self.false_alarm_probability
            )
            self.expected_normalized_detection_treshold = 58.46936430041756
        with it('finds correct value'):
            expect(self.generated_normalized_detection_treshold).to(equal(self.expected_normalized_detection_treshold))

        with it('generates differnt value with other random set'):
            for i in range(self.max_attemtps):
                # sometimes result is not different, let's try one more time
                random_series_array = self.estimator._FalseAlarmProbability__generate_random_series(
                    self.number_of_random_series
                )
                new_generated_normalized_detection_treshold = self.estimator._FalseAlarmProbability__find_normalized_detection_treshold(
                    random_series_array, self.false_alarm_probability
                )
                result = self.generated_normalized_detection_treshold == new_generated_normalized_detection_treshold
                if result == False:
                    break
            expect(self.generated_normalized_detection_treshold).not_to(equal(new_generated_normalized_detection_treshold))
    with description('use_aver is False'):
        with before.all:
            self.use_aver = False
        with description('#__init__'):
            with it('sets number_of_freq_estimations'):
                expected_num_of_freq_estimations = 35934
                expect(
                    expected_num_of_freq_estimations
                ).to(
                    equal(self.estimator._FalseAlarmProbability__number_of_freq_estimations)
                )
            with included_context('object values setter'):
                pass

        with description('#estimate'):
            with before.all:
                self.expected_normalized_detection_treshold_min = 55.0
                self.expected_normalized_detection_treshold_max = 60.0
            with before.each:
                self.generated_normalized_detection_treshold = self.estimator.estimate(
                    self.number_of_random_series, self.false_alarm_probability
                )
            with it('fits to the range'):
                expect(self.generated_normalized_detection_treshold).to(be_below_or_equal(self.expected_normalized_detection_treshold_max))
                expect(self.generated_normalized_detection_treshold).to(be_above_or_equal(self.expected_normalized_detection_treshold_min))

            with it('is always different'):
                for i in range(self.max_attemtps):
                    # sometimes result is not different, let's try one more time
                    new_generated_normalized_detection_treshold = self.estimator.estimate(
                        self.number_of_random_series, self.false_alarm_probability
                    )
                    result = self.generated_normalized_detection_treshold == new_generated_normalized_detection_treshold
                    if result == False:
                        break
                expect(result).to(equal(False))

        with description('#__generate_random_series'):
            with included_context('random series generator'):
                pass

        with description('#__find_normalized_detection_treshold'):
            with included_context('normalized_detection_treshold generator'):
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
                    equal(self.estimator._FalseAlarmProbability__number_of_freq_estimations)
                )
            with included_context('object values setter'):
                pass
        with description('#__generate_random_series'):
            with included_context('random series generator'):
                pass

        with description('#__find_normalized_detection_treshold'):
            with included_context('normalized_detection_treshold generator'):
                pass