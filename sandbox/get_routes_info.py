import numpy as np

def great_circle_time(start,end):
    distance = great_circle_distance(end, start)
    elapsed_time = end.TimeStamp - start.TimeStamp
    return distance/elapsed_time.seconds*3600


def great_circle_distance(end, start):
    lat1 = float(start.Lat) * np.pi / 180
    lat2 = float(end.Lat) * np.pi / 180
    dLat = lat1 - lat2
    dLong = float(start.Long - end.Long) * np.pi / 180
    dAngle = 2 * np.arcsin(np.sqrt(np.sin(dLat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dLong / 2) ** 2))
    distance = 6400 * dAngle
    return distance



def get_route_details(route,m=None):
    route_points = route.position_data_routes_rel_collection
    start = route_points[0].position_data
    end = route_points[-1].position_data
    average_speed = sum(
        great_circle_time(s.position_data, e.position_data) for s, e in zip(route_points[:-1], route_points[1:])) / len(
        route_points)
    if m:
        m.drawgreatcircle(float(start.Long), float(start.Lat), float(end.Long), float(end.Lat), linewidth=2, color='b')
        pos_coords = [m(*p[::-1]) for p in [(float(p.position_data.Lat), float(p.position_data.Long)) for p in route_points]]
        m.scatter([c[0] for c in pos_coords], [c[1] for c in pos_coords], 3, 'k')
    return ('{:4f}'.format(start.Lat), '{:4f}'.format(start.Long), '{:4f}'.format(end.Lat), '{:4f}'.format(end.Long),
            (end.TimeStamp - start.TimeStamp).total_seconds()/60, len(route_points),
          great_circle_distance(start, end), average_speed, end.Op, end.Reg, end.Type)
