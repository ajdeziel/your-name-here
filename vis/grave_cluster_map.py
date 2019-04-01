"""
Color-coded map of family clusters in the database.
"""

import sys
import random
from db.db_models import Person, FamilyCluster
from db.db_utils import get_db_session

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


def show_clusters(session):
    num_records = session.query(Person).count()

    hot = plt.get_cmap("hot")
    cNorm = colors.Normalize(vmin=0, vmax=1000)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=hot)

    num_plotted = 0
    for cluster in session.query(FamilyCluster).all():
        x = np.ndarray(len(cluster.People))
        y = np.ndarray(len(cluster.People))

        for i, person in enumerate(cluster.People):
            x[i] = person.DeathRecord.GraveSiteCentroid_Long
            y[i] = person.DeathRecord.GraveSiteCentroid_Lat
            # print(x[i], y[i])

        if len(cluster.People) > 0:
            plt.scatter(x, y, color=scalarMap.to_rgba(random.randint(1, 1000)))
            num_plotted += 1

        if num_plotted == 1000:
            break

    plt.show()


if __name__ == "__main__":
    session = get_db_session(sys.argv[1])
    show_clusters(session)
