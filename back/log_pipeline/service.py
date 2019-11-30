"""
back.log_pipeline.service

Module, last bloc of the pipeline, that makes a link to the database.
"""

from ..app import db
from ..app.models.general_traffic import GeneralTraffic
from ..app.models.section_traffic import SectionTraffic
from ..app.models.alerts import Alerts

class Service:
    
    @staticmethod
    def reset_database():
        GeneralTraffic.query.delete()
        SectionTraffic.query.delete()
        Alerts.query.delete()
        db.session.commit()
        
    @staticmethod
    def add_general_metrics(metrics):
        general_traffic = GeneralTraffic(**metrics.__dict__)
        db.session.add(general_traffic)
        db.session.commit()
        
    @staticmethod
    def add_sections_metrics(sections_metrics):
        for section, metrics in sections_metrics.items():
            section_traffic = SectionTraffic(**metrics.__dict__)
            db.session.add(section_traffic)
        db.session.commit()
        
    @staticmethod
    def send_alert(data):
        form = { c.name: data[c.name] for c in Alerts(
            ).__table__.columns if c.name in data }
        alerts = Alerts(**form)
        db.session.add(alerts)
        db.session.commit()