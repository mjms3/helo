from sandbox import MIN_LONG, MAX_LONG, MIN_LAT, MAX_LAT


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

if __name__=='__main__':
    import matplotlib
    from mpl_toolkits.basemap import Basemap

    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    from data_utilities.data_access_layer import DataAccessLayer

    dal = DataAccessLayer()

    routes = dal.session.query(dal.tbls.routes).all()
    start_lat = MIN_LAT
    start_long= MIN_LONG
    end_lat = MAX_LAT
    end_long = MAX_LONG
    MAP_BOUNDS = 0.5
    m = Basemap(projection='merc',
                resolution='l', llcrnrlat=min(start_lat, end_lat) - MAP_BOUNDS, llcrnrlon=min(start_long, end_long) - MAP_BOUNDS,
                urcrnrlat=max(start_lat, end_lat) + MAP_BOUNDS, urcrnrlon=max(start_long, end_long) + MAP_BOUNDS)

    m.drawcoastlines()
    for route in routes:
        get_route_details(route, m)
    plt.savefig('all_routes.png',dpi=300)
