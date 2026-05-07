from flask import Flask
from app.routes import register_routes


def create_app():
    print("Creating app...")
    app = Flask(__name__)
    app.config["TESTING"] = True

    register_routes(app)

    return app
from flask import Flask
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True

    register_routes(app)
    return app