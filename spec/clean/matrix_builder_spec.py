from spec.spec_helper import *
import clean.matrix_builder as mb

with description(mb) as self:
    with description('#estimate_max_freq'):
        with before.all:
            self.time_grid = np.array([0.0, 5.0, 6.0, 9.0, 20.0]).reshape((-1, 1))
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
                ).to(raise_error(ValueError))