from flask import Blueprint
from flask import render_template, url_for

index_blueprint = Blueprint('index', __name__, template_folder='templates')


@index_blueprint.route("/", methods=['GET'])
def main():
    return render_template("index.html")
