from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from awa.config import TestConfig

app = Flask(__name__)
app.config.from_object(TestConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blueprints
from awa.main.routes import main
from awa.iplan.routes import iplan
from awa.ibudget.routes import ibudget
app.register_blueprint(main)
app.register_blueprint(iplan)
app.register_blueprint(ibudget)

# models
from awa.iplan import models
