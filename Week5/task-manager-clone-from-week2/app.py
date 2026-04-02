from flask import Flask

from routes.v1_routes import v1
from routes.v2_routes import v2
from routes.v3_routes import v3


app = Flask(__name__)

app.register_blueprint(v1)
app.register_blueprint(v2)
app.register_blueprint(v3)


if __name__ == "__main__":
    app.run(debug=True)