"""
back.app.models.json

This module aims at converting models in a json format.
"""

class JsonModel(object):
    """
    This module aims at converting models in a json format.
    
    Methods
    -------
    as_dict()
        Convert a model that inherit from JsonModel in a json format
    """
    
    def as_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }