"""
back.app.routes.alerts

This module contains the different services for the alerts table.
"""

from flask import jsonify, request, Blueprint

from back.app import app, db
from back.app.models.alerts import Alerts
from back.app.utils import required_fields

alerts_blueprint = Blueprint('alerts', __name__)

@alerts_blueprint.route('/history', methods=['GET'])
def get_alerts_history():
    """ Route that returns the last 20 alerts triggered from the different sections
    
    Returns
    -------
    list
        a list of alert in the format of dictionary
    status code : int
        HTTP status code of the request
    """
    
    alerts_history = Alerts.query\
        .order_by(Alerts.time.desc())\
        .limit(20)
    return jsonify([alert.as_dict() for alert in alerts_history]), 200

# TODO add time to required fields
@alerts_blueprint.route('/add', methods=['POST'])
@required_fields(['section', 'status', 'hits'])
def createAlerts():
    """ Route that create new a entry for an alert in database
    
    Parameters
    ----------
    section : str
        the section on which the alert has been triggered
    status : int
        status: 1 is High traffic, 0 is back to normal
    hits : int
        number of hits that triggered the alert
    time : datetime
        time when the alert was triggered
        
    Returns
    -------
    message
        message caracterizing the request
    status code
        HTTP status code of the request
    """
    
    form = { c.name: request.form[c.name] for c in Alerts(
        ).__table__.columns if c.name in request.form }
    alerts = Alerts(**form)
    db.session.add(alerts)
    db.session.commit()
    return jsonify(msg='OK'), 200