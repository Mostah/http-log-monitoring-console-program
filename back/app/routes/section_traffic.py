"""
back.app.routes.general_traffic

This module contains the different services for the sections traffic information table.
"""

from flask import jsonify, request, Blueprint
from sqlalchemy import func

from .. import app, db
from ..models.section_traffic import SectionTraffic
from ..utils import required_fields

section_traffic_blueprint = Blueprint('section-traffic', __name__)

@section_traffic_blueprint.route('/lasts', methods=['GET'])
def get_sections_stats():
    """ Route that returns the last stats from each section registered in the database
    
    Returns
    -------
    list
        list of dict containing the stats information of the section
    status code : int
        HTTP status code of the request
    """
    
    last_sections_stats = db.session.query(SectionTraffic, func.max(SectionTraffic.time))\
        .group_by(SectionTraffic.section)\
        .order_by(SectionTraffic.hits.desc())\
        .all()
    return jsonify([stats[0].as_dict() for stats in last_sections_stats]), 200

# TODO add time to required fields
@section_traffic_blueprint.route('/add', methods=['POST'])
@required_fields(['section','hits', 'average', 'unique_hosts', 'total_bytes', 'availability', 'error_codes_count'])
def add_section_stats():
    """ Route that create new a entry for a section traffic information in database
      
    Parameters
    ----------
    section : str
        section this entry is about
    hits : int
        hits per seconds calculated over the given timeframe
    average : int
        average of hits per second over the given timeframe
    unique_hosts : int
        number of different hosts calculated over the given timeframe
    total_bytes : int
        number of bytes transfered over the given timeframe
    availability : float
        availability over the given timeframe
    error_codes_count : str
        erros status codes ocount over the given timeframe
    time : datetime
        time from the log for this batch of stats

    Returns
    -------
    status code : int
        HTTP status code of the request
    """
    
    form = { c.name: request.form[c.name] for c in SectionTraffic(
        ).__table__.columns if c.name in request.form }
    section_stats = SectionTraffic(**form)
    db.session.add(section_stats)
    db.session.commit()
    return jsonify(msg='OK'), 200