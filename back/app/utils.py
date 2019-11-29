"""
app._utils

This module provide usefull general functions for the app.
"""

from flask import request, jsonify
from functools import wraps

# Check fields decorator
def required_fields(fields):
    """ check if every required fields are provided in the request, 
    return code 400 if not.
    """
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            if not(all(k in request.form and request.form[k] is not None for k in fields)):
                message = "The following fields need to be provided: " + ", ".join(fields)
                return jsonify(msg=message), 400

            return f(*args, **kw)
        return wrapper
    return decorator