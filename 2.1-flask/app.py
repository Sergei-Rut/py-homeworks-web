from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRE_URI)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import views, models

