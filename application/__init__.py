import os
import logging.config

from dotenv import load_dotenv
from .logger import LoggerConfig
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.local import LocalProxy
from flask import current_app

# Initiate logger
logging.config.dictConfig(LoggerConfig.dictConfig)
logger = LocalProxy(lambda: current_app.logger)

# Load .env file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to root
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path, override=False)

# Create and configure the app
app = Flask(__name__)
app.config.from_object(Config)

# Init SQLAlchemy and migrate
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app=app, db=db)

# Init flask_login
login_manager = LoginManager(app=app)

# Import models so migration can detect changes
from application.models import *

# Register blueprints
with app.app_context():
    from .main import main_routes
    from .auth import auth_routes
    from .user import user_routes
    from .exam import exam_routes
    from .cli import cli_bp
    app.register_blueprint(main_routes.main_bp)
    app.register_blueprint(auth_routes.auth_bp)
    app.register_blueprint(user_routes.user_bp)
    app.register_blueprint(exam_routes.exam_bp)
    app.register_blueprint(cli_bp)

if __name__ == '__main__':
    app.run()
