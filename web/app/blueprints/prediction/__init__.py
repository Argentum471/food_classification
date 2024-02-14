from flask import Blueprint, request, render_template, current_app, Response
from app.blueprints.prediction.handlers.prediction_handler import html_response, json_response

prediction_blueprint = Blueprint('prediction_blueprint', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@prediction_blueprint.route("/submit", methods=['POST'])
def get_output():

    if request.content_type == "application/json":
        return json_response(request)

    else:
        prediction_struct = html_response(request=request, static_folder=current_app.static_folder)
        return render_template("index.html", prediction=prediction_struct.predict,
                               img_path=prediction_struct.img_path,
                               top_predictions=prediction_struct.top_predictions)



