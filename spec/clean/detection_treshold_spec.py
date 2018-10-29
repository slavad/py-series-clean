from spec.spec_helper import *
import clean.detection_treshold as dtr

with description(dtr.DetectionTreshold) as self:
    with before.all:
        self.sigma = 2.5
        self.khi = 4
        self.number_of_random_series = 1000
        self.time_grid = np.load("./spec/fixtures/time_grid_1.pickle")
        self.false_alarm_probability = 0.80
        self.max_attemtps = 10
    with before.each:
        self.estimator = dtr.DetectionTreshold(self.time_grid, self.sigma)
    with description('#__init__'):
        with it('sets all values'):
            expect(
                self.time_grid
            ).to(
                equal_ndarray(self.estimator._DetectionTreshold__time_grid)
            )
            expect(
                self.sigma
            ).to(
                equal(self.estimator._DetectionTreshold__sigma)
            )

    with description('#estimate'):
        with before.all:
            self.expected_detection_treshold_min = 55.0
            self.expected_detection_treshold_max = 65.0
        with before.each:
            self.generated_detection_treshold = self.estimator.estimate(
                self.number_of_random_series, self.false_alarm_probability
            )
        with it('fits to the range'):
            expect(self.generated_detection_treshold).to(be_below_or_equal(self.expected_detection_treshold_max))
            expect(self.generated_detection_treshold).to(be_above_or_equal(self.expected_detection_treshold_min))

        with it('is always different'):
            for i in range(self.max_attemtps):
                # sometimes result is not different, let's try one more time
                new_generated_detection_treshold = self.estimator.estimate(
                    self.number_of_random_series, self.false_alarm_probability
                )
                result = self.generated_detection_treshold == new_generated_detection_treshold
                if result == False:
                    break
            expect(result).to(equal(False))

    with description('#__generate_random_series'):
        with before.each:
            self.random_series_array = self.estimator._DetectionTreshold__generate_random_series(
                self.number_of_random_series
            )
        with it('generates array with correct shape'):
            expected_shape = (self.time_grid.shape[0], self.number_of_random_series)
            expect(self.random_series_array.shape).to(
                equal(expected_shape)
            )
        with it('series are always different'):
            new_random_series_array = self.estimator._DetectionTreshold__generate_random_series(
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

    with description('#__find_detection_treshold'):
        with before.each:
            random_series_array = np.load('./spec/fixtures/random_series_array_1.pickle')
            self.generated_detection_treshold = self.estimator._DetectionTreshold__find_detection_treshold(
                random_series_array, self.false_alarm_probability
            )
            self.expected_detection_treshold = 58.46936430041756
        with it('finds correct value'):
            expect(self.generated_detection_treshold).to(equal(self.expected_detection_treshold))

        with it('generates differnt value with other random set'):
            for i in range(self.max_attemtps):
                # sometimes result is not different, let's try one more time
                random_series_array = self.estimator._DetectionTreshold__generate_random_series(
                    self.number_of_random_series
                )
                new_generated_detection_treshold = self.estimator._DetectionTreshold__find_detection_treshold(
                    random_series_array, self.false_alarm_probability
                )
                result = self.generated_detection_treshold == new_generated_detection_treshold
                if result == False:
                    break
            expect(self.generated_detection_treshold).not_to(equal(new_generated_detection_treshold))
