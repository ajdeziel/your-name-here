import sys
from typing import List
from db.db_utils import get_db_session
from db.db_models import Person, FamilyCluster


class GenerationCluster:
    mean_year: int
    people: List[Person]

    def __init__(self, person: Person):
        self.people = [person]
        self.mean_year = person.EstBirthYear

    def merge(self, c2):
        self.mean_year = (self.mean_year * len(self.people)) + (c2.mean_year * len(c2.people)) \
                         / (len(self.people) + len(c2.people))
        self.people.extend(c2.people)


def trace_generations(session):
    for family_cluster in session.query(FamilyCluster).all():
        print("Finding generations for family cluster %d" % family_cluster.Id)

        # Cluster the family by GENERATION. Each generation cluster has a radius of 10 years.
        clusters = [GenerationCluster(person) for person in family_cluster.People
                    if person.EstBirthYear is not None]

        print("\t* Last names: %s" % ", ".join(set([person.LastName for person in family_cluster.People])))
        print("\t* Known birth years in cluster: %d" % len(clusters))
        while True:
            if len(clusters) <= 1:
                break

            # Find closest cluster
            best_distance = float("inf")
            c1, c2 = clusters[0], clusters[1]
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    dist = abs(clusters[i].mean_year - clusters[j].mean_year)
                    if dist < best_distance:
                        best_distance = dist
                        c1, c2 = clusters[i], clusters[j]

            # Cluster radius: 10 years
            if best_distance >= 10:
                break

            c1.merge(c2)
            clusters.remove(c2)

        clusters.sort(key=lambda x: x.mean_year)
        print("\t* Found %d generations" % len(clusters))
        gen_num = 0
        for cluster in clusters:
            for person in cluster.people:
                person.GenerationNumber = gen_num


if __name__ == "__main__":
    sessions = get_db_session(sys.argv[1])
    trace_generations(sessions)
