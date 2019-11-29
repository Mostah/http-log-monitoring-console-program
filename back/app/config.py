
"""
app.config

This module contains the constants to config the app.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Config module for the application.
    
    I'm taking the database URL from the DATABASE_URL environment variable, and if 
    that isn't defined, I'm configuring a database named app.db located in the main 
    directory of the application, which is stored in the basedir variable.
    
    For development purpose I'm going to use a SQLite database. SQLite databases are 
    the most convenient choice for developing small applications, as each database is 
    stored in a single file on disk and there is no need to run a database server 
    like MySQL and PostgreSQL.
    """
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   

    
