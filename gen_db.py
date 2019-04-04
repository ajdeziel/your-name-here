"""
Generate a sqlite database containing all the data we used for this project.

This database can be used with several of our visualization scripts in the
vis/ folder.
    > python vis/grave_cluster_map.py proj_data.db
"""

import os
from db.db_utils import get_db_session
from db.db_generator import add_death_records, add_marriage_certs, find_places
from db.clustering import do_clustering, post_process

DB_FILE = "proj_data.db"


def gen_db():
    session = get_db_session(DB_FILE)

    print("# Add death records")
    add_death_records("data/Ross_Bay_Cemetery_Plot_Grid.kml", session)

    print("# Add marriage certificates")
    add_marriage_certs("data/marriage_certs.csv", session)

    print("# Run clustering")
    do_clustering(session)
    post_process(session)
    session.commit()

    # INTENTIONALLY COMMENTED OUT
    # Using find_places requires a google maps API key to geocode places of
    # birth and death. This information is included with the project database
    # in our submission .zip file.
    #
    if os.environ.get("GOOGLEMAPS_API_KEY"):
        print("# Find places")
        find_places(session)
    else:
        print("GOOGLEMAPS_API_KEY not defined. Not getting geocoding information!")


if __name__ == "__main__":
    gen_db()
