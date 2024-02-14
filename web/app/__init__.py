
from flask import Flask

from app.blueprints.prediction import prediction_blueprint
from app.blueprints.index import index_blueprint


import warnings

warnings.filterwarnings("ignore")
food_app = Flask(__name__, static_url_path='/app/static', template_folder='templates', static_folder='static')
food_app.register_blueprint(prediction_blueprint, static_folder='static')
food_app.register_blueprint(index_blueprint)

