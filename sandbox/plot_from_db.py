import pandas as pd
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




def data_frame(query, columns):
    """
    Takes a sqlalchemy query and a list of columns, returns a dataframe.
    """
    def make_row(x):
        return dict([(c, getattr(x, c)) for c in columns])
    return pd.DataFrame([make_row(x) for x in query])

from sqlalchemy import inspect
import numpy as np
mapper = inspect(Position_Data)
cols = [c.key for c in mapper.attrs]


for Id in ((4222386,),):# helicopter_ids[1:2]:

    position_data_points = session.query(Position_Data).filter_by(Id=Id[0]).all()

    df = data_frame(position_data_points, cols)
    df['previous_position']
    print('foo')


m = Basemap(projection='merc',
            resolution='l',llcrnrlat=50,llcrnrlon=-6,
            urcrnrlat=59,urcrnrlon=2)
m.drawcoastlines()
take_off_coords =[m(float(p[1]),float(p[0])) for p in take_off_points]
landing_coords = [m(float(p[1]),float(p[0])) for p in landing_points]
pos_coords = [m(float(p.Long), float(p.Lat)) for p in position_data_points]
print(len(take_off_points),len(landing_points))

m.scatter([c[0] for c in pos_coords], [c[1] for c in pos_coords],1,'k')
m.scatter([c[0] for c in landing_coords], [c[1] for c in landing_coords],3,'b')
m.scatter([c[0] for c in take_off_coords], [c[1] for c in take_off_coords],3,'r')
plt.show()
input("")