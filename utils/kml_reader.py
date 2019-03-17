from fastkml import kml


def read_kml_placemarks(file_name):
    """Extract simpledata elements and polygon shapes from a KML tree.

    Why. WHY did XML processing have to return?

    :return Dictionary of SimpleData items, list of polygon points.
    """
    k = kml.KML()
    with open(file_name, 'r') as file:
        k.from_string(file.read())

    # Nesting hierarchy: Document -> Folder -> [ Placemark ... ]
    placemarks = next(next(k.features()).features()).features()
    for placemark in placemarks:
        # Ignore XML elements which are not placemarks
        if type(placemark) is not kml.Placemark:
            continue

        # Create dictionary of extended data
        simple_items = placemark.extended_data.elements[0].data
        extended_data = {x["name"]: x["value"] for x in simple_items}

        yield extended_data, placemark.geometry.exterior.geoms
