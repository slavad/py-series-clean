from spec.spec_helper import *
import clean.iterator as itr
import clean.matrix_builder as mb
import clean.schuster as sch

with description(itr.Iterator) as self:
    with before.all:
        #TODO test also with noise only
        #TODO refactor all with equal_ndarray and equal_with_precision
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

        self.window_vector = mb.calculate_window_vector(
            self.time_grid, self.number_of_freq_estimations, self.max_freq
        )

    with before.each:
        self.iterator = itr.Iterator(
            self.treshold,
            self.harmonic_share, self.number_of_freq_estimations,
            self.time_grid, self.values, self.max_freq
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
                self.values
            ).to(
                equal_ndarray(self.iterator._Iterator__values)
            )
            expect(
                self.max_freq
            ).to(
                equal(self.iterator._Iterator__max_freq)
            )
            expect(
                self.dirty_vector
            ).to(
                equal_ndarray(self.iterator._Iterator__dirty_vector)
            )
            expect(
                sch.calc_schuster_counts(self.dirty_vector[self.number_of_freq_estimations:], method_flag='average')[0]*self.treshold
            ).to(
                equal(self.iterator._Iterator__normalized_detection_treshold)
            )
            expect(
                self.window_vector
            ).to(
                equal_ndarray(self.iterator._Iterator__window_vector)
            )

    with description('#__calculate_complex_amplitude'):
        with before.all:
            self.max_count_index = 12
            max_count_value = self.dirty_vector[self.number_of_freq_estimations:][self.max_count_index][0]
            window_value = self.window_vector[2*self.number_of_freq_estimations:][2*self.max_count_index][0]
            nominator = max_count_value + np.conj(max_count_value)*window_value
            denominator = 1 - np.abs(np.power(window_value, 2))
            self.expected_value = nominator/denominator

        with it('retruns correct value'):
            expect(
                self.iterator._Iterator__calculate_complex_amplitude(self.dirty_vector, self.max_count_index)
            ).to(
                equal(self.expected_value)
            )
