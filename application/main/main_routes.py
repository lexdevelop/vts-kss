from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from application.models import Question, Exam

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/', methods=['GET'])
@login_required
def home():
    """Dashboard route."""
    question_count = Question.query.count()
    exam_count = Exam.query.filter_by(user_id=current_user.id).count()
    return render_template('dashboard.html', question_count=question_count, exam_count=exam_count)


@main_bp.app_errorhandler(404)
def handle_404(e):
    return render_template('error_pages/404.html', request=request), 404


@main_bp.app_errorhandler(401)
def handle_401(e):
    return render_template('error_pages/401.html', request=request), 401


@main_bp.app_errorhandler(500)
def handle_500(e):
    return render_template('error_pages/500.html', request=request), 500
