import os
import logging.config

from dotenv import load_dotenv
from .logger import LoggerConfig
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initiate logger
logging.config.dictConfig(LoggerConfig.dictConfig)

# Load .env file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to root
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path, override=False)

# Create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Init SQLAlchemy and migrate
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)

if __name__ == '__main__':
    app.run()
