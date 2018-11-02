from spec.spec_helper import *
import clean.restorer as rst
import clean.matrix_builder as mb

with description(rst.Restorer) as self:
    with before.all:
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

            with it('has correct values'):
                for key in self.expected_keys_arr_result:
                    expect(
                        self.restoration_result[key]
                    ).to(contain_non_zero_vals)
                    expect(
                        self.restoration_result[key]
                    ).to(equal_ndarray(getattr(self, key)))

        with description('restore'):
            with before.each:
                self.restoration_result = self.restorer.restore()
                self.expected_keys = [
                    'freq_vector', 'uniform_time_grid',
                    'iterations', 'clean_spectrum', 'correlogram',
                    'uniform_series', 'frequencies', 'amplitudes', 'phases'
                ]

                self.expected_keys_arr_result = [
                    'freq_vector', 'uniform_time_grid',
                    'clean_spectrum', 'correlogram',
                    'uniform_series', 'frequencies', 'amplitudes', 'phases'
                ]

            with included_context('restoration result checker'):
                pass

            with it('resturns non-None value'):
                expect(self.restoration_result).not_to(be_none)

            with it('returns correct iteration value'):
                expect(
                    self.restoration_result['iterations']
                ).to(equal(self.iterations))

        with description('#__restore_ccs'):
            with before.each:
                self.restoration_result = self.restorer._Restorer__restore_ccs()
                self.expected_keys = [
                     'clean_spectrum', 'correlogram', 'uniform_series'
                ]
                self.expected_keys_arr_result = self.expected_keys

            with included_context('restoration result checker'):
                pass

        with description('__restore_fap'):
            with before.each:
                self.restoration_result = self.restorer._Restorer__restore_fap()
                self.expected_keys = [
                     'frequencies', 'amplitudes', 'phases'
                ]
                self.expected_keys_arr_result = self.expected_keys

            with included_context('restoration result checker'):
                pass