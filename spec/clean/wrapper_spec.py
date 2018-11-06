from spec.spec_helper import *
import clean.wrapper as wrp

with description(wrp.Wrapper) as self:
    with before.all:
        self.use_aver = False
        self.time_grid = np.load("./spec/fixtures/time_grid_1.pickle")
        self.values = np.load("./spec/fixtures/series_1.pickle")
        self.distance_vector = np.load("./spec/fixtures/distance_vector_1.pickle")
    with before.each:
        self.wrapper = wrp.Wrapper(self.time_grid, self.values)

    with description('__init__'):
        with it('sets correct values'):
            expect(self.wrapper._Wrapper__time_grid).to(equal_ndarray(self.time_grid))
            expect(self.wrapper._Wrapper__values).to(equal_ndarray(self.values))
            expect(self.wrapper._Wrapper__distance_vector).to(equal_ndarray(self.distance_vector))

    with shared_context('#__estimate_max_freq checker'):
        with description('#__estimate_max_freq'):
            with before.all:
                self.time_grid = np.array(
                    [0.0, 5.0, 6.0, 9.0, 20.0]
                ).reshape((-1, 1))
            with it('returns max freq estimated by minimum time distance'):
                expect(self.wrapper._Wrapper__estimate_max_freq(self.use_aver)).to(
                    equal(self.expected_max_freq)
                )
    with description('use_aver is False'):
        with before.all:
            self.use_aver = False
            self.expected_max_freq = 0.5
        with included_context('#__estimate_max_freq checker'):
            pass

    with description('use_aver is True'):
        with before.all:
            self.use_aver = True
            self.expected_max_freq = 0.1
        with included_context('#__estimate_max_freq checker'):
            pass

    with description('#__calculate_estimations_vector_size'):
        with before.all:
            self.use_aver = False
            self.time_grid = np.array([0.0, 3.5]).reshape((-1, 1))
        with it('calculates correct value'):
            max_freq = 0.8
            khi = 4
            expected_num_of_freq_estimations = 12
            expect(self.wrapper._Wrapper__calculate_estimations_vector_size(max_freq, khi)).to(
                equal(expected_num_of_freq_estimations)
            )

    with description('clean'):
        with description('use_aver is False'):
            with before.all:
                self.use_aver = False

        with description('use_aver is True'):
            with before.all:
                self.use_aver = True