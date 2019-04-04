from db.db_models import Person, Place
from scraping.deathrecords import scrape_death_records
from scraping.marriagecerts import scrape_marriagecerts_csv
from scraping.googlemaps_geocoding import geocode


def add_marriage_certs(csv_file, session):
    for cert in scrape_marriagecerts_csv(csv_file):
        session.merge(cert)

    session.commit()


def add_death_records(kml_file, session):
    for person, record in scrape_death_records(kml_file):
        existing_record = session.query(Person).filter(Person.FirstName == person.FirstName,
                                                       Person.LastName == person.LastName,
                                                       Person.DeathRecord.has(FullPlot=record.FullPlot))

        # We sometimes get duplicates from this dataset. If the record has the same
        # first name, last name and plot ID then we can safely ignore it.
        # TODO: merge these entries to get complete information!
        if session.query(existing_record.exists()).scalar():
            print("Ignoring duplicate record for '%s %s' at FullPlot '%s'"
                  % (person.FirstName, person.LastName, person.DeathRecord.FullPlot))
            continue

        session.merge(person)


def find_places(session):
    # Find all unique places where people were born and died
    places = set()

    birth_places = session.query(Person.PlaceOfBirth_Desc).distinct()
    for place, in birth_places:
        places.add(place)

    death_places = session.query(Person.PlaceOfDeath_Desc).distinct()
    for place, in death_places:
        places.add(place)

    places.remove(None)  # None should be ignored when geocoding places
    for place_name in places:
        print("Geocoding location: %s" % place_name)
        located_name, long, lat = geocode(place_name)
        if located_name:
            print("\t* %s (Long: %f, Lat: %f)" % (located_name, long, lat))

            place = Place(
                Name=located_name,
                Long=long,
                Lat=lat
            )

            # Update places of birth
            for person in session.query(Person).filter(Person.PlaceOfBirth_Desc == place_name):
                person.PlaceOfBirth = place

            # Update places of death
            for person in session.query(Person).filter(Person.PlaceOfDeath_Desc == place_name):
                person.PlaceOfDeath = place
        else:
            print("\t* Could not find location")
