from helpers.common_imports import *
def read_file(file_path):
    """reads file with time series"""
    time_grid = [];
    values = []
    with open(file_path, 'r') as file:
        line = file.readline()
        while line:
            result = list(map(float, line.strip().split(' ')))
            time_grid.append(result[0])
            values.append(result[1])
            line = file.readline()
    result = {
        'time_grid': np.array(time_grid).reshape(-1,1),
        'values': np.array(values).reshape(-1,1)
    }
    return result

def save_series(time_grid, values, file_path, flag):
    """save series to the file """
    length = time_grid.shape[0]
    file = open(file_path, "w")
    for i in range(0, length):
        # time and value
        if flag == 'real':
            string = '%e %e' % (time_grid[i][0], np.real(values[i][0]))
        elif flag == 'complex':
            string = '%e %e %ei' % (time_grid[i][0], np.real(values[i][0]), np.imag(values[i][0]))
        elif flag == 'abs':
            string = '%e %e' % (time_grid[i][0], np.abs(values[i][0]))
        else:
            raise ValueError("unknown flag")
        print(string, file=file)
    file.close

def save_harmonics(freqs, amplitudes, phases, file_path):
    """save harmonics to the file """
    length = freqs.shape[0]
    file = open(file_path, "w")
    for i in range(0, length):
        # linear freq, amplitude, phase
        string = '%e %e %e' % (freqs[i][0], amplitudes[i][0], phases[i][0])
        print(string, file=file)
    file.close