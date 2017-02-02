from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://helo_db:helo_db@localhost/esp')
metadata = MetaData(bind=engine)


class PositionData(Base):
    __table__ = Table('position_data', metadata, autoload=True)

class DataAbstractionLayer(object):


    session = create_session(bind=engine)