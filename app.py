from flask import Flask
from routes import service_blueprint, ui_blueprint 
from calls import CubeScheduler, CubeCallManager

app = Flask(__name__)
app.register_blueprint(service_blueprint)
app.register_blueprint(ui_blueprint)
app.config['scheduler'] = CubeScheduler()
app.config['callmanager'] = CubeCallManager()

if __name__ == "__main__":
    app.run(debug=True)