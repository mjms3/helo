import numpy as np

DEGREES_TO_RADIANS = np.pi / 180
RADIANS_TO_KNOTS = 6400  # Radius of the earth in Knots
SECONDS_TO_MINUTES = 1/60
MINUTES_PER_HOUR = 60


def great_circle_time(start, end):
    distance = great_circle_distance(end, start)
    elapsed_time = end.TimeStamp - start.TimeStamp
    return distance / elapsed_time.seconds * 3600

def great_circle_distance_np(lat_and_long_array):
    lat = lat_and_long_array[:, 0]
    dLat = np.diff(lat) * DEGREES_TO_RADIANS
    long = lat_and_long_array[:, 1]
    dLong = np.diff(long) * DEGREES_TO_RADIANS
    lat1 = lat[:-1]
    lat2 = lat[1:]
    dAngle = distance_from_lat_and_long(dLat, dLong, lat1, lat2)
    return RADIANS_TO_KNOTS*dAngle


def distance_from_lat_and_long(dLat, dLong, lat1, lat2):
    return 2 * np.arcsin(np.sqrt(np.sin(dLat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dLong / 2) ** 2))


def great_circle_distance(start, end):
    lat1 = float(start.latitude) * DEGREES_TO_RADIANS
    lat2 = float(end.latitude) * DEGREES_TO_RADIANS
    dLat = lat1 - lat2
    dLong = float(start.longitude - end.longitude) * DEGREES_TO_RADIANS
    dAngle = distance_from_lat_and_long(dLat, dLong, lat1, lat2)
    return RADIANS_TO_KNOTS * dAngle
