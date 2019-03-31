from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session

from db.db_models import MarriageCert, DeathRecord

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/proj_data.db'
db = SQLAlchemy(app)

# Create global SQLAlchemy DB Session
# db_engine = create_engine('sqlite:///./db/proj_data.db')  #TODO: Remember to swap over to PostgreSQL later!
# DBSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))
# DBSession.configure(bind=db_engine)
# session = DBSession()


@app.route('/graves')
def get_graves():
    graves_coords = db.session.query(DeathRecord.GraveSiteCentroid_Long, DeathRecord.GraveSiteCentroid_Lat).all()

    # AWWWWWWWWWW YEAAAAAAAH (...sorry Cam)
    graves_coords_json = [{"latitude": g_lat, "longitude": g_long} for g_lat, g_long in graves_coords]
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
