from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
import flask
import os


APP_NAME = "Smart Flask Reverse Proxy"

app = flask.Flask(APP_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'


db = SQLAlchemy(app)


class File(db.Model):
    __tablename__ = "devices"
    uuid = Column(String, primary_key=True)
    agent = Column(String)
    ip = Column(String)


with app.app_context():
    db.create_all()


@app.before_first_request
def init():
    app.config["DB"] = db
    app.config["API_SECRET"] = os.environ["API_SECRET"]
    app.config["ACTIONS"] = {}
    app.config["INDEX"] = {}
    app.config["BACKEND"] = f"{os.environ['KEYCLOAK_PROTOCOL']}://{os.environ['KEYCLOAK_SERVER']}"
