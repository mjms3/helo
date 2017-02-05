from textwrap import dedent

import matplotlib
from mpl_toolkits.basemap import Basemap

matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt

from sandbox.data_access_layer import DataAccessLayer


# and(.Long | .>-6 and . <2) and (.Lat | . >50 and . <59)
MIN_LONG = -6
MAX_LONG = 2
MIN_LAT = 50
MAX_LAT = 59

number_of_squares = 10

def longitude_mapper(long):
    return int((long-MIN_LONG)/(MAX_LONG-MIN_LONG)*number_of_squares)

def latitude_mapper(lat):
    return int((lat-MIN_LAT)/(MAX_LAT-MIN_LAT)*number_of_squares)

def linear_idx(int_lat,int_long):
    return int_lat + number_of_squares*int_long

def linear_idx_to_grid_square(lin_idx):
    lat_square = lin_idx % number_of_squares
    long_square = (lin_idx - lat_square) // number_of_squares
    return lat_square, long_square

def grid_square_to_coord(lat_square,long_square):
    return (MIN_LAT +(MAX_LAT-MIN_LAT)*lat_square/number_of_squares,
            MIN_LONG+(MAX_LONG-MIN_LONG)*long_square/number_of_squares)

def coord_from_linear_idx(lin_idx):
    return grid_square_to_coord(*linear_idx_to_grid_square(lin_idx))


if __name__ == '__main__':

    dal = DataAccessLayer()

    # Ignore S92 in the short term as it seems to do all the oil rig related stuff
    results=dal.engine.execute(dedent("""\
    select distinct h.helicopter_id from helicopters h join position_data pd on h.position_data_Id = pd.Id
    where pd.Type in ('R44','S76','A109','EC20','EC35','EC55','AS55')
    """))


    routes = dal.session.query(dal.tbls.routes).filter(dal.tbls.routes.helicopter_id.in_(r[0] for r in results))
    transition_matrix = np.zeros(2*(number_of_squares**2,))


    for route in routes:
        start_square = linear_idx(latitude_mapper(route.route_start_lat),
                                  longitude_mapper(route.route_start_long))
        end_square = linear_idx(latitude_mapper(route.route_end_lat),
                                longitude_mapper(route.route_end_long))
        print(route.route_start_lat,route.route_start_long)
        print(coord_from_linear_idx(start_square))
        transition_matrix[start_square,end_square] += 1

    m = Basemap(projection='merc',
            resolution='l',llcrnrlat=50,llcrnrlon=-6,
            urcrnrlat=59,urcrnrlon=2)
    m.drawcoastlines()

    max_count = np.max(transition_matrix)
    print('Max count: ', max_count)
    for idx in range(number_of_squares**2):
        for idy in range(number_of_squares**2):
            if transition_matrix[idx,idy]>0:
                start_point = coord_from_linear_idx(idx)
                end_point = coord_from_linear_idx(idy)
                m.drawgreatcircle(start_point[1],start_point[0],end_point[1],end_point[0],del_s=20,alpha=transition_matrix[idx,idy]/max_count,linewidth=2,color='b')
    plt.show()

    input('')