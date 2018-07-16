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