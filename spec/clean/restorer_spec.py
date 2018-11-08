from spec.spec_helper import *
import clean.restorer as rst
import clean.matrix_builder as mb
import clean.schuster as sch

with description(rst.Restorer) as self:
    with before.all:
        self.round_precision = 10
        self.super_resultion_vector = np.load('./spec/fixtures/super_resultion_vector_with_result_1.pickle')
        self.max_freq = 928.6049396317791 # precalculated value
        self.number_of_freq_estimations = 35934 # precalculated value
        self.time_grid = np.load("./spec/fixtures/time_grid_1.pickle")
        self.uniform_time_grid = np.load("./spec/fixtures/uniform_time_grid_1.pickle")
        self.index_vector = np.load("./spec/fixtures/index_vector_1.pickle")
        self.freq_vector = np.load("./spec/fixtures/freq_vector_1.pickle")
        self.clean_window_vector = np.load("./spec/fixtures/clean_window_vector_1.pickle")
        self.clean_spectrum = np.load("./spec/fixtures/clean_spectrum_1.pickle")
        self.correlogram = np.load("./spec/fixtures/correlogram_1.pickle")
        self.uniform_series = np.load("./spec/fixtures/uniform_series_1.pickle")
        self.frequencies = np.load("./spec/fixtures/frequencies_1.pickle")
        self.amplitudes = np.load("./spec/fixtures/amplitudes_1.pickle")
        self.phases = np.load("./spec/fixtures/phases_1.pickle")

    with before.each:
        self.restorer = rst.Restorer(
            self.iterations, self.super_resultion_vector, self.number_of_freq_estimations, self.time_grid, self.max_freq
        )

    with shared_context('common attrs values checker'):
        with it('sets only iterations value'):
            expect(
                self.iterations
            ).to(
                equal(self.restorer._Restorer__iterations)
            )
            expect(self.restorer.__dict__).to(
                have_only_keys(*self.expected_restorer_vars)
            )
    with description('number of iterations in zero'):
        with before.all:
            self.iterations = 0
            self.expected_restorer_vars = ['_Restorer__iterations']

        with description('__init__'):
            with included_context('common attrs values checker'):
                pass
        with description('restore'):
            with it('resturns None'):
                expect(self.restorer.restore()).to(be_none)

    with description('number of iterations is not zero'):
        with before.all:
            self.iterations = 4
            self.expected_restorer_vars = [
                 '_Restorer__iterations', '_Restorer__super_resultion_vector',
                 '_Restorer__number_of_freq_estimations', '_Restorer__max_freq',
                 '_Restorer__uniform_time_grid', '_Restorer__index_vector',
                 '_Restorer__freq_vector', '_Restorer__clean_window_vector'
            ]
        with description('__init__'):
            with included_context('common attrs values checker'):
                pass
            with it('sets other attrs'):
                expect(
                    self.super_resultion_vector
                ).to(
                    equal_ndarray(self.restorer._Restorer__super_resultion_vector)
                )
                expect(
                    self.number_of_freq_estimations
                ).to(
                    equal(self.restorer._Restorer__number_of_freq_estimations)
                )
                expect(
                    self.max_freq
                ).to(
                    equal(self.restorer._Restorer__max_freq)
                )
                expect(
                    self.uniform_time_grid
                ).to(
                    equal_ndarray(self.restorer._Restorer__uniform_time_grid)
                )
                expect(
                    self.index_vector
                ).to(
                    equal_ndarray(self.restorer._Restorer__index_vector)
                )
                expect(
                    self.freq_vector
                ).to(
                    equal_ndarray(self.restorer._Restorer__freq_vector)
                )
                expect(
                    self.clean_window_vector
                ).to(
                    equal_ndarray(self.restorer._Restorer__clean_window_vector)
                )

        with shared_context('restoration result checker'):
            with it('contains correct keys'):
                expect(self.restoration_result).to(have_only_keys(*self.expected_keys))

            with it('has correct values and does not contain zeroes'):
                for key in self.expected_keys:
                    expect(
                        self.restoration_result[key]
                    ).to(contain_non_zero_vals(self.round_precision))
                    expect(
                        self.restoration_result[key]
                    ).to(equal_ndarray(getattr(self, key),self.round_precision))

        with description('restore'):
            with before.each:
                self.restoration_result = self.restorer.restore()
                self.expected_keys = [
                    'freq_vector', 'uniform_time_grid',
                    'clean_spectrum', 'correlogram',
                    'uniform_series', 'frequencies', 'amplitudes', 'phases'
                ]

            with included_context('restoration result checker'):
                pass

            with it('resturns non-None value'):
                expect(self.restoration_result).not_to(be_none)


        with description('#__restore_ccs'):
            with before.each:
                self.restoration_result = self.restorer._Restorer__restore_ccs()
                self.expected_keys = [
                     'clean_spectrum', 'correlogram', 'uniform_series'
                ]

            with included_context('restoration result checker'):
                pass

        with description('__restore_fap'):
            with before.each:
                self.restoration_result = self.restorer._Restorer__restore_fap()
                self.expected_keys = [
                     'frequencies', 'amplitudes', 'phases'
                ]

            with included_context('restoration result checker'):
                pass

        with description('#__build_clean_window_vector'):
            with before.each:
                self.actual_result =  self.restorer._Restorer__build_clean_window_vector()

            with it('returns correct value'):
                expect(self.actual_result).to(equal_ndarray(self.clean_window_vector))

        with description('#__build_uniform_time_grid'):
            with before.each:
                self.actual_result =  self.restorer._Restorer__build_uniform_time_grid(self.time_grid)

            with it('returns correct value'):
                expect(self.actual_result).to(equal_ndarray(self.uniform_time_grid))

        with shared_context('correct value checker'):
            with it('returns correct value'):
                expect(self.actual_result).to(equal_ndarray(self.expected_result))

        with description('#__build_clean_spectrum'):
            with before.all:
                self.expected_result = np.load("./spec/fixtures/clean_spectrum_1.pickle")

            with before.each:
                self.actual_result =  self.restorer._Restorer__build_clean_spectrum()

            with included_context('correct value checker'):
                pass

        with description('#__build_correlogram'):
            with before.all:
                self.expected_result = np.load("./spec/fixtures/correlogram_1.pickle")

            with before.each:
                self.actual_result =  self.restorer._Restorer__build_correlogram(self.clean_spectrum)

            with included_context('correct value checker'):
                pass

        with description('#__build_uniform_series'):
            with before.all:
                self.expected_result = np.load("./spec/fixtures/uniform_series_1.pickle")

            with before.each:
                self.actual_result =  self.restorer._Restorer__build_uniform_series(self.clean_spectrum)

            with included_context('correct value checker'):
                pass

        with description('#__build_correlogram_or_uniform_series'):
            with before.each:
                self.actual_result =  self.restorer._Restorer__build_correlogram_or_uniform_series(self.values)

            with description('argument is squared abs clean_spectrum)'):
                with before.all:
                    self.values = sch.squared_abs(self.clean_spectrum)
                    self.expected_result = np.load("./spec/fixtures/correlogram_1.pickle")

                with included_context('correct value checker'):
                    pass

            with description('argument is squared clean_spectrum)'):
                with before.all:
                    self.values = self.clean_spectrum
                    self.expected_result = np.load("./spec/fixtures/uniform_series_1.pickle")

                with included_context('correct value checker'):
                    pass