from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from application.models import User
from .forms.register_form import RegisterForm
from application import db

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__, url_prefix='/user', template_folder='templates', static_folder='static')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered.', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template('register.html', form=form)
