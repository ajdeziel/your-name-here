"""
Convert shape files to the long/lat coordinate system (EPSG 4326)
"""

import sys
import geopandas as gpd


def convert(shapefile, outfile="out.shp"):
    # Read CRS WKT string from file (describes initial coordinate system)
    prj_path = shapefile.replace(".shp", ".prj")
    crs_wkt = open(prj_path).read()

    print("Reading...")
    map_df = gpd.read_file(shapefile, crs_wkt=crs_wkt)

    # Convert to long/lat coordinate system
    print("Converting...")
    df_converted = map_df.to_crs({"init": "epsg:4326"})

    print("Writing...")
    df_converted.to_file(outfile)


if __name__ == "__main__":
    convert(sys.argv[1])
