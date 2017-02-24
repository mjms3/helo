
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

_engine = create_engine('mysql://helo_db:helo_db@localhost/esp')
_Base = declarative_base(_engine)

class RawData(_Base):
    __tablename__ ='raw_data'
    position_data_id = sa.Column(sa.Integer, primary_key=True)
    Id = sa.Column(sa.Integer,nullable=False)
    Icao = sa.Column(sa.Text)
    Reg = sa.Column(sa.Text)
    Alt = sa.Column(sa.Integer)
    GAlt = sa.Column(sa.Integer)
    Call = sa.Column(sa.Text)
    CallSus = sa.Column(sa.Boolean)
    Lat = sa.Column(sa.Numeric(precision=9, scale=6))
    Long = sa.Column(sa.Numeric(precision=9, scale=6))
    Spd = sa.Column(sa.Numeric(precision=5, scale=1))
    Trak = sa.Column(sa.Numeric(precision=9, scale=6))
    Type = sa.Column(sa.Text)
    Mdl = sa.Column(sa.Text)
    Man = sa.Column(sa.Text)
    CNum = sa.Column(sa.Text)
    From = sa.Column(sa.Text)
    To = sa.Column(sa.Text)
    Op = sa.Column(sa.Text)
    OpCode = sa.Column(sa.Text)
    Mil = sa.Column(sa.Boolean)
    Cou = sa.Column(sa.Text)
    Gnd = sa.Column(sa.Boolean)
    TimeStamp = sa.Column(sa.DateTime,nullable=False)

    uq_position_data = sa.UniqueConstraint('Id','TimeStamp')

_metadata = _Base.metadata
_Session = sessionmaker(bind=_engine)
_session = _Session()


class DataAccessLayer(object):
    metadata = _metadata
    engine = _engine
    session = _session
    tbls = _metadata.tables