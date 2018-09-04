from spec.spec_helper import *
import clean.iterator as itr
import clean.matrix_builder as mb
import clean.schuster as sch

with description(itr.Iterator) as self:
    with before.all:
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

        self.max_count_index = 12
        self.max_count_value = self.dirty_vector[
            self.number_of_freq_estimations:
        ][self.max_count_index][0]

        self.complex_amplitude = 4.690355355904826+1.7147337162545526j

        self.super_resultion_vector = mb.build_super_resultion_vector(self.number_of_freq_estimations)

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

    with description('iterate'):
        # TODO: modify functions that return arrays
        # return dictionary values!
        with description('noise only in dirty_vector'):
            pass

        with description('signal with noise in dirty_vector'):
            pass

        with description('signal without noise in dirty_vector'):
            pass

    with description('#__calculate_complex_amplitude'):
        with before.all:
            self.expected_value = self.complex_amplitude

        with it('retruns correct value'):
            expect(
                self.iterator._Iterator__calculate_complex_amplitude(
                    self.dirty_vector, self.max_count_index, self.max_count_value
                )
            ).to(
                equal(self.expected_value)
            )

    with shared_context('array comparer'):
        with it('has different value, but the same shape'):
            expect(
                self.actual_vector
            ).to(equal_ndarray(self.expected_vector))

            expect(
                self.actual_vector
            ).not_to(equal_ndarray(self.initial_vector))

            expect(
                self.actual_vector.shape
            ).to(equal(self.initial_vector.shape))

    with description('#__extract_data_from_dirty_vector'):
        with before.all:
            self.expected_vector =  np.load(
                "./spec/fixtures/dirty_vector_with_extracted_data.pickle"
            )
            self.initial_vector = self.dirty_vector
        with before.each:
            self.actual_vector = self.iterator._Iterator__extract_data_from_dirty_vector(
                self.dirty_vector, self.max_count_index, self.complex_amplitude
            )

        with included_context('array comparer'):
            pass

    with description('#__add_data_to_super_resultion_vector'):
        with before.all:
            self.expected_vector =  np.load(
                "./spec/fixtures/super_resol_vector_with_added.pickle"
            )
            self.initial_vector = self.super_resultion_vector

        with before.each:
            self.actual_vector = self.iterator._Iterator__add_data_to_super_resultion_vector(
                self.super_resultion_vector, self.max_count_index, self.complex_amplitude
            )

        with included_context('array comparer'):
            pass

    with description('#__get_max_count_index_and_value'):
        with before.all:
            self.number_of_freq_estimations = 3
            self.expected_max_count_index = 1

        with before.each:
            self.actual_max_count_index, self.actual_max_count_value = self.iterator._Iterator__get_max_count_index_and_value(
                self.old_dirty_vector
            )
            self.index_shift = 3
            self.expected_max_count_value = self.old_dirty_vector[self.expected_max_count_index + self.index_shift][0]

            self.global_max_count_index = sch.calc_schuster_counts(
                self.old_dirty_vector, method_flag='argmax'
            )[0] - self.index_shift

        with shared_context('index and value comparer'):
            with it('returns max value among positive indexes'):
                expect(self.expected_max_count_index).to(equal(self.actual_max_count_index))
                expect(self.expected_max_count_value).to(equal(self.actual_max_count_value))

        with shared_context('global index comparer'):
            with it('global max index value is not equal to positive max index value'):
                expect(self.global_max_count_index).not_to(equal(self.actual_max_count_index))
                expect(self.global_max_count_index).to(equal(self.expected_global_max_count_index))

        with description('global max value has negative index'):
            with before.all:
                self.old_dirty_vector = np.array(
                    [
                        -0.46675812-8.47496127j, # -3
                        0.27706322+0.13034116j,  # -2
                        0.7039825 +0.23917624j,  # -1
                        0.81231448-0.22629087j,  # 0
                        0.81979139-7.79749563j,  # 1
                        -0.47948349+0.05279927j, # 2
                        0.71972369+0.53702611j   # 3
                    ]
                ).reshape((-1, 1))
                self.expected_global_max_count_index = -3

            with included_context('index and value comparer'):
                pass

            with included_context('global index comparer'):
                pass

        with description('global max value has zero index'):
            with before.all:
                self.old_dirty_vector = np.array(
                    [
                        -0.46675812-0.47496127j, # -3
                        0.27706322+0.13034116j,  # -2
                        0.7039825 +0.23917624j,  # -1
                        0.81231448-9.22629087j,  # 0
                        0.81979139-7.79749563j,  # 1
                        -0.47948349+0.05279927j, # 2
                        0.71972369+0.53702611j   # 3
                    ]
                ).reshape((-1, 1))
                self.expected_global_max_count_index = 0
            with included_context('index and value comparer'):
                pass

            with included_context('global index comparer'):
                pass

        with description('global max value has positive index'):
            with before.all:
                self.old_dirty_vector = np.array(
                    [
                        -0.46675812-0.47496127j,  # -3
                        0.27706322+0.13034116j,   # -2
                        0.7039825 +0.23917624j,   # -1
                        0.81231448-0.22629087j,   # 0
                        0.81979139-10.79749563j,   # 1
                        -1.47948349+0.05279927j, # 2,
                        0.71972369+0.53702611j    # 3
                    ]
                ).reshape((-1, 1))
            with included_context('index and value comparer'):
                pass

            with it('has global max value equal to positive max value'):
                expect(self.global_max_count_index).to(equal(self.actual_max_count_index))

    with description('__one_step'):
        with before.all:
            self.old_super_resultion_vector = mb.build_super_resultion_vector(
                self.number_of_freq_estimations
            )
        with description('dirty_vector contains signal'):
            with before.all:
                self.expected_super_resultion_vector_with_added_data =  np.load(
                    "./spec/fixtures/super_resol_vector_with_added.pickle"
                )
                self.expected_dirty_vector_with_extracted_data =  np.load(
                    "./spec/fixtures/dirty_vector_with_extracted_data.pickle"
                )
                self.old_dirty_vector = self.dirty_vector
            with before.each:
                (
                    self.actual_dirty_vector_with_extracted_data,
                    self.actual_super_resultion_vector_with_added_data
                ) = self.iterator._Iterator__one_step(
                    self.old_super_resultion_vector, self.old_dirty_vector
                )
            with description('super resolution vector'):
                with before.each:
                    self.initial_vector = self.old_super_resultion_vector
                    self.actual_vector = self.actual_super_resultion_vector_with_added_data
                    self.expected_vector = self.expected_super_resultion_vector_with_added_data

                with included_context('array comparer'):
                    pass

            with description('dirty vector'):
                with before.each:
                    self.initial_vector = self.old_dirty_vector
                    self.actual_vector = self.actual_dirty_vector_with_extracted_data
                    self.expected_vector = self.expected_dirty_vector_with_extracted_data

                with included_context('array comparer'):
                    pass

        with description('dirty vector does not contain signal'):
            with before.all:
                self.old_dirty_vector = np.load(
                    "./spec/fixtures/old_dirty_vector_no_signal.pickle"
                )
            with before.each:
                self.result = self.iterator._Iterator__one_step(
                    self.old_super_resultion_vector, self.old_dirty_vector
                )
            with it('returns None'):
                expect(self.result).to(be_none)
