"""
back.app.models.general_traffic

This module contains the model format of the traffic stats over the whole website.
"""

from back.app import db
from datetime import datetime
from back.app.models.json import JsonModel

class GeneralTraffic(db.Model, JsonModel):
    """
    A module that contains the model format of the traffic stats over the whole website.
    
    Attributes
    ----------
    id : int
        id of the entry
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
    """
    
    
    id = db.Column(db.Integer, primary_key=True)
    hits = db.Column(db.Integer, default=0) 
    minimum = db.Column(db.Integer, default=0) 
    average = db.Column(db.Integer, default=0) 
    maximum = db.Column(db.Integer, default=0) 
    unique_hosts = db.Column(db.Integer, default=0)
    availability = db.Column(db.Float, default=0) 
    total_bytes = db.Column(db.Integer, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<GeneralTraffic {}'.format(self.time)