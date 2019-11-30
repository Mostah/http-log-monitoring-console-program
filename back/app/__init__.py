"""
back.app

modules that contain the back application and the database
"""

from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instanciation of flask application and SQLAlchemy database
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .routes.section_traffic import section_traffic_blueprint
from .routes.general_traffic import general_traffic_blueprint
from .routes.alerts import alerts_blueprint

# Encapsulation of every part of our app into modules
app.register_blueprint(section_traffic_blueprint, url_prefix='/section-traffic')
app.register_blueprint(general_traffic_blueprint, url_prefix='/general-traffic')
app.register_blueprint(alerts_blueprint, url_prefix='/alerts')