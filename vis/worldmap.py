import geopandas as gpd
import matplotlib.pyplot as plt


def worldmap():
    map_df = gpd.read_file("shapes/ne_50m_land.shp")
    map_df.head()
    map_df.plot()
    plt.show()


if __name__ == "__main__":
    worldmap()
