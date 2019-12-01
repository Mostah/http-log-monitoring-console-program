"""
back.app.routes.general_traffic

This module contains the different services for the general traffic information table.
"""

from flask import jsonify, request, Blueprint

from .. import app, db
from ..models.general_traffic import GeneralTraffic
from ..utils import required_fields

general_traffic_blueprint = Blueprint('general-traffic', __name__)

@general_traffic_blueprint.route('/last', methods=['GET'])
def get_general_stats():
    """ Route that returns the last general information from the database
    
    Returns
    -------
    dict
        a dict containing the general information
    status code : int
        HTTP status code of the request
    """
    
    last_general_stats = GeneralTraffic.query\
        .order_by(GeneralTraffic.time.desc())\
        .limit(1)\
        .all()
    return jsonify([stats.as_dict() for stats in last_general_stats]), 200

@general_traffic_blueprint.route('/add', methods=['POST'])
@required_fields(['hits', 'minimum', 'average', 'maximum', 'unique_hosts', 'total_bytes', 'availability', 'time'])
def add_general_stats():
    """ Route that create new a entry for a general traffic information in database
       
    Parameters
    ----------
    hits : int
        hits per seconds calculated over last 10 sec
    minimum : int
        minimum hits per seconds encountered over the last 10 sec
    average : int
        average of hits per second over last 10 mins
    maximum : int
        maximum hits per seconds encountered over the last 10 sec
    unique_hosts : int
        number of different hosts calculated over last 10 mins
    total_bytes : int
        number of bytes transfered over last 10 mins
    availability : float
        availability over the last 10 mins
    time : datetime
        time from the log for this batch of stats
    
    Returns
    -------
    status code : int
        HTTP status code of the request
    """
    
    form = { c.name: request.form[c.name] for c in GeneralTraffic(
        ).__table__.columns if c.name in request.form }
    general_stats = GeneralTraffic(**form)
    db.session.add(general_stats)
    db.session.commit()
    return jsonify(msg='OK'), 200
