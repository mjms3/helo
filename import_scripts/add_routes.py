from collections import namedtuple
from datetime import timedelta

import numpy as np
import pandas as pd
from sqlalchemy import inspect

from data_utilities.data_access_layer import DataAccessLayer

dal = DataAccessLayer()


def data_frame(query, columns):
    """
    Takes a sqlalchemy query and a list of columns, returns a dataframe.
    """

    def make_row(x):
        return dict([(c, getattr(x, c)) for c in columns])

    return pd.DataFrame([make_row(x) for x in query])


mapper = inspect(Position_Data)
cols = [c.key for c in mapper.attrs]


class Route(object):
    def __init__(self):
        self.points = []
        self.position_data_points = []

    def get_starting_row(self):
        return self.points[0]

    def get_ending_row(self):
        return self.points[-1]

    def get_starting_coord(self):
        starting_row = self.get_starting_row()
        return (float(starting_row['Lat']), float(starting_row['Long']))

    def get_ending_coord(self):
        ending_row = self.get_ending_row()
        return (float(ending_row['Lat']), float(ending_row['Long']))

    def get_points(self):
        return [(float(p['Lat']), float(p['Long'])) for p in self.points]


def process_data_frame(df,query):
    routes = [Route()]
    current_route = routes[0]
    for (_, row), position_data in zip(df.iterrows(),query):
        if row['TimeStamp_diff'] > timedelta(minutes=30) or row['calculated_speed'] < 1e-1:
            routes.append(Route())
            current_route = routes[-1]
        if row['calculated_speed'] > 1e-1:
            current_route.points.append(row)
            current_route.position_data_points.append(position_data)
    return routes


def get_df_from_position_data(position_data_points):
    df = data_frame(position_data_points, cols)
    df['position_norm'] = df.apply(lambda row: float(np.sqrt(row['Lat'] ** 2 + row['Long'] ** 2)) * np.pi / 180, axis=1)
    df['TimeStamp_diff'] = df['TimeStamp'].diff()
    df['position_norm_diff'] = df['position_norm'].diff()
    df['calculated_speed'] = abs(df['position_norm_diff'] / df['TimeStamp_diff'].dt.total_seconds() * 6400 * 3600)
    return df

point_tuple = namedtuple('Point','Lat Long')

for helicopter in relevant_helicopters:
    Id = helicopter.position_data_Id
    position_data_points = list(dal.session.query(Position_Data).filter_by(Id=Id).all())
    df = get_df_from_position_data(position_data_points)
    route_list = process_data_frame(df,position_data_points)
    for r in route_list:
        if len(r.points) > 30:
            route_start_lat, route_start_long = r.get_starting_coord()
            route_end_lat, route_end_long = r.get_ending_coord()
            start = point_tuple(Lat=route_start_lat,Long=route_start_long)
            end = point_tuple(Lat=route_end_lat,Long=route_end_long)
            if great_circle_distance(end, start)>40:

                route = dal.tbls.routes(route_start_lat=route_start_lat,
                                        route_start_long=route_start_long,
                                        route_end_lat=route_end_lat,
                                        route_end_long=route_end_long,
                                        helicopter_id=helicopter.helicopter_id)
                dal.session.add(route)
                dal.session.commit()
                for point in r.position_data_points:
                    pdr_rel = dal.tbls.position_data_routes_rel(route_id=route.route_id,
                                                                position_data_id=point.position_data_id)
                    dal.session.add(pdr_rel)
            dal.session.commit()


