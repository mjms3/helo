import numpy as np

DEGREES_TO_RADIANS = np.pi / 180
RADIANS_TO_KNOTS = 6400  # Radius of the earth in Knots
SECONDS_TO_MINUTES = 1/60


def great_circle_time(start, end):
    distance = great_circle_distance(end, start)
    elapsed_time = end.TimeStamp - start.TimeStamp
    return distance / elapsed_time.seconds * 3600

def great_circle_distance_np(lat_and_long_array):
    lat = lat_and_long_array[:, 0]
    dLat = np.diff(lat) * DEGREES_TO_RADIANS
    long = lat_and_long_array[:, 1]
    dLong = np.diff(long) * DEGREES_TO_RADIANS
    dAngle = 2 * np.arcsin(np.sqrt(np.sin(dLat / 2) ** 2 + np.cos(lat[:-1]) * np.cos(lat[1:]) * np.sin(dLong / 2) ** 2))
    return RADIANS_TO_KNOTS*dAngle

def great_circle_distance(end, start):
    lat1 = float(start.Lat) * DEGREES_TO_RADIANS
    lat2 = float(end.Lat) * DEGREES_TO_RADIANS
    dLat = lat1 - lat2
    dLong = float(start.Long - end.Long) * DEGREES_TO_RADIANS
    dAngle = 2 * np.arcsin(np.sqrt(np.sin(dLat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dLong / 2) ** 2))
    distance = RADIANS_TO_KNOTS * dAngle
    return distance
