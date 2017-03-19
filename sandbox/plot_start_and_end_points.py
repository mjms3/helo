from textwrap import dedent

import matplotlib
from matplotlib.colors import LogNorm

from data_utilities.data_access_layer import DataAccessLayer

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

dal = DataAccessLayer()
PositionReading = dal.tbls['position_reading']
Route = dal.tbls['route']

route_points = list(dal.engine.execute(dedent("""\
select latitude, longitude from
position_reading
where longitude between -6 and 2
and latitude between 50 and 59
""")))
all_coords = [(float(p.latitude), float(p.longitude)) for p in route_points]

n_frames = 200
n_skip = len(all_coords) // n_frames

MIN_X = 575
MAX_X = 1250
def convert_x(x):
    return MIN_X + (x+6)/8*(MAX_X-MIN_X)


MIN_Y = 0
MAX_Y = 1280
def convert_y(y):
    return MAX_Y - (y-50)/9*(MAX_Y-MIN_Y)

img_data = plt.imread('background.jpg')


plt.hist2d([convert_x(p[1]) for p in all_coords],[convert_y(p[0]) for p in all_coords],bins=50,alpha=0.5,norm=LogNorm(), zorder=2)
plt.imshow(img_data,zorder=1)
plt.xlim([MIN_X, MAX_X])
plt.axis('off')
plt.savefig('heatmap.png',dpi=300,bbox_inches='tight')


# for i_frame in range(n_frames):
    # coords = all_coords[i_frame * n_skip:n_skip * (i_frame + 1)]
    # plt.scatter([convert_x(p[1]) for p in coords],[convert_y(p[0]) for p in coords],alpha=0.3, s=0.05,c='r')
    #
    # plt.savefig('frame{}.png'.format(i_frame), dpi=300,bbox_inches='tight')
