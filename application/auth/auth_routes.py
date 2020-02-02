from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from application.models import User, login_manager
from .forms.login_form import LoginForm

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth', template_folder='templates', static_folder='static')


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Please login first.', 'danger')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password combination.', 'danger')
            return redirect(url_for('auth_bp.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main_bp.home'))
    return render_template('login.html', form=form)


@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
