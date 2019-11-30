"""
back.log_pipeline.service

Module, last bloc of the pipeline, that makes a link to the database.
"""

from ..app import db
from ..app.models.general_traffic import GeneralTraffic
from ..app.models.section_traffic import SectionTraffic
from ..app.models.alerts import Alerts

class Service:
    """
    Implement method to access the database of the application. On the present
    implementation, it access directly the db but could be change if the db was
    in another server.
    
    Methods
    -------
    reset_database()
        delete all entry of all the table of the db
    add_general_metrics()
        add a new entry in the general traffic database
    add_sections_metrics()
        add a new entry for every section in the section traffic database
    send_alert()
        add a new entry in the alert database
    """
    
    @staticmethod
    def reset_database():
        """delete all entry of all the table of the db
        """
        
        GeneralTraffic.query.delete()
        SectionTraffic.query.delete()
        Alerts.query.delete()
        db.session.commit()
        
    @staticmethod
    def add_general_metrics(metrics):
        """add a new entry in the general traffic database
        
        Parameters
        ----------
        metrics : GeneralMetrics
            object containing all the metrics for the new entry
        """
        
        general_traffic = GeneralTraffic(**metrics.__dict__)
        db.session.add(general_traffic)
        db.session.commit()
        
    @staticmethod
    def add_sections_metrics(sections_metrics):
        """add a new entry for every section in the section traffic database
        
        Parameters
        ----------
        metrics : list
            list containing all the SectionMetrics for the new entries
        """
        
        for section, metrics in sections_metrics.items():
            section_traffic = SectionTraffic(**metrics.__dict__)
            db.session.add(section_traffic)
        db.session.commit()
        
    @staticmethod
    def send_alert(data):
        """add a new entry in the alert database
        
        Parameters
        ----------
        data : dict
            dict containing all the information required for the new entry in alert database
        """
        
        form = { c.name: data[c.name] for c in Alerts(
            ).__table__.columns if c.name in data }
        alert = Alerts(**form)
        db.session.add(alert)
        db.session.commit()