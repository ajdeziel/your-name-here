"""
Color-coded map of family clusters in the database.
"""

import sys
import random
from db.db_models import Person, FamilyCluster
from db.db_utils import get_db_session

import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from shapely.geometry import Point


def show_clusters(session):
    num_records = session.query(Person).count()

    colour_map = plt.get_cmap("hsv")
    c_norm = colors.Normalize(vmin=0, vmax=10000)
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=colour_map)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    ross_bay_cemetery_map = gpd.read_file('./shapes/ross_bay_cemetery_plot_grid.dbf')
    ross_bay_cemetery_map.plot(ax=ax)

    num_plotted = 0
    for cluster in session.query(FamilyCluster):
        cluster_pts = []
        # x = np.ndarray(len(cluster.People))
        # y = np.ndarray(len(cluster.People))

        for i, person in enumerate(cluster.People):
            x = person.DeathRecord.GraveSiteCentroid_Long
            y = person.DeathRecord.GraveSiteCentroid_Lat
            # print(x[i], y[i])
            cluster_pts.append((y, x))

        if len(cluster.People) > 0:
            clusters = gpd.GeoSeries([Point(lat, long) for lat, long in cluster_pts])
            clusters.plot(ax=ax, color=scalar_map.to_rgba(random.randint(1, 10000)))
            num_plotted += 1

        # if len(cluster.People) > 0:
        #     plt.scatter(x, y, color=scalar_map.to_rgba(random.randint(1, 10000)))
        #     num_plotted += 1

        if num_plotted == 1000:
            break

    plt.show()


if __name__ == "__main__":
    session = get_db_session(sys.argv[1])
    show_clusters(session)
