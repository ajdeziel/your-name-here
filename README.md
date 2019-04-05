# YourNameHere
#### _Making genealogy, simplified for all_.

This application was constructed as part of a course project for SENG 474 (Data Mining)
at the University of Victoria, during the months from January to April 2019.

## Authors
* AJ Po-Deziel (V00815622)
* Charlie Friend (V00816542)

## Documentation
Our full technical report is available for viewing on [Google Docs](https://docs.google.com/document/d/19MDuBIBiprdEkjVKmGyASPpxfbHw2RC0aF55ljVxJ8A/edit?usp=sharing).
It contains our methods surrounding the construction of this application, data mining methods
and techniques employed, as well as certain design decisions that we took.

## Running Our Code

This repository consists of several scripts to gather and cluster death records into a SQLite database. A pre-generated
version of the database is included (`proj_data.db`), but you can also generate one using `gen_db.py`.

If you're having trouble running any scripts in this repository, be sure the **root** of the project is in your PYTHONPATH.
```bash
$ export PYTHONPATH=$PYTHONPATH:`pwd`
```

**Notable Files**:
* `db/db_generator.py`: Adds all data from our input datasets into a SQLite database.
* `db/clustering.py`: Contains our core clustering algorithm for death records.
* `vis/grave_cluster_map.py`: Creates a visualization of the family clusters generated in `clustering.py`.
* `vis/trace_origin.py`: Creates a visualization of the birth and death places of a given family. This currently
uses the Hartnell family as an example, the code can be easily changed to view other families.
