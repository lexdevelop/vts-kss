from flask import Blueprint, render_template

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/', methods=['GET'])
def home():
    """Homepage route."""
    return render_template('dashboard.html')