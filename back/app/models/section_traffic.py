"""
back.app.models.section_traffic

This module contains the model format of the traffic stats from a section.
"""

from back.app import db
from datetime import datetime
from back.app.models.json import JsonModel

class SectionTraffic(db.Model, JsonModel):
    """
    A module that contains the model format of the traffic stats from a section.
    
    Attributes
    ----------
    id : int
        id of the entry
    section : str
        section this entry is about
    hits : int
        hits per seconds calculated over last 10 sec
    average10 : int
        average of hits per second over last 10 mins
    average60 : int
        average of hits per second over last 60 mins
    unique_hosts : int
        number of different hosts calculated over last 10 mins
    total_bytes : int
        number of bytes transfered over last 10 mins
    availability : float
        availability over the last 10 mins
    codes_count : str
        status codes over the last 10 mins
    time : datetime
        time from the log for this batch of stats
    """
    
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(128), index=True)
    hits = db.Column(db.Integer, default=0) 
    average10 = db.Column(db.Integer, default=0) 
    average60 = db.Column(db.Integer, default=0) 
    unique_hosts = db.Column(db.Integer, default=0) 
    total_bytes = db.Column(db.Integer, default=0) 
    availability = db.Column(db.Float, default=0) 
    codes_count = db.Column(db.String(128), default='') 
    time = db.Column(db.DateTime, default=datetime.utcnow) 
    
    def __repr__(self):
        return '<SectionTraffic {}'.format(self.section)