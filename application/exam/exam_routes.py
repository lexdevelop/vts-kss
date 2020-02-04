from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from application.models import Exam, Question, Answer
from .forms import QuestionForm
from application import db

# Blueprint Configuration
exam_bp = Blueprint('exam_bp', __name__, url_prefix='/exam', template_folder='templates', static_folder='static')


@exam_bp.route('/', methods=['GET'])
@login_required
def exam_list():
    exams = Exam.query.filter_by(user_id=current_user.get_id()).all()
    return render_template('exam_list.html', exams=exams)


@exam_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_exam():
    return render_template('create_exam.html')


@exam_bp.route('/question', methods=['GET'])
@login_required
def question_list():
    questions = Question.query.all()
    return render_template('question_list.html', questions=questions)


@exam_bp.route('/question/new', methods=['GET', 'POST'])
@login_required
def create_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(question_title=form.question_title.data)
        db.session.add(question)
        for entry in form.answers.entries:
            answer = Answer(answer_title=entry.data['answer_title'], correct=entry.data['correct'], question=question)
            db.session.add(answer)
        db.session.commit()
        flash('Question successfully added.', 'success')
        return redirect(url_for('exam_bp.question_list'))
    return render_template('create_question.html', form=form)


@exam_bp.route('/question/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    question = Question.query.filter_by(id=id).first_or_404()
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        form.populate_obj(question)
        db.session.commit()
        flash('Question successfully edited.', 'success')
        return redirect(url_for('exam_bp.question_list'))
    return render_template('create_question.html', form=form)


@exam_bp.route('/question/delete/<int:id>', methods=['GET'])
@login_required
def delete_question(id):
    question = Question.query.filter_by(id=id).first_or_404()
    db.session.delete(question)
    db.session.commit()
    flash('Question successfully deleted.', 'success')
    return redirect(url_for('exam_bp.question_list'))
