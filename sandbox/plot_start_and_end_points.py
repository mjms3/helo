import matplotlib
matplotlib.use('TkAgg')
from mpl_toolkits.basemap import Basemap

from data_utilities.data_access_layer import DataAccessLayer
import matplotlib.pyplot as plt

dal = DataAccessLayer()
Routes = dal.tbls.routes

route_list = dal.session.query(Routes).all()

m = Basemap(projection='merc',
        resolution='l',llcrnrlat=50,llcrnrlon=-6,
        urcrnrlat=59,urcrnrlon=2)
m.drawcoastlines()
take_off_coords =[m(float(r.route_start_long), float(r.route_start_lat)) for r in route_list]
landing_coords =[m(float(r.route_end_long), float(r.route_end_lat)) for r in route_list]
m.scatter([c[0] for c in landing_coords], [c[1] for c in landing_coords],5,'b')
m.scatter([c[0] for c in take_off_coords], [c[1] for c in take_off_coords],5,'r')
plt.show()
input('')