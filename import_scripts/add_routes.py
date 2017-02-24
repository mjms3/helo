from datetime import datetime
from itertools import groupby
from operator import attrgetter

from sqlalchemy.sql.expression import and_

from data_utilities.common_components import position_reading_date_filter
from data_utilities.data_access_layer import DataAccessLayer, Routes
from esp.distance_utils import great_circle_distance

dal = DataAccessLayer()
PositionReadings = dal.tbls['position_readings']


def get_ordered_position_recordings_for_date(date):
    ordered_records = dal.session.query(PositionReadings).filter(position_reading_date_filter(date)).order_by(
        PositionReadings.c.helicopter_id,
        PositionReadings.c.time_stamp).all()
    return ordered_records


def get_number_of_position_records_for_date(date):
    return dal.session.query(PositionReadings).filter(position_reading_date_filter(date)).count()


def potential_new_route_condition(row):
    if row.minutes_since_last_reading is None or row.calculated_speed is None:
        return False
    if row.minutes_since_last_reading > 30 or row.calculated_speed < 1e-6:
        return True


def route_points_are_valid(route_records):
    if len(route_records) > 30 and great_circle_distance(route_records[0],
                                                         route_records[-1]) > 40:
        return True
    return False


def potential_new_route_marker(position_reading_row, route_count=[0]):
    if potential_new_route_condition(position_reading_row):
        return_value = route_count[0] = route_count[0] + 1
    else:
        return_value = route_count[0]
    return return_value


date = datetime(2016, 6, 20)
for helicopter_id, position_records in groupby(get_ordered_position_recordings_for_date(date),
                                               attrgetter('helicopter_id')):
    for local_route_id, route_records in groupby(position_records,
                                                 potential_new_route_marker):
        route_records_list = list(route_records)
        if route_points_are_valid(route_records_list):
            route = Routes(distance_travelled=sum(r.knots_moved_since_last_reading for r in route_records_list if r.knots_moved_since_last_reading is not None),
                           elapsed_time_min=sum(r.minutes_since_last_reading for r in route_records_list if r.minutes_since_last_reading is not None),
                           )
            dal.session.add(route)
            dal.session.commit()

            dal.engine.execute(PositionReadings.update().where(and_(PositionReadings.c.helicopter_id==helicopter_id,
                                                                  PositionReadings.c.time_stamp.between(route_records_list[0].time_stamp,
                                                                                                        route_records_list[-1].time_stamp))).values(route_id=route.route_id))
            dal.session.commit()
