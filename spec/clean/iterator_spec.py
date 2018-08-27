from spec.spec_helper import *
import clean.iterator as itr
import clean.matrix_builder as mb
import clean.schuster as sch

with description(itr.Iterator) as self:
    with before.all:
        #TODO test also with noise only
        #TODO write custom matcher for numpy arrays and refactor with it!
        self.time_grid_and_values = (
            np.load("./spec/fixtures/time_grid_1.pickle"),
            np.load("./spec/fixtures/series_1.pickle")
        )
        self.time_grid = self.time_grid_and_values[0]
        self.values = self.time_grid_and_values[1]
        self.khi = 4
        self.use_aver = False # TODO: test with true later
        self.max_freq = mb.estimate_max_freq(self.time_grid, self.use_aver)
        self.number_of_freq_estimations = mb.calculate_estimations_vector_size(
            self.max_freq, self.time_grid, self.khi
        )
        self.treshold = 0.8
        self.harmonic_share = 0.5

        self.dirty_vector = mb.calculate_dirty_vector(
            self.time_grid, self.values, self.number_of_freq_estimations, self.max_freq
        )

        self.iterator = itr.Iterator(
            self.treshold,
            self.harmonic_share, self.number_of_freq_estimations,
            self.time_grid, self.values, self.max_freq
        )

        self.window_vector = mb.calculate_window_vector(
            self.time_grid, self.number_of_freq_estimations, self.max_freq
        )

    with description('__init__'):
        with it('sets all values'):
            expect(
                self.harmonic_share
            ).to(
                equal(self.iterator._Iterator__harmonic_share)
            )
            expect(
                self.number_of_freq_estimations
            ).to(
                equal(self.iterator._Iterator__number_of_freq_estimations)
            )
            expect(
                self.time_grid
            ).to(
                equal_ndarray(self.iterator._Iterator__time_grid)
            )
            expect(
                np.all(self.values == self.iterator._Iterator__values)
            ).to(
                equal(True)
            )
            expect(
                self.max_freq
            ).to(
                equal(self.iterator._Iterator__max_freq)
            )
            expect(
                np.all(self.dirty_vector == self.iterator._Iterator__dirty_vector)
            ).to(
                equal(True)
            )
            expect(
                sch.calc_schuster_counts(self.dirty_vector[self.number_of_freq_estimations:], method_flag='average')[0]*self.treshold
            ).to(
                equal(self.iterator._Iterator__normalized_detection_treshold)
            )
            expect(
                np.all(self.window_vector == self.iterator._Iterator__window_vector)
            ).to(
                equal(True)
            )

    with description('#iterator'):
        with it('iterates'):
            pass