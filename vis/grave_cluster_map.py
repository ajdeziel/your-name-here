"""
Color-coded map of family clusters in the database.
"""

import sys
import random
from db.db_models import Person, FamilyCluster, DeathRecord
from db.db_utils import get_db_session

import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


def show_clusters(session):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    ross_bay_cemetery_map = gpd.read_file('./shapes/Ross_Bay_Cemetery_Plot_Grid_WGS84.shp')
    ross_bay_cemetery_map.plot(ax=ax)

    q = session.query(Person.LastName, Person.FamilyCluster_Id,
                DeathRecord.GraveSiteCentroid_Lat, DeathRecord.GraveSiteCentroid_Long)\
                .join(DeathRecord.Person)

    count = q.count()
    clusters_colors = {}  # cluster ID -> random color value

    data = []
    for lastname, cluster_id, gs_lat, gs_lng in q:
        if cluster_id not in clusters_colors:
            clusters_colors[cluster_id] = random.randint(0, count)

        data.append((lastname, cluster_id, clusters_colors[cluster_id], Point(gs_lng, gs_lat)))

    pts_df = gpd.GeoDataFrame(data, columns=["LastName", "ClusterId", "ColorId", "Geometry"], geometry="Geometry")
    pts_df.plot(ax=ax, column="ColorId", cmap="hsv")

    plt.show()


if __name__ == "__main__":
    session = get_db_session(sys.argv[1])
    show_clusters(session)
