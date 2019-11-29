from flask import jsonify, request, Blueprint

from back.app import app, db
from back.app.models.alerts import Alerts
from back.app.utils import required_fields

alerts_blueprint = Blueprint('alerts', __name__)

@alerts_blueprint.route('/history', methods=['GET'])
def get_alerts_history():
    alerts_history = Alerts.query.limit(20)
    return jsonify([alert.as_dict() for alert in alerts_history]), 200

# TODO add time to required fields
@alerts_blueprint.route('/add', methods=['POST'])
@required_fields(['section', 'status', 'hits'])
def createAlerts():
    form = { c.name: request.form[c.name] for c in Alerts(
        ).__table__.columns if c.name in request.form }
    alerts = Alerts(**form)
    db.session.add(alerts)
    db.session.commit()
    return jsonify(msg='OK'), 200