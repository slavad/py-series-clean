from spec.spec_helper import *
import clean.matrix_builder as mb

with description(mb) as self:
    with description('#estimate_max_freq'):
        with before.all:
            self.time_grid = np.array([0.0, 5.0, 6.0, 9.0, 20.0]).reshape((-1, 1))
        with description('by min distance'):
            with it('returns max freq estimated by minimum time distance'):
                expect(mb.estimate_max_freq(self.time_grid, False)).to(
                    equal(0.5)
                )
        with description('by average distance'):
            with it('returns max freq estimated by average time distance'):
                expect(mb.estimate_max_freq(self.time_grid, True)).to(
                    equal(0.1)
                )
    with description('#calculate_estimations_vector_size'):
        with before.all:
            self.time_grid = np.array([0.0, 3.5]).reshape((-1, 1))
        with it('calculates correct value'):
            max_freq = 0.8
            khi = 4
            expect(mb.calculate_estimations_vector_size(max_freq, self.time_grid, khi)).to(
                equal(12)
            )