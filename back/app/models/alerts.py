"""
app.models.alerts

This module contains the model format for the alerts.
"""

from back.app import db
from datetime import datetime
from back.app.models.json import JsonModel

class Alerts(db.Model, JsonModel):
    """
    A module that contains the alert format use for anomalous traffic.
    
    Attributes
    ----------
    id : int
        id of the entry
    section : str
        section this entry is about
    status : int
        1 is for a high traffic, 0 is back to normal
    hits : int
        number of hits per second that triggered the alert
    time : datetime
        time from the log that triggered the alert
    """
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(128), index=True)
    status = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Alert {}'.format(self.website)