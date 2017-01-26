import json
import numpy as np
import matplotlib

matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

file_name_pattern = '../data/2016-06-20-{:02d}{:02d}Z.json'

MIN_LAT = 50
MAX_LAT = 59
MIN_LONG = -6
MAX_LONG = 2


def row_is_valid(data_dict):
    if not all(k in data_dict for k in ['Lat', 'Long', 'Spd']):
        return False

    if data_dict['Species'] != 4:
        return False

    return MIN_LAT < float(data_dict['Lat']) < MAX_LAT and MIN_LONG < float(data_dict['Long']) < MAX_LONG


uk_based_points = []
for i_hour in range(24):
    for i_min in range(60):
        file_name = file_name_pattern.format(i_hour, i_min)
        with open(file_name, 'r') as in_file:
            single_min_data = json.loads(in_file.read())

        aircraft_position_list = single_min_data['acList']

        uk_based_points.extend([p for p in aircraft_position_list if row_is_valid(p)])

num_points = len(uk_based_points)

pos_array = np.zeros((num_points, 3))

for i_point, point in enumerate(uk_based_points):
    pos_array[i_point, :] = [point['Lat'], point['Long'], point['Spd']]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.scatter(pos_array[:, 1], pos_array[:, 0], c=pos_array[:, 2])
fig.savefig('example_plot.png', dpi=300)
print(num_points)
