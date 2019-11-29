from flask import jsonify, request, Blueprint
from sqlalchemy import func

from back.app import app, db
from back.app.models.section_traffic import SectionTraffic
from back.app.utils import required_fields

section_traffic_blueprint = Blueprint('section-traffic', __name__)

@section_traffic_blueprint.route('/lasts', methods=['GET'])
def get_sections_stats():
    last_sections_stats = db.session.query(SectionTraffic, func.max(SectionTraffic.time))\
        .group_by(SectionTraffic.section)\
        .order_by(SectionTraffic.hits.desc())\
        .all()
    return jsonify([stats[0].as_dict() for stats in last_sections_stats]), 200

# TODO add time to required fields
@section_traffic_blueprint.route('/add', methods=['POST'])
@required_fields(['section','hits', 'average10', 'average60', 'unique_hosts', 'total_bytes', 'availability', 'codes_count'])
def add_section_stats():
    form = { c.name: request.form[c.name] for c in SectionTraffic(
        ).__table__.columns if c.name in request.form }
    section_stats = SectionTraffic(**form)
    db.session.add(section_stats)
    db.session.commit()
    return jsonify(msg='OK'), 200