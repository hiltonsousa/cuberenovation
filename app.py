from flask import Flask
from routes import service_blueprint, ui_blueprint 
from calls import CubeScheduler, CubeCallManager

app = Flask(__name__)
app.register_blueprint(service_blueprint)
# the ui blueprint has only one entry for now...
app.register_blueprint(ui_blueprint)
app.config['scheduler'] = CubeScheduler(app)
app.config['callmanager'] = CubeCallManager()

if __name__ == "__main__":
    app.run(debug=True)