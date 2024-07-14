from flask import Blueprint, render_template
from ..domainmodel.model import Genre
import random

home_blueprint = Blueprint(
    'home_bp', __name__
)

@home_blueprint.route('/')
def home():
    pagetitle = "HomePage"

    return render_template('homePage.html', mytitle=pagetitle)
