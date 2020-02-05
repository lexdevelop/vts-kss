from application import app
from application.config import TestConfig
from application import db

app.config.from_object(TestConfig)
