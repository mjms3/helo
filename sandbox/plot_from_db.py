from collections import defaultdict

import matplotlib
matplotlib.use('TKAgg')

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://helo_db:helo_db@localhost/esp')
metadata = MetaData(bind=engine)

class Position_Data(Base):
    __table__ = Table('position_data', metadata, autoload=True)

session = create_session(bind=engine)

helicopter_ids = list(session.query(Position_Data.Id).distinct())

take_off_points = []
landing_points = []

def is_take_off_point(point, prev):
    return point.Spd > 20 and prev.Spd < 20

def is_landing_point(point, prev):
    return point.Spd <20 and prev.Spd > 20

for Id in helicopter_ids:
    position_data_points = list(session.query(Position_Data).filter_by(Id=Id[0]).all())
    previous_point = position_data_points[0]
    for point in position_data_points[1:]:
        if is_take_off_point(point,previous_point):
            take_off_points.append((point.Lat, point.Long))
        elif is_landing_point(point,previous_point):
            landing_points.append((point.Lat,point.Long))
        previous_point = point




m = Basemap(projection='merc',
            resolution='l',llcrnrlat=50,llcrnrlon=-6,
            urcrnrlat=59,urcrnrlon=2)
m.drawcoastlines()
take_off_coords =[m(float(p[1]),float(p[0])) for p in take_off_points]
landing_coords = [m(float(p[1]),float(p[0])) for p in landing_points]
m.scatter([c[0] for c in landing_coords], [c[1] for c in landing_coords],3,'b')
m.scatter([c[0] for c in take_off_coords], [c[1] for c in take_off_coords],3,'r')
plt.show()
input("")