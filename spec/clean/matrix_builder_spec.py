from spec.spec_helper import *
import clean.matrix_builder as mb

with description(mb) as self:
    with shared_context('compare actual and expected with precision'):
        with it('returns correct vector'):
            expect(
                self.expected_result
            ).to(
                equal_ndarray(self.actual_result, self.precision)
            )

    with before.all:
        self.precision = 7
    with description('#estimate_max_freq'):
        with before.all:
            self.time_grid = np.array(
                [0.0, 5.0, 6.0, 9.0, 20.0]
            ).reshape((-1, 1))
        with description('by min distance'):
            with it('returns max freq estimated by minimum time distance'):
                expected_max_freq = 0.5
                expect(mb.estimate_max_freq(self.time_grid, False)).to(
                    equal(expected_max_freq)
                )
        with description('by average distance'):
            with it('returns max freq estimated by average time distance'):
                expected_max_freq = 0.1
                expect(mb.estimate_max_freq(self.time_grid, True)).to(
                    equal(expected_max_freq)
                )

    with description('#calculate_estimations_vector_size'):
        with before.all:
            self.time_grid = np.array([0.0, 3.5]).reshape((-1, 1))
        with it('calculates correct value'):
            max_freq = 0.8
            khi = 4
            expected_num_of_freq_estimations = 12
            expect(mb.calculate_estimations_vector_size(max_freq, self.time_grid, khi)).to(
                equal(expected_num_of_freq_estimations)
            )

    with description('#generate_index_vector'):
        with description('argument is odd'):
            with before.all:
                self.vector_size = 5
                self.expected_vector = np.array(
                    [-2, -1, 0, 1, 2]
                ).reshape((-1, 1))
            with it('generates correct vector'):
                expect(
                    mb.generate_index_vector(self.vector_size)
                ).to(equal_ndarray(self.expected_vector))

        with description('argument is event'):
            with before.all:
                self.vector_size = 4
            with it('raises error'):
                expect(
                    lambda: mb.generate_index_vector(self.vector_size)
                ).to(raise_error(ValueError, "matrix_size must be odd"))

    with description('#run_ft'):
        with shared_context('run_ft results checker'):
            with before.all:
                self.time_grid = np.array(
                    [0.0, 0.5, 0.6, 0.9, 2.0]
                ).reshape((-1, 1))
                self.number_of_freq_estimations = 2
                self.freq_vector = np.array(
                    [-2.0,0.0,2.0]
                ).reshape((-1, 1))

            with before.each:
                #it's ok to round here, since the results are not exactly the same
                self.expected_result = self.expected_result*self.norm
                self.actual_result = mb.run_ft(
                    self.time_grid, self.values,
                    self.freq_vector, self.number_of_freq_estimations,
                    self.kind
                )

            with included_context('compare actual and expected with precision'):
                pass

        with description('kind == "direct"'):
            with before.each:
                self.kind = 'direct'
                self.coeff = -1j*2*np.pi
                self.norm = 1.0/self.time_grid.shape[0]
                self.values = np.array(
                    [
                        -1.0 + 0.1j,
                        0.9 - 1.4j,
                        -4.5 + 1.1j,
                        1.1 - 2.0j,
                        0.2 + 1.6j
                    ]
                ).reshape((-1, 1))
                self.expected_result = np.array(
                    # see e.g. eq 148 ref 2
                    [
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[0][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[1][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[2][0]*self.time_grid
                            )*self.values
                        )
                    ]
                ).reshape((-1, 1))

            with included_context('run_ft results checker'):
                pass
        with description('kind == "inverse"'):
            with before.each:
                self.kind = 'inverse'
                self.coeff = 1j*2*np.pi
                self.values = np.array(
                    [
                        -1.0 + 0.1j,
                        0.9 - 1.4j,
                        -4.5 + 1.1j
                    ]
                ).reshape((-1, 1))
                self.norm = self.time_grid.shape[0]/self.number_of_freq_estimations
                self.expected_result = np.array(
                # see e.g. eq 161 ref 2
                    [
                        np.sum(
                            np.exp(
                                self.coeff*self.time_grid[0][0]*self.freq_vector
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.time_grid[1][0]*self.freq_vector
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.time_grid[2][0]*self.freq_vector
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.time_grid[3][0]*self.freq_vector
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.time_grid[4][0]*self.freq_vector
                            )*self.values
                        )
                    ]
                ).reshape((-1, 1))

            with included_context('run_ft results checker'):
                pass
        with description('kind == "qwerty"'):
            with before.each:
                self.time_grid = None
                self.values = None
                self.number_of_freq_estimations = None
                self.freq_vector = None
                self.kind = 'qwerty'
                self.coeff = None
                self.norm = None
                self.action = lambda: mb.run_ft(
                    self.time_grid, self.values,
                    self.freq_vector, self.number_of_freq_estimations,
                    self.kind
                )
            with it('raises error'):
                expect(
                    self.action
                ).to(raise_error(ValueError, "unknown kind"))

    with description('#generate_freq_vector'):
        with before.all:
            self.index_vector = np.array([-1.0, 0.0, 1.0])
            self.max_freq = 2.0
            self.number_of_freq_estimations = 3
            self.expected_result = self.index_vector*self.max_freq/self.number_of_freq_estimations
        with it('generates correct value'):
            expect(
                self.expected_result
            ).to(
                equal_ndarray(
                    mb.generate_freq_vector(
                        self.index_vector, self.max_freq, self.number_of_freq_estimations
                    )
                )
            )

    with description('#size_of_spectrum_vector'):
        with before.all:
            self.number_of_freq_estimations = 3
            self.expected_result = 2*self.number_of_freq_estimations + 1
        with it('returns correct value'):
            expect(self.expected_result).to(
                equal(mb.size_of_spectrum_vector(self.number_of_freq_estimations))
            )
    with description('#size_of_window_vector'):
        with before.all:
            self.number_of_freq_estimations = 3
            self.expected_result = 4*self.number_of_freq_estimations + 1
        with it('returns correct value'):
            expect(self.expected_result).to(
                equal(mb.size_of_window_vector(self.number_of_freq_estimations))
            )

    with description('vector generators'):
        with before.all:
            self.time_grid = np.array(
                [0.0, 0.5, 0.6, 0.9, 2.0]
            ).reshape((-1, 1))
            self.max_freq = 2
            self.number_of_freq_estimations = 3
            self.coeff = -1j*2*np.pi
            self.norm = 1.0/self.time_grid.shape[0]

        with description('#calculate_dirty_vector'):
            with before.each:
                self.values = np.array(
                    [-1.0, 0.9, -4.5, 1.1, 0.2]
                ).reshape((-1, 1))

                self.index_vector = mb.generate_index_vector(
                    mb.size_of_spectrum_vector(self.number_of_freq_estimations)
                )
                self.freq_vector = mb.generate_freq_vector(
                    self.index_vector,
                    self.max_freq,
                    self.number_of_freq_estimations
                )
                self.expected_result = np.array(
                    [
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[0][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[1][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[2][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[3][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[4][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[5][0]*self.time_grid
                            )*self.values
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[6][0]*self.time_grid
                            )*self.values
                        )
                    ]
                ).reshape((-1, 1))*self.norm
                self.actual_result = mb.calculate_dirty_vector(
                    self.time_grid,
                    self.values,
                    self.number_of_freq_estimations,
                    self.max_freq
                )
            with included_context('compare actual and expected with precision'):
                pass

        with description('#calculate_window_vector'):
            with before.each:
                self.values = np.array(
                    [-1.0, 0.9, -4.5, 1.1, 0.2]
                ).reshape((-1, 1))

                self.index_vector = mb.generate_index_vector(
                    mb.size_of_window_vector(self.number_of_freq_estimations)
                )
                self.freq_vector = mb.generate_freq_vector(
                    self.index_vector,
                    self.max_freq,
                    self.number_of_freq_estimations
                )
                self.expected_result = np.array(
                    [
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[0][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[1][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[2][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[3][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[4][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[5][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[6][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[7][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[8][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[9][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[10][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[11][0]*self.time_grid
                            )
                        ),
                        np.sum(
                            np.exp(
                                self.coeff*self.freq_vector[12][0]*self.time_grid
                            )
                        )
                    ]
                ).reshape((-1, 1))*self.norm
                self.actual_result = mb.calculate_window_vector(
                    self.time_grid,
                    self.number_of_freq_estimations,
                    self.max_freq
                )

            with included_context('compare actual and expected with precision'):
                pass

        with description('#build_super_resultion_vector'):
            with before.all:
                self.vector_size = mb.size_of_spectrum_vector(self.number_of_freq_estimations)
                self.expected_result = np.array([
                    0+0j,
                    0+0j,
                    0+0j,
                    0+0j,
                    0+0j,
                    0+0j,
                    0+0j
                ]).reshape((-1, 1))
            with it('returns correct vector'):
                actual_result = mb.build_super_resultion_vector(self.number_of_freq_estimations)
                expect(
                    actual_result
                ).to(equal_ndarray(self.expected_result))