import datetime

import numpy as np
from sqlalchemy.sql.expression import bindparam, and_

from data_utilities.common_components import position_reading_date_filter
from data_utilities.data_access_layer import DataAccessLayer
from esp.distance_utils import SECONDS_TO_MINUTES, great_circle_distance_np, MINUTES_PER_HOUR

dal = DataAccessLayer()

PositionReading = dal.tbls['position_reading']
Helicopter = dal.tbls['helicopter']


def get_position_records_for_date(helicopter, date):
    position_records = dal.session.query(PositionReading).filter(PositionReading.c.helicopter_id == helicopter,
                                                                 position_reading_date_filter(date)).all()

    return position_records


def update_position_info(date):
    helicopter_ids = [r.helicopter_id for r in dal.session.query(Helicopter).all()]

    for helicopter_id in helicopter_ids:
        position_records = get_position_records_for_date(helicopter_id, date)
        if len(position_records)>1: #Ignore degenerate case of only having a single point in a day for a helicopter
            update_position_records(position_records)


def update_position_records(position_records):
    time_stamps = np.asarray([r.time_stamp.timestamp() for r in position_records])
    time_deltas_minutes = np.diff(time_stamps) * SECONDS_TO_MINUTES
    lat_and_longs = np.asarray([[r.latitude, r.longitude] for r in position_records], dtype=np.float64)
    pos_change = great_circle_distance_np(lat_and_longs)
    calc_speed = pos_change / time_deltas_minutes * MINUTES_PER_HOUR
    stmt = PositionReading.update().where(and_(PositionReading.c.helicopter_id == bindparam('_helicopter_id'),
                                               PositionReading.c.time_stamp == bindparam('_time_stamp'))).values(
        minutes_since_last_reading=bindparam('time_elapsed'),
        knots_moved_since_last_reading=bindparam('pos_change'),
        calculated_speed=bindparam('calc_speed'))
    dal.engine.execute(stmt, [{'_helicopter_id': r.helicopter_id,
                               '_time_stamp': r.time_stamp,
                               'time_elapsed': delta_t,
                               'pos_change': delta_x,
                               'calc_speed': speed,
                               } for r, delta_t, delta_x, speed in
                              zip(position_records[1:], time_deltas_minutes, pos_change, calc_speed)])
    dal.session.commit()

