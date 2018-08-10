import numpy as np
import py_series_clean.schuster as sch
import py_series_clean.matrix_builder as mb
import pdb

class Iterator(object):
    """iterates over the dirty spectrum and extracts clean one"""
    def __init__(self, treshold, max_iterations, harmonic_share, number_of_freq_estimations, time_grid, values, max_freq):
        self.treshold = treshold
        self.max_iterations = max_iterations
        self.harmonic_share = harmonic_share
        self.number_of_freq_estimations = number_of_freq_estimations
        self.time_grid = time_grid
        self.values = values
        self.max_freq = max_freq
        self.window_vector = mb.calculate_window_vector(
            self.time_grid, self.number_of_freq_estimations, self.max_freq
        )

    def iterate(self):
        """iterator: steps 7 to 17 pp 51-52 ref 2"""
        super_resultion_vector = mb.build_super_resultion_vector(self.number_of_freq_estimations)
        dirty_vector = mb.calculate_dirty_vector(
            self.time_grid, self.values, self.number_of_freq_estimations, self.max_freq
        )
        current_step = 0

        while current_step < self.max_iterations:
            result = self.one_step(super_resultion_vector, dirty_vector)
            if not result:
                break
            else:
                dirty_vector, super_resultion_vector = result
                current_step += 1
        return super_resultion_vector, current_step

    def calculate_complex_amplitude(self, dirty_vector, max_count_index):
        """eq 154 ref 2"""
        max_count_value = dirty_vector[self.number_of_freq_estimations:][max_count_index][0]
        window_value = self.window_vector[2*self.number_of_freq_estimations:][2*max_count_index][0]
        nominator = max_count_value + np.conj(max_count_value)*window_value
        denominator = 1 - sch.squared_abs(window_value)
        return nominator/denominator

    def extract_data_from_dirty_spec(self, dirty_vector, max_count_index, complex_amplitude):
        """eq 155 ref 2"""
        #TODO: check if vector shifts are ok here and above and below
        min_index = self.number_of_freq_estimations
        max_index = self.number_of_freq_estimations + 2*self.number_of_freq_estimations + 1
        window_vector_left_shift = self.window_vector[
            min_index - max_count_index:max_index - max_count_index
        ]
        window_vector_right_shift = self.window_vector[
            min_index + max_count_index:max_index + max_count_index
        ]
        difference = complex_amplitude*window_vector_left_shift + np.conj(complex_amplitude)*window_vector_right_shift
        result = dirty_vector - self.harmonic_share*difference
        return result

    def add_data_to_super_resultion_vector(self, super_resultion_vector, max_count_index, complex_amplitude):
        """eq 156 ref 2"""
        #TODO: check if vector shifts are ok here and above and below
        vector_to_add = mb.build_super_resultion_vector(self.number_of_freq_estimations)
        vector_to_add[self.number_of_freq_estimations + max_count_index] = self.harmonic_share*complex_amplitude
        vector_to_add[self.number_of_freq_estimations - max_count_index] = self.harmonic_share*np.conj(complex_amplitude)
        result = vector_to_add + super_resultion_vector
        return result

    def one_step(self, old_super_resultion_vector, old_dirty_vector):
        """one step of the iteration process"""
        dirty_subvector = old_dirty_vector[self.number_of_freq_estimations:]
        schuster_count = sch.calc_schuster_counts(dirty_subvector, method_flag='average')[0]
        # eq 152 in ref 2
        normalized_detection_treshold = schuster_count*self.treshold
        dirty_subvector_wo_zero = old_dirty_vector[self.number_of_freq_estimations+1:]
        # we need to add 1 to the index, because our dirty_vector index has different indexing:
        # from -number_of_freq_estimations to number_of_freq_estimations
        max_count_index = sch.calc_schuster_counts(dirty_subvector_wo_zero, method_flag='argmax')[0] + 1
        max_count_value = dirty_subvector_wo_zero[max_count_index - 1][0]
        if sch.squared_abs(max_count_value) >= normalized_detection_treshold:
            # eq 154 ref 2
            complex_amplitude = self.calculate_complex_amplitude(old_dirty_vector, max_count_index)
            dirty_vector = self.extract_data_from_dirty_spec(
                old_dirty_vector,
                max_count_index, complex_amplitude
            )
            super_resultion_vector = self.add_data_to_super_resultion_vector(
                old_super_resultion_vector,max_count_index,
                complex_amplitude
            )
            return dirty_vector, super_resultion_vector
        else:
            return None
