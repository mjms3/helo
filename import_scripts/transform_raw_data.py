from logging import getLogger

from data_utilities.data_access_layer import DataAccessLayer

log = getLogger('transform_raw_data')


def process_raw_data():
    dal = DataAccessLayer()

    RawData = dal.tbls['raw_data']
    Operator = dal.tbls['operator']
    Helicopter = dal.tbls['helicopter']
    PositionReading = dal.tbls['position_reading']

    # Get new operators
    operator_details = dal.session.query(RawData).outerjoin(Operator, Operator.c.operator_name == RawData.c.Op). \
        filter(Operator.c.operator_name == None). \
        group_by(RawData.c.Op, RawData.c.Cou).all()

    if operator_details:
        log.info('New operators found: %s', [op.Op for op in operator_details])
        dal.engine.execute(Operator.insert(),
                           [{'operator_name': op.Op,
                             'is_military': None,
                             'operator_country': op.Cou,
                             } for op in operator_details])
        dal.session.commit()
    else:
        log.info('No new operators found.')

    # Get new helicopters
    helicopter_details = dal.session.query(RawData, Operator). \
        outerjoin(Helicopter, Helicopter.c.helicopter_data_source_id == RawData.c.Id). \
        filter(Helicopter.c.helicopter_data_source_id == None). \
        join(Operator, Operator.c.operator_name == RawData.c.Op). \
        group_by(RawData.c.Id, RawData.c.Icao, RawData.c.Reg, RawData.c.Type, RawData.c.Mdl).all()

    if helicopter_details:
        log.info('New helicopters found: %s', [h.Icao for h in helicopter_details])
        dal.engine.execute(Helicopter.insert(),
                           [{'helicopter_data_source_id': h.Id,
                             'icao': h.Icao,
                             'registration': h.Reg,
                             'helicopter_type': h.Type,
                             'helicopter_model': h.Mdl,
                             'helicopter_operator_id': h.operator_id,
                             } for h in helicopter_details])
        dal.session.commit()
    else:
        log.info('No new helicopters found.')

    # Get new position readings
    position_readings = dal.session.query(RawData, Helicopter). \
        join(Helicopter, Helicopter.c.helicopter_data_source_id == RawData.c.Id).all()

    log.info('Inserting %s new position readings into the database', len(position_readings))
    dal.engine.execute(PositionReading.insert(),
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
