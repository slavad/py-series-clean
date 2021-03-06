from helpers.common_imports import *
import clean.matrix_builder as mb
import clean.schuster as sch

class Restorer(object):
    """restores clean spectrum, algorithm steps 18 to 21 ref 2"""
    def __init__(self, iterations, super_resultion_vector, number_of_freq_estimations, time_grid, max_freq):
        self.__iterations = iterations
        if iterations != 0:
            self.__super_resultion_vector = super_resultion_vector
            self.__number_of_freq_estimations = number_of_freq_estimations
            self.__max_freq = max_freq
            self.__uniform_time_grid = self.__build_uniform_time_grid(time_grid)
            self.__index_vector = mb.generate_index_vector(
                mb.size_of_spectrum_vector(self.__number_of_freq_estimations)
            )
            self.__freq_vector = mb.generate_freq_vector(
                self.__index_vector, self.__max_freq, self.__number_of_freq_estimations
            )
            self.__clean_window_vector = self.__build_clean_window_vector()


    def restore(self):
        """restores spectrum and series"""
        # if nothing was detected:
        if self.__iterations == 0:
            return None
        else:
            ccs_restoration_result = self.__restore_ccs()
            fap_restoration_result = self.__restore_fap()
            result = {
                'freq_vector': self.__freq_vector,
                'uniform_time_grid': self.__uniform_time_grid
            }

            result.update(ccs_restoration_result)
            result.update(fap_restoration_result)

            return result

    def __restore_ccs(self):
        """restores clean spectrum, algorithm steps 18 to 21 ref 2"""
        clean_spectrum = self.__build_clean_spectrum()
        correlogram = self.__build_correlogram(clean_spectrum)
        uniform_series = self.__build_uniform_series(clean_spectrum)
        result = {
            'clean_spectrum': clean_spectrum,
            'correlogram': correlogram,
            'uniform_series': uniform_series
        }
        return result

    def __restore_fap(self):
        """req 143 and 144 ref 2"""
        non_zeroes = np.extract(np.abs(self.__super_resultion_vector) != 0, self.__super_resultion_vector)
        freqs = np.extract(np.abs(self.__super_resultion_vector) != 0, self.__freq_vector)
        amplitudes = 2*np.abs(non_zeroes)
        phases = np.arctan2(np.imag(non_zeroes),np.real(non_zeroes))
        result = {
            'frequencies': freqs.reshape(-1,1),
            'amplitudes': amplitudes.reshape(-1,1),
            'phases': phases.reshape(-1,1)
        }
        return result

    def __build_clean_window_vector(self):
        """eq 157 ref 2"""
        clean_window_vector = mb.calculate_window_vector(
            self.__uniform_time_grid, self.__number_of_freq_estimations, self.__max_freq
        )
        return clean_window_vector

    def __build_uniform_time_grid(self, time_grid):
        """eq 158 ref 2"""
        step_size = (time_grid[-1][0] - time_grid[0][0])/(time_grid.shape[0] - 1)
        start = 0
        stop = step_size*time_grid.shape[0]
        result = np.arange(start,stop,step_size).reshape(-1,1)
        return result

    def __build_clean_spectrum(self):
        """eq 159 ref 2"""
        number_of_rows = self.__super_resultion_vector.shape[0]
        array = []
        for index in range(0, number_of_rows):
            max_index = index + 2*self.__number_of_freq_estimations
            min_index = max_index - 2*self.__number_of_freq_estimations
            subvector = self.__clean_window_vector[min_index:max_index+1]
            # subvector is flipped, because in eq 159 index of vector C (k) is substracted from index for vector S (j)
            array.append(np.matmul(self.__super_resultion_vector.T, np.flip(subvector, axis=0))[0][0])
        result = np.array(array).reshape(-1,1)
        return result

    def __build_correlogram(self, clean_spectrum):
        """eq 160 ref 2"""
        values = sch.squared_abs(clean_spectrum)
        result = self.__build_correlogram_or_uniform_series(values)
        return result

    def __build_uniform_series(self, clean_spectrum):
        """eq 161 ref 2"""
        result = self.__build_correlogram_or_uniform_series(clean_spectrum)
        return result

    def __build_correlogram_or_uniform_series(self, values):
        """eq 160 and 161 ref 2"""
        result = mb.run_ft(
            self.__uniform_time_grid, values, self.__freq_vector, self.__number_of_freq_estimations, 'inverse'
        )
        return result