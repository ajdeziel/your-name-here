import sys
from typing import List

from utils.distance import haversine
from db.db_utils import get_db_session
from db.db_models import Person, FamilyCluster

# Clusters have a maximum radius of 10 meters (roughly two/tree plots away).
CLUSTER_THRESHOLD = 10


def merge_clusters(c1: FamilyCluster, c2: FamilyCluster):
    num_people = c1.NumPeople + c2.NumPeople
    cx = (c1.Centroid_Long * c1.NumPeople + c2.Centroid_Long * c2.NumPeople) / num_people
    cy = (c1.Centroid_Lat * c1.NumPeople + c2.Centroid_Lat * c2.NumPeople) / num_people

    cluster = FamilyCluster(Centroid_Long=cx, Centroid_Lat=cy, NumPeople=num_people)
    cluster.people = c1.People.extend(c2.People)

    return cluster


def cluster_group(group: List[Person]):
    """Cluster a group of people by the geographic proximity of their grave sites.
    We say a group of people is "close" if they are within 2 plots of each other.
    """

    # Initialize a family cluster for each person
    clusters = []
    for person in group:
        cluster = FamilyCluster(
            Centroid_Long=person.DeathRecord.GraveSiteCentroid_Long,
            Centroid_Lat=person.DeathRecord.GraveSiteCentroid_Lat,
            NumPeople=1
        )

        clusters.append(cluster)
        person.FamilyCluster = cluster

    # Merge clusters until nearest cluster is below threshold
    while True:
        # If everything went into one cluster, we can break
        if len(clusters) == 1:
            break

        # Find closest pairs of clusters
        # O(n^3), I know, working on it.
        closest_distance = float("inf")
        c1, c2 = clusters[0], clusters[1]
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                distance = haversine(clusters[i].centroid(), clusters[j].centroid())
                if distance < closest_distance:
                    closest_distance = distance
                    c1, c2 = clusters[i], clusters[j]

        if closest_distance < 10:
            merged = merge_clusters(c1, c2)

            clusters.remove(c1)
            clusters.remove(c2)
            clusters.append(merged)
        else:
            break

    return clusters


def do_clustering(session):
    # Run clustering on individual last names
    for last_name, in session.query(Person.LastName).distinct():
        print("Clustering last name: %s" % last_name)

        # Find all records with same last name
        same_last_name = session.query(Person).filter(Person.LastName == last_name).all()
        print("\tFound %d people." % len(same_last_name))

        clusters = cluster_group(same_last_name)
        for person in same_last_name:
            session.merge(person)

        print("\tFound %d clusters" % len(clusters))


if __name__ == "__main__":
    session = get_db_session(sys.argv[1])
    do_clustering(session)
    session.commit()
