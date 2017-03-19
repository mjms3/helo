import datetime

from data_utilities.data_access_layer import DataAccessLayer

dal = DataAccessLayer()
PositionReading = dal.tbls['position_reading']


def position_reading_date_filter(date):
    return PositionReading.c.time_stamp.between(
        date.combine(date, datetime.time(0)),
        date.combine(date, datetime.time(23, 59, 59)))
