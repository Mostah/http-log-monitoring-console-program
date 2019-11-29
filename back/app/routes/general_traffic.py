from flask import jsonify, request, Blueprint

from back.app import app, db
from back.app.models.general_traffic import GeneralTraffic
from back.app.utils import required_fields

general_traffic_blueprint = Blueprint('general-traffic', __name__)

@general_traffic_blueprint.route('/last', methods=['GET'])
def get_general_stats():
    last_general_stats = GeneralTraffic.query\
        .order_by(GeneralTraffic.time.desc())\
        .first_or_404()
    return jsonify(last_general_stats.as_dict()), 200

# TODO add time to required fields
@general_traffic_blueprint.route('/add', methods=['POST'])
@required_fields(['hits', 'minimum', 'average', 'maximum', 'unique_hosts', 'total_bytes', 'availability'])
def add_general_stats():
    form = { c.name: request.form[c.name] for c in GeneralTraffic(
        ).__table__.columns if c.name in request.form }
    general_stats = GeneralTraffic(**form)
    db.session.add(general_stats)
    db.session.commit()
    return jsonify(msg='OK'), 200
