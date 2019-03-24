from flask import Flask, render_template, jsonify
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db_models import MarriageCert, DeathRecord

app = Flask(__name__)

# Create global SQLAlchemy DB Session
DBSession = sessionmaker()
db_engine = create_engine('sqlite:///./db/proj_data.db')  #TODO: Remember to swap over to PostgreSQL later!
DBSession.configure(bind=db_engine)
session = DBSession()


@app.route('/graves')
def get_graves():
    graves_coords = session.query(DeathRecord.GraveSiteCentroid_X, DeathRecord.GraveSiteCentroid_Y).all()

    # AWWWWWWWWWW YEAAAAAAAH (...sorry Cam)
    graves_coords_json = json.dumps([{"x": cx, "y": cy} for cx, cy in graves_coords])
    return jsonify(graves_coords_json)


@app.route('/')
def main():
    """
    When site is first requested, load the index home page.
    :return: Index HTML template
    """
    return render_template('index.html')

    # return render_template('index.html')


# TODO: To fix once we can get this to load on map load.
# @app.route('/', methods=['GET'])
# def retrieve_data():
#     """
#     Retrieve death records, marriage certificates from database upon loading of index page.
#     :return: No return value
#     """
#
#     dr = DeathRecord()
#     mc = MarriageCert()
#     graves_coords_query = session.query(dr.GraveSitePts).select_from(DeathRecord.__tablename__)
#     marriage_certs_query = session.query(mc).select_from(MarriageCert.__tablename__)
#
#     graves_coords = []
#     for row in graves_coords_query.all():
#         graves_coords_raw = row.split(' ')
#         for grave in graves_coords_raw:
#             plot_coords = list(map(float, grave.split(',')))
#             graves_coords.append(plot_coords)
#
#     return render_template('index.html', graves_coords=graves_coords)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
