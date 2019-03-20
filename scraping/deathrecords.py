from db.db_models import DeathRecord
from utils.kml_reader import read_kml_placemarks
from scraping.utils import extract_name_fields, parse_age, parse_date


def scrape_death_records(kml_file):
    for ext_data, points in read_kml_placemarks(kml_file):
        # No real useful information in row without name - ignore!
        if "FullName" not in ext_data or type(ext_data["FullName"]) != str:
            continue

        name_first, name_middle, name_last = extract_name_fields(ext_data["FullName"].strip())

        # Try to parse date of death
        date_of_death = None
        if "DeathYYYYMMDD" in ext_data and ext_data["DeathYYYYMMDD"] is not None:
            date_of_death = parse_date(ext_data["DeathYYYYMMDD"])

            if date_of_death is None:
                print("WARN: Could not parse date string '%s'" % ext_data["DeathYYYYMMDD"])

        # Try to parse age at death (in years)
        age_at_death = None
        if "Age" in ext_data and ext_data["Age"] is not None:
            age_at_death = parse_age(ext_data["Age"])

        # Get birth city and country, if available
        birth_city = ext_data["BirthCity"] if "BirthCity" in ext_data else None
        birth_country = ext_data["BirthCountry"] if "BirthCountry" in ext_data else None
        place_of_death = ext_data["PlaceOfDeath"] if "PlaceOfDeath" in ext_data else None

        # Process polygon points and compute centroid
        poly_pts = set()
        for point in points:
            poly_pts.add((point.x, point.y))
        poly_pts_str = " ".join([str(x) + "," + str(y) for x, y in poly_pts])

        pts_x = list(map(lambda p: p[0], poly_pts))
        centroid_x = sum(pts_x) / len(pts_x)

        pts_y = list(map(lambda p: p[1], poly_pts))
        centroid_y = sum(pts_y) / len(pts_y)

        yield DeathRecord(
            FirstName=name_first,
            MiddleName=name_middle,
            LastName=name_last,
            DeathDate=date_of_death,
            DeathAge=age_at_death,
            BirthCity=birth_city,
            BirthCountry=birth_country,
            PlaceOfDeath=place_of_death,
            Block=ext_data["Block"],
            Road=ext_data["Road"],
            Row=ext_data["Row"],
            Side=ext_data["Side"],
            FullPlot=ext_data["FullPlot"],
            GraveSitePts=poly_pts_str,
            GraveSiteCentroid_X=centroid_x,
            GraveSiteCentroid_Y=centroid_y
        )