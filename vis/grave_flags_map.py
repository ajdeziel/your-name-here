import sys
from db.db_models import Person, DeathRecord
from db.db_utils import get_db_session

import geopandas as gpd
from matplotlib.pyplot import show


def show_place_of_origin():
    # Create Ross Bay Cemetery plot grid from Victoria Open Data ArcGIS shapefile
    ross_bay_cemetery_plots = gpd.read_file('./shapes/ross_bay_cemetery_plot_grid.dbf')
    ross_bay_cemetery_plots.head()
    ross_bay_cemetery_plots.plot()

    # Retrieve ArcGIS OID, origin country of each interred person
    origin_records = session.query(DeathRecord.Arcgis_OID, DeathRecord.Person.BirthCountry) \
                     .filter(DeathRecord.Arcgis_OID != None).all()
    place_of_origin = [{"arcgis_oid": arcgis_oid, "place_of_origin": place_of_origin} for arcgis_oid, place_of_origin
                       in origin_records]

    flags = {}

    # Match each retrieved record to respective plot in ArcGIS map
    for plot in ross_bay_cemetery_plots.iterrows():
        for record in place_of_origin:
            plot_oid = record["arcgis_oid"]
            if plot["OBJECTID"] == plot_oid:
                flags[plot_oid] = record["place_of_origin"].replace(" ", "-")

    # for origin in flags.items():
    #     origin

    show()


if __name__ == '__main__':
    session = get_db_session(sys.argv[1])
    show_place_of_origin()
