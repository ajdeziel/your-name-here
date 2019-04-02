import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import sys

from db.db_models import Person, Place
from db.db_utils import get_db_session


def trace_origin(session, family_name):
    """
    Trace path of all members of a respective family from place of birth to place of death.
    :param session: Database session configuration
    :param family_name: Specific family name in database
    :return: World map of family members' origins
    """
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    # Draw political boundaries
    world = gpd.read_file("shapes/ne_50m_admin_0_countries.shp")
    world.plot(ax=ax)

    # Retrieve birth place, death place from database specifying family name
    cities_birth_coords = session.query(Place.Lat, Place.Long).join(Person.PlaceOfBirth)\
        .filter(Person.LastName == family_name.upper())
    cities_death_coords = session.query(Place.Lat, Place.Long).join(Person.PlaceOfDeath)\
        .filter(Person.LastName == family_name.upper())

    cities_birth = [(lat, long) for lat, long in cities_birth_coords]
    cities_death = [(lat, long) for lat, long in cities_death_coords]

    cities_geo = zip(cities_birth, cities_death)

    # Map respective family member's place of birth to place of death
    cities = gpd.GeoSeries([LineString([(lat_b, long_b), (lat_d, long_d)])
                            for (lat_b, long_b), (lat_d, long_d) in cities_geo])

    cities.plot(ax=ax, color='black')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Please provide a family name.")
        sys.exit(-1)

    session = get_db_session("../db/proj_data.db")
    trace_origin(session, sys.argv[1])
