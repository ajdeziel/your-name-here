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

    @staticmethod
    def merge(c1, c2):
        c = GenerationCluster()



def trace_generations(session):
    for family_cluster in session.query(FamilyCluster).all():
        print("Finding generations for family cluster %d" % family_cluster.Id)

        clusters = [GenerationCluster(person) for person in family_cluster.People]
        while True:



if __name__ == "__main__":
    sessions = get_db_session(sys.argv[1])
    trace_generations(sessions)
