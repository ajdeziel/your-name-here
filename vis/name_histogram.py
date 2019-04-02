import numpy as np
from sqlalchemy import func, desc
import matplotlib.pyplot as plt

from db.db_models import Person
from db.db_utils import get_db_session


def name_histogram(session):
    """Plot the distribution of the top 10 most popular lats names in our dataset."""

    data = session.query(Person.LastName, func.count(Person.LastName))\
        .group_by(Person.LastName)\
        .order_by(desc(func.count(Person.LastName)))\
        .limit(10).all()

    index = np.arange(10)
    labels = [x.LastName for x in data]

    values = [x[1] for x in data]

    plt.barh(index, values)
    plt.yticks(index, labels)
    plt.xticks()

    plt.title("Common Family Names in Ross Bay Cemetery Dataset")

    plt.show()


if __name__ == "__main__":
    session = get_db_session("../db/proj_data.db")
    name_histogram(session)
