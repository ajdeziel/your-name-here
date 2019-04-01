import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

from db.db_models import Place
from db.db_utils import get_db_session


def trace_lineage(session, family_name):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    # Draw political boundaries
    world = gpd.read_file("shapes/ne_50m_admin_0_countries.shp")
    world.plot(ax=ax)

    cities_coords = session.query(Place.Lat, Place.Long)
    cities = gpd.GeoSeries([Point(lat, lng) for lat, lng in cities_coords])
    cities.plot(ax=ax, color='r')

    plt.show()


if __name__ == "__main__":
    session = get_db_session("../db/proj_data.db")
    trace_lineage(session, "Hartnell")
