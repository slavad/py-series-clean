from helpers.common_imports import *
import clean.schuster as sch
import clean.matrix_builder as mb

class Iterator(object):
    """iterates over the dirty spectrum and extracts clean one"""
    def __init__(self, noise_probability, harmonic_share, number_of_freq_estimations, time_grid, values, max_freq):
        self.__harmonic_share = harmonic_share
        self.__number_of_freq_estimations = number_of_freq_estimations
        self.__time_grid = time_grid
        self.__values = values
        self.__max_freq = max_freq

        self.__dirty_vector = mb.calculate_dirty_vector(
            self.__time_grid, self.__values, self.__number_of_freq_estimations, self.__max_freq
        )
        dirty_subvector = self.__dirty_vector[number_of_freq_estimations:]
        schuster_count = sch.calc_schuster_counts(dirty_subvector, method_flag='average')[0]
        # eq 152 in ref 2
        self.__normalized_detection_threshold = schuster_count*(1.0 - noise_probability)
        self.__window_vector = mb.calculate_window_vector(
            self.__time_grid, self.__number_of_freq_estimations, self.__max_freq
        )

    def iterate(self, max_iterations):
        """iterator: steps 7 to 17 pp 51-52 ref 2"""
        super_resultion_vector = mb.build_super_resultion_vector(self.__number_of_freq_estimations)

        current_step = 0
        dirty_vector = self.__dirty_vector
        while current_step < max_iterations:
            result = self.__one_step(super_resultion_vector, dirty_vector)
            if not result:
                break
            else:
                dirty_vector = result['dirty_vector']
                super_resultion_vector = result['super_resultion_vector']
                current_step += 1
        result = {
            'super_resultion_vector': super_resultion_vector,
            'iterations': current_step
        }
        return result

    def __calculate_complex_amplitude(self, dirty_vector, max_count_index, max_count_value):
        """eq 154 ref 2"""
        window_value = self.__window_vector[2*self.__number_of_freq_estimations:][2*max_count_index][0]
        nominator = max_count_value + np.conj(max_count_value)*window_value
        denominator = 1 - sch.squared_abs(window_value)
        return nominator/denominator

    def __extract_data_from_dirty_vector(self, dirty_vector, max_count_index, complex_amplitude):
        """eq 155 ref 2"""
        # min_index corresponds to -m-th index in eq 155 ref 2 for W
        min_index = self.__number_of_freq_estimations
        # +1 since last value is not included, when the subarray is extracted
        # max_index corresponds to m-th index in eq 155 ref 2 for W
        max_index = 3*self.__number_of_freq_estimations + 1
        window_vector_left_shift = self.__window_vector[
            min_index - max_count_index:max_index - max_count_index
        ]
        window_vector_right_shift = self.__window_vector[
            min_index + max_count_index:max_index + max_count_index
        ]
        difference = complex_amplitude*window_vector_left_shift + np.conj(complex_amplitude)*window_vector_right_shift
        result = dirty_vector - self.__harmonic_share*difference
        return result

    def __add_data_to_super_resultion_vector(self, super_resultion_vector, max_count_index, complex_amplitude):
        """eq 156 ref 2"""
        #self.__number_of_freq_estimations index corresponds the 0th index in eq 156 ref 2 for vector C
        vector_to_add = mb.build_super_resultion_vector(self.__number_of_freq_estimations)
        vector_to_add[self.__number_of_freq_estimations + max_count_index] = self.__harmonic_share*complex_amplitude
        vector_to_add[self.__number_of_freq_estimations - max_count_index] = self.__harmonic_share*np.conj(complex_amplitude)
        result = vector_to_add + super_resultion_vector
        return result

    def __get_max_count_index_and_value(self, old_dirty_vector):
        """gets max count index and value"""
        dirty_subvector_wo_zero = old_dirty_vector[self.__number_of_freq_estimations+1:]
        # we need to add 1 to the index, because our dirty_vector index has different indexing:
        # from -number_of_freq_estimations to number_of_freq_estimations
        max_count_index = sch.calc_schuster_counts(
            dirty_subvector_wo_zero, method_flag='argmax'
        )[0] + 1
        max_count_value = dirty_subvector_wo_zero[max_count_index - 1][0]
        result = {
            'index': max_count_index,
            'value': max_count_value
        }
        return result

    def __one_step(self, old_super_resultion_vector, old_dirty_vector):
        """one step of the iteration process"""
        max_count_index_and_value = self.__get_max_count_index_and_value(old_dirty_vector)
        if sch.squared_abs(max_count_index_and_value['value']) >= self.__normalized_detection_threshold:
            # eq 154 ref 2
            complex_amplitude = self.__calculate_complex_amplitude(
                old_dirty_vector,
                max_count_index_and_value['index'],
                max_count_index_and_value['value']
            )
            dirty_vector = self.__extract_data_from_dirty_vector(
                old_dirty_vector,
                max_count_index_and_value['index'],
                complex_amplitude
            )
            super_resultion_vector = self.__add_data_to_super_resultion_vector(
                old_super_resultion_vector,
                max_count_index_and_value['index'],
                complex_amplitude
            )
            result = {
                'dirty_vector': dirty_vector,
                'super_resultion_vector': super_resultion_vector
            }
            return result
        else:
            return None
