from sandbox.data_access_layer import DataAccessLayer
import logging

logging.basicConfig(filename='transform_raw_data.log',
                    level=logging.DEBUG)

_log = logging.getLogger()
dal = DataAccessLayer()

RawData = dal.tbls['raw_data']
Operators = dal.tbls['operators']
Helicopters = dal.tbls['helicopters']
PositionReadings = dal.tbls['position_readings']

# Get new operators
operator_details = dal.session.query(RawData).filter(RawData.c.Cou == 'United Kingdom'). \
    outerjoin(Operators, Operators.c.operator_name == RawData.c.Op). \
    filter(Operators.c.operator_name == None). \
    group_by(RawData.c.Op, RawData.c.Cou).all()

if operator_details:
    dal.engine.execute(Operators.insert(),
                       [{'operator_name': op.Op,
                         'is_military': None,
                         'operator_country': op.Cou,
                         } for op in operator_details])
    dal.session.commit()

# Get new helicopters
helicopter_details = dal.session.query(RawData, Operators). \
    outerjoin(Helicopters, Helicopters.c.helicopter_data_source_id == RawData.c.Id). \
    filter(Helicopters.c.helicopter_data_source_id == None). \
    join(Operators, Operators.c.operator_name == RawData.c.Op). \
    group_by(RawData.c.Id, RawData.c.Icao, RawData.c.Reg, RawData.c.Type, RawData.c.Mdl).all()

if helicopter_details:
    dal.engine.execute(Helicopters.insert(),
                       [{'helicopter_data_source_id': h.Id,
                         'icao': h.Icao,
                         'registration': h.Reg,
                         'helicopter_type': h.Type,
                         'helicopter_model': h.Mdl,
                         'helicopter_operator_id': h.operator_id,
                         } for h in helicopter_details])
    dal.session.commit()

# Get new position readings
position_readings = dal.session.query(RawData, Helicopters). \
    join(Helicopters, Helicopters.c.helicopter_data_source_id == RawData.c.Id).all()

dal.engine.execute(PositionReadings.insert(),
                   [{'helicopter_id': r.helicopter_id,
                     'latitude': r.Lat,
                     'longitude': r.Long,
                     'altitude': r.Alt,
                     'barometric_altitude': r.GAlt,
                     'speed': r.Spd,
                     'bearing': r.Trak,
                     'time_stamp': r.TimeStamp,
                     } for r in position_readings])
dal.session.commit()