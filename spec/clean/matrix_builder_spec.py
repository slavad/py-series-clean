from spec.spec_helper import *
import clean.matrix_builder as mb

with description(mb) as self:
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
                    np.all(
                        mb.generate_index_vector(self.vector_size) == self.expected_vector
                    )
                ).to(equal(True))

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
                self.values = np.array(
                    [
                        -1.0 + 0.1j,
                        0.9 - 1.4j,
                        -4.5 + 1.1j,
                        1.1 - 2.0j,
                        0.2 + 1.6j
                    ]
                ).reshape((-1, 1))
                self.number_of_freq_estimations = 2
                self.freq_vector = np.array(
                    [-2.0,0.0,2.0]
                ).reshape((-1, 1))

            with before.each:
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
                        )
                    ]
                ).reshape((-1, 1))
                #it's ok to round here, since the results are not exactly the same
                self.expected_result = np.round(self.expected_result*self.norm, 7)
            with it('returns correct transform matrix'):
                result = mb.run_ft(
                    self.time_grid_for_fun, self.values,
                    self.freq_vector_for_fun, self.number_of_freq_estimations,
                    self.kind
                )
                #see above
                result = np.round(result, 7)
                expect(
                    np.all(
                        result == self.expected_result
                    )
                ).to(equal(True))

        with description('kind == "direct"'):
            with before.each:
                self.kind = 'direct'
                self.time_grid_for_fun = self.time_grid
                self.freq_vector_for_fun = self.freq_vector
                self.coeff = -1j*2*np.pi
                self.norm = 1.0/self.time_grid_for_fun.shape[0]

            with included_context('run_ft results checker'):
                pass
        with description('kind == "inverse"'):
            with before.each:
                self.kind = 'inverse'
                self.time_grid_for_fun = self.time_grid.reshape((1,-1))
                self.freq_vector_for_fun = self.freq_vector.reshape((1,-1))
                self.coeff = 1j*2*np.pi
                self.norm = self.time_grid_for_fun.shape[0]/self.number_of_freq_estimations

            with included_context('run_ft results checker'):
                pass
        with description('kind == "qwerty"'):
            with before.each:
                self.time_grid = np.array(
                    [0.0]
                ).reshape((-1, 1))
                self.values = np.array(
                    [0]
                ).reshape((-1, 1))
                self.number_of_freq_estimations = 2
                self.freq_vector = np.array(
                    [0]
                ).reshape((-1, 1))
                self.kind = 'qwerty'
                self.time_grid_for_fun = self.time_grid
                self.freq_vector_for_fun = self.freq_vector
                self.coeff = 1
                self.norm = 1
                self.action = lambda: mb.run_ft(
                    self.time_grid_for_fun, self.values,
                    self.freq_vector_for_fun, self.number_of_freq_estimations,
                    self.kind
                )
            with it('raises error'):
                expect(
                    self.action
                ).to(raise_error(ValueError, "unknown kind"))