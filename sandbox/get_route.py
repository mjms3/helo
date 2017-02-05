import matplotlib
matplotlib.use('TkAgg')

from collections import namedtuple

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from sandbox.data_access_layer import DataAccessLayer
from sandbox.get_routes_info import get_route_details

dal = DataAccessLayer()
Routes = dal.tbls.routes

point = namedtuple('Point','Lat Long')

def get_route(start,end,m):
    start_lat = start.Lat
    start_long = start.Long
    end_lat = end.Lat
    end_long = end.Long
    TOLERANCE = 3e-1
    routes_filter = dal.session.query(Routes).filter(
        Routes.route_start_lat.between(start_lat - TOLERANCE, start_lat + TOLERANCE),
        Routes.route_start_long.between(start_long - TOLERANCE, start_long + TOLERANCE),
        Routes.route_end_lat.between(end_lat - TOLERANCE, end_lat + TOLERANCE),
        Routes.route_end_long.between(end_long - TOLERANCE, end_long + TOLERANCE),
    )
    candidate_routes = routes_filter.all()
    for route in candidate_routes:
        print(get_route_details(route, m))


start_lat =   51.055189
start_long = -0.952225
start_point = point(Lat=start_lat, Long=start_long)
end_lat = 51.746397
end_long = -1.571198
end_point = point(Lat=end_lat, Long=end_long)
MAP_BOUNDS = 1
m = Basemap(projection='merc',
            resolution='l', llcrnrlat=min(start_lat, end_lat) - MAP_BOUNDS, llcrnrlon=min(start_long, end_long) - MAP_BOUNDS,
            urcrnrlat=max(start_lat, end_lat) + MAP_BOUNDS, urcrnrlon=max(start_long, end_long) + MAP_BOUNDS)

m.drawcoastlines()
get_route(start_point,end_point,m)
plt.show()
input('')