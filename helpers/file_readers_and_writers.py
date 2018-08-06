import numpy as np
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
    return np.array(time_grid).reshape(-1,1), np.array(values).reshape(-1,1)

def save_series(series, file_path, flag):
    """save seriess to the file """
    length = series[0].shape[0]
    if flag != 'complex' and flag != 'real':
        raise ValueError("unknown flag")
    file = open(file_path, "w")
    for i in range(0, length):
        # time and value
        if flag == 'real':
            string = '%e %e' % (series[0][i][0], np.real(series[1][i][0]))
        elif flag == 'complex':
            string = '%e %e %ei' % (series[0][i][0], np.real(series[1][i][0]), np.imag(series[1][i][0]))
        else:
            raise ValueError("unknown flag")
        print(string, file=file)
    file.close