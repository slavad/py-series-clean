from spec.spec_helper import *
import clean.wrapper as wrp

with description(wrp.Wrapper) as self:
    with before.all:
        self.use_aver = False
        self.round_precision = 10
        self.khi = 4
        self.detection_treshold = 0.3
        self.harmonic_share = 0.5
        self.max_iterations = 10
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
        with before.all:
            self.expected_keys = [
                'iterations', 'freq_vector', 'uniform_time_grid',
                'clean_spectrum', 'correlogram', 'uniform_series',
                'frequencies', 'amplitudes', 'phases'
            ]

            self.expected_keys_arr = [
                'freq_vector', 'uniform_time_grid',
                'clean_spectrum', 'correlogram', 'uniform_series',
                'frequencies', 'amplitudes', 'phases'
            ]


        with before.each:
            self.result = self.wrapper.clean(
                self.detection_treshold, self.max_iterations, self.harmonic_share, self.khi, self.use_aver
            )

        with description('use_aver is False'):
            with before.all:
                self.use_aver = False

                self.expected_iterations = 4
                self.uniform_time_grid = np.load("./spec/fixtures/uniform_time_grid_1.pickle")
                self.freq_vector = np.load("./spec/fixtures/freq_vector_1.pickle")
                self.clean_spectrum = np.load("./spec/fixtures/clean_spectrum_1.pickle")
                self.correlogram = np.load("./spec/fixtures/correlogram_1.pickle")
                self.uniform_series = np.load("./spec/fixtures/uniform_series_1.pickle")
                self.frequencies = np.load("./spec/fixtures/frequencies_1.pickle")
                self.amplitudes = np.load("./spec/fixtures/amplitudes_1.pickle")
                self.phases = np.load("./spec/fixtures/phases_1.pickle")

            with it('returns dict with correct keys'):
                expect(self.result).to(have_only_keys(*self.expected_keys))

            with it('returns correct number of iterations'):
                expect(self.result['iterations']).to(equal(self.expected_iterations))

            with it('returns correct ndarray values'):
                for key in self.expected_keys_arr:
                    expect(
                        self.result[key]
                    ).to(contain_non_zero_vals)
                    expect(
                        self.result[key]
                    ).to(equal_ndarray(getattr(self, key), self.round_precision))

        with description('use_aver is True'):
            pass
            #TBD