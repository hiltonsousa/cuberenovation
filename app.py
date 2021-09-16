from flask import Flask
from routes import cube_blueprint 
from calls import CubeRenovationScheculer

app = Flask(__name__)
app.register_blueprint(cube_blueprint)
app.config['scheduler'] = CubeRenovationScheculer()

if __name__ == "__main__":
    app.run(debug=True)