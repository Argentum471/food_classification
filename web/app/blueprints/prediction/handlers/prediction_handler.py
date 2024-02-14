import os
import numpy as np
from flask import jsonify, abort
from app.classifier.src import classification_wrapper
from app.blueprints.prediction.structs.response import PredictResponse
import cv2
import base64


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


def json_response(request):
    input_json = request.get_json()
    image_base64 = input_json["sample"]
    image_data = base64.b64decode(image_base64)
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    top_predictions = classification_wrapper(image)
    top1_prediction = {
        "label": top_predictions[0][0],
        "probability": np.float64(top_predictions[0][1])
    }
    return jsonify(top1_prediction)


def html_response(request, static_folder):
    if 'sample' not in request.files:
        abort(415, description="No file part")

    file = request.files["sample"]

    if not allowed_file(file.filename):
        abort(415, description="Invalid file format. Please upload an image.")

    file_path = os.path.join(static_folder, file.filename)
    file.save(file_path)

    image = cv2.imread(file_path)
    top_predictions = classification_wrapper(image)
    prediction = True

    return PredictResponse(
        img_path=os.path.join('app/static', file.filename),
        predict=prediction,
        top_predictions=top_predictions
    )
