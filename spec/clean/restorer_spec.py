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
                have_keys(*self.expected_restorer_vars)
            )
            expect(
                len(self.restorer.__dict__.keys())
            ).to(equal(len(self.expected_restorer_vars)))
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
        with description('restore'):
            with before.each:
                self.restoration_result = self.restorer.restore()
                self.expected_keys = [
                    'freq_vector', 'uniform_time_grid',
                    'iterations', 'clean_spectrum', 'correlogram',
                    'uniform_series', 'frequencies', 'amplitudes', 'phases'
                ]

            with it('resturns non-None value'):
                expect(self.restoration_result).not_to(be_none)

            with it('returns dict with correct keys'):
                expect(self.restoration_result).to(have_keys(*self.expected_keys))
                expect(
                    len(self.restoration_result)
                ).to(equal(len(self.expected_keys)))

            with it('returns correct key values'):
                expect(
                    self.restoration_result['freq_vector']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['freq_vector']
                ).to(equal_ndarray(self.freq_vector))

                expect(
                    self.restoration_result['uniform_time_grid']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['uniform_time_grid']
                ).to(equal_ndarray(self.uniform_time_grid))

                expect(
                    self.restoration_result['iterations']
                ).to(equal(self.iterations))

                expect(
                    self.restoration_result['clean_spectrum']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['clean_spectrum']
                ).to(equal_ndarray(self.clean_spectrum))

                expect(
                    self.restoration_result['correlogram']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['correlogram']
                ).to(equal_ndarray(self.correlogram))

                expect(
                    self.restoration_result['uniform_series']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['uniform_series']
                ).to(equal_ndarray(self.uniform_series))

                expect(
                    self.restoration_result['frequencies']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['frequencies']
                ).to(equal_ndarray(self.frequencies))

                expect(
                    self.restoration_result['amplitudes']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['amplitudes']
                ).to(equal_ndarray(self.amplitudes))

                expect(
                    self.restoration_result['phases']
                ).to(contain_non_zero_vals)
                expect(
                    self.restoration_result['phases']
                ).to(equal_ndarray(self.phases))