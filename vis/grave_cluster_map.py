"""
Color-coded map of family clusters in the database.
"""

import sys
import random
import numpy as np
from db.db_models import Person, FamilyCluster, DeathRecord
from db.db_utils import get_db_session

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from shapely.geometry import Point


def show_clusters(session):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    ross_bay_cemetery_map = gpd.read_file('./shapes/Ross_Bay_Cemetery_Plot_Grid_WGS84.shp')
    ross_bay_cemetery_map.plot(ax=ax)

    q = session.query(Person.LastName, Person.FamilyCluster_Id,
                DeathRecord.GraveSiteCentroid_Lat, DeathRecord.GraveSiteCentroid_Long)\
                .join(DeathRecord.Person)

    i = 0
    count = q.count()
    x, y = np.zeros(count, dtype=np.float64), np.zeros(count, dtype=np.float64)
    # cmap = cmx.rainbow(np.linspace(0, count))
    for lastname, cluster_id, gs_lat, gs_lng in q:
        x[i] = gs_lng
        y[i] = gs_lat
        i += 1

    plt.scatter(x, y, color='red')

    plt.show()


if __name__ == "__main__":
    session = get_db_session(sys.argv[1])
    show_clusters(session)
