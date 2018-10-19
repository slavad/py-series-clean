from spec.spec_helper import *
import clean.iterator as itr
import clean.matrix_builder as mb
import clean.schuster as sch

with description(itr.Iterator) as self:
    with before.all:
        self.time_grid = np.load("./spec/fixtures/time_grid_1.pickle")
        self.values = np.load("./spec/fixtures/series_1.pickle")
        self.khi = 4
        self.max_freq = 928.6049396317791 # precalculated value
        self.number_of_freq_estimations = 35934 # precalculated value
        self.false_alarm_probability = 0.2
        self.harmonic_share = 0.5

        self.dirty_vector = mb.calculate_dirty_vector(
            self.time_grid, self.values, self.number_of_freq_estimations, self.max_freq
        )

        self.window_vector = mb.calculate_window_vector(
            self.time_grid, self.number_of_freq_estimations, self.max_freq
        )

        self.max_count_index = 12
        self.round_precision = 10
        self.max_count_value = self.dirty_vector[
            self.number_of_freq_estimations:
        ][self.max_count_index][0]

        self.complex_amplitude = 4.690355355904826+1.7147337162545526j

        self.super_resultion_vector = mb.build_super_resultion_vector(self.number_of_freq_estimations)

    with before.each:
        self.iterator = itr.Iterator(
            self.false_alarm_probability,
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
                sch.calc_schuster_counts(self.dirty_vector[self.number_of_freq_estimations:], method_flag='average')[0]*(1.0 - self.false_alarm_probability)
            ).to(
                equal(self.iterator._Iterator__detection_threshold)
            )
            expect(
                self.window_vector
            ).to(
                equal_ndarray(self.iterator._Iterator__window_vector)
            )

    with description('iterate'):
        with shared_context('max value checker'):
            with it('super_resultion_vector contains non-zero values'):
                expect(self.max_value_abs).to(
                    be_above(0.0)
                )

        with shared_context('iterations result checker'):
            with it('contains correct key list'):
                expect(
                    set(self.actual_iteration_result.keys())
                ).to(equal(self.expected_key_list))

            with it('contains correct iterations count'):
                expect(
                    self.actual_iteration_result['iterations']
                ).to(equal(self.expected_iterations))

            with it('returns correct super_resultion_vector value'):
                expect(
                    self.actual_iteration_result['super_resultion_vector']
                ).to(equal_ndarray(self.expected_super_resultion_vector, self.round_precision))

        with before.all:
            self.values = np.load("./spec/fixtures/series_1.pickle")
            self.expected_key_list = {'super_resultion_vector', 'iterations'}

        with before.each:
            self.actual_iteration_result = self.iterator.iterate(self.max_iterations)
            self.max_value_abs = np.max(
                np.abs(self.actual_iteration_result['super_resultion_vector'])
            )

        with description('noise only in dirty_vector'):
            with before.all:
                self.max_iterations = 10
                self.expected_iterations = 4
                self.expected_super_resultion_vector = np.load('./spec/fixtures/super_resultion_vector_with_result_1.pickle')

            with included_context('max value checker'):
                pass

            with included_context('iterations result checker'):
                pass


        with description('itereations do not converge, because max_iterations is too small'):
            with before.all:
                self.max_iterations = 3
                self.expected_iterations = 3
                self.expected_super_resultion_vector_converged = np.load('./spec/fixtures/super_resultion_vector_with_result_1.pickle')
                self.expected_super_resultion_vector = np.load('./spec/fixtures/super_resultion_vector_with_result_2.pickle')

            with included_context('max value checker'):
                pass

            with included_context('iterations result checker'):
                pass

            with it('converged vector is not equal to expected_super_resultion_vector'):
                expect(
                    self.actual_iteration_result['super_resultion_vector']
                ).not_to(equal_ndarray(self.expected_super_resultion_vector_converged))

        with description('signal with noise only in dirty_vector'):
            with before.all:
                self.values = np.random.normal(loc=0.0, scale=1, size=100).reshape(-1, 1)
                self.false_alarm_probability = 0
                self.max_iterations = 10
                self.expected_iterations = 0
                #self.expected_super_resultion_vector = np.load('./spec/fixtures/super_resultion_vector_with_result_3.pickle')

            # with it('super_resultion_vector contains zero values'):
            #     expect(self.max_value_abs).to(
            #         equal(0.0)
            #     )
            #
            # with included_context('iterations result checker'):
            #     pass
        #
        # with description('signal without noise in dirty_vector'):
        #     pass

    with description('#__calculate_complex_amplitude'):
        with before.all:
            self.expected_value = self.complex_amplitude

        with it('retruns correct value'):
            expect(
                self.iterator._Iterator__calculate_complex_amplitude(
                    self.dirty_vector, self.max_count_index, self.max_count_value
                )
            ).to(
                equal_with_precision(self.expected_value, self.round_precision)
            )

    with shared_context('array comparer'):
        with it('has different value, but the same shape'):
            expect(
                self.actual_vector
            ).to(equal_ndarray(self.expected_vector, self.round_precision))

            expect(
                self.actual_vector
            ).not_to(equal_ndarray(self.initial_vector, self.round_precision))

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
            index_and_max_count_value = self.iterator._Iterator__get_max_count_index_and_value(
                self.old_dirty_vector
            )
            self.actual_max_count_index = index_and_max_count_value['index']
            self.actual_max_count_value = index_and_max_count_value['value']
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
                one_step_result = self.iterator._Iterator__one_step(
                    self.old_super_resultion_vector, self.old_dirty_vector
                )
                self.actual_dirty_vector_with_extracted_data = one_step_result['dirty_vector']
                self.actual_super_resultion_vector_with_added_data = one_step_result['super_resultion_vector']
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
