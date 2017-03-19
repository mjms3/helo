from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

_engine = create_engine('mysql://helo_db:helo_db@localhost/esp')
_Base = declarative_base(_engine)


class RawData(_Base):
    __tablename__ = 'raw_data'
    raw_data_id = sa.Column(sa.Integer, primary_key=True)
    Id = sa.Column(sa.Integer, nullable=False)  # Id in source data set
    Icao = sa.Column(sa.Text)  # Icao (should be unique to Id)
    Reg = sa.Column(sa.Text)  # Reg (should be unique to Id)
    Alt = sa.Column(sa.Integer)  # Altitude
    GAlt = sa.Column(sa.Integer)  # Pressure adjusted altitude
    Call = sa.Column(sa.Text)  # Call sign (not unique, don't extract)
    CallSus = sa.Column(sa.Boolean)  # Is the call sign suspect?
    Lat = sa.Column(sa.Numeric(precision=9, scale=6))  # Latitude
    Long = sa.Column(sa.Numeric(precision=9, scale=6))  # Longitude
    Spd = sa.Column(sa.Numeric(precision=5, scale=1))  # Speed
    Trak = sa.Column(sa.Numeric(precision=9, scale=6))  # Bearing
    Type = sa.Column(sa.Text)  # Helicopter type
    Mdl = sa.Column(sa.Text)  # Helicopter Mdl (should be unique per Id)
    Man = sa.Column(sa.Text)  # Manufacturer (don't extract)
    CNum = sa.Column(sa.Text)  # Not sure. (Don't extract)
    From = sa.Column(sa.Text)  # Flight departure point (mainly not populated)
    To = sa.Column(sa.Text)  # Flight destination (mainly not populated)
    Op = sa.Column(sa.String(191))  # Helicopter operator
    OpCode = sa.Column(sa.Text)  # Not populated
    Mil = sa.Column(sa.Boolean)  # Is military
    Cou = sa.Column(sa.Text)  # Country of operator
    Gnd = sa.Column(sa.Boolean)  # On the ground ?
    TimeStamp = sa.Column(sa.DateTime, nullable=False)  # Timestamp of data point

    uq_raw_data = sa.UniqueConstraint('Id', 'TimeStamp')


class CanonicalOperator(_Base):
    __tablename__ = 'canonical_operator'
    canonical_operator_id = sa.Column(sa.Integer, primary_key=True)
    canonical_operator_name = sa.Column(sa.Text)


class Operator(_Base):
    __tablename__ = 'operator'
    operator_id = sa.Column(sa.Integer, primary_key=True)
    operator_name = sa.Column(sa.String(191))
    is_military = sa.Column(sa.Boolean)
    canonical_operator_id = sa.Column(sa.Integer, sa.ForeignKey('canonical_operator.canonical_operator_id'),
                                      nullable=True)
    operator_country = sa.Column(sa.String(191), default='United Kingdom')
    uq_operator_name_country = sa.UniqueConstraint('operator_name','operator_country')


class Helicopter(_Base):
    __tablename__ = 'helicopter'
    helicopter_id = sa.Column(sa.Integer, primary_key=True)
    helicopter_data_source_id = sa.Column(sa.Integer, nullable=False, unique=True)
    icao = sa.Column(sa.String(6), nullable=False, unique=True)
    registration = sa.Column(sa.String(10), nullable=False, unique=True)
    helicopter_type = sa.Column(sa.Text, nullable=False)
    helicopter_model = sa.Column(sa.Text, nullable=False)
    helicopter_operator_id = sa.Column(sa.Integer, sa.ForeignKey('operator.operator_id'), nullable=False)


class Route(_Base):
    __tablename__ = 'route'
    route_id = sa.Column(sa.Integer, primary_key=True)
    elapsed_time_min = sa.Column(sa.Integer, nullable=False)
    distance_travelled = sa.Column(sa.Numeric(precision=18, scale=8), nullable=False)


class PositionReading(_Base):
    __tablename__ = 'position_reading'
    position_reading_id = sa.Column(sa.Integer, primary_key=True)
    helicopter_id = sa.Column(sa.Integer, sa.ForeignKey('helicopter.helicopter_id'), nullable=False)
    latitude = sa.Column(sa.Numeric(precision=9, scale=6), nullable=False)
    longitude = sa.Column(sa.Numeric(precision=9, scale=6), nullable=False)
    altitude = sa.Column(sa.Integer, nullable=True)
    barometric_altitude = sa.Column(sa.Integer, nullable=True)
    speed = sa.Column(sa.Numeric(precision=5, scale=1), nullable=True)
    bearing = sa.Column(sa.Numeric(precision=9, scale=6), nullable=True)
    minutes_since_last_reading = sa.Column(sa.Integer, nullable=True)
    knots_moved_since_last_reading = sa.Column(sa.Numeric(precision=18, scale=8), nullable=True)
    route_id = sa.Column(sa.Integer, sa.ForeignKey('route.route_id'), nullable=True)
    time_stamp = sa.Column(sa.DateTime, nullable=False)
    calculated_speed = sa.Column(sa.Numeric(precision=18, scale=8), nullable=True)
    uq_position_reading_heli_time = sa.UniqueConstraint('helicopter_id', 'time_stamp')


_metadata = _Base.metadata
_Session = sessionmaker(bind=_engine)
_session = _Session()


class DataAccessLayer(object):
    metadata = _metadata
    engine = _engine
    session = _session
    tbls = _metadata.tables
