from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)

#  all other variable instances need to come after the app instance
bootstrap = Bootstrap(app)
app.config.from_object(Config)

from app import routes
