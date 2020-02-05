from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from application.models import Exam, Question, Answer
from .forms import QuestionForm
from application import db
import pickle

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
    if request.method == 'POST':
        exam_payload = {}
        answer_ids = request.form.getlist('answer')
        question_ids = request.form.getlist('question')
        questions = Question.query.filter(Question.id.in_(question_ids)).all()
        for question in questions:
            exam_payload.update({question.id: {'question': question.question_title, 'answers': {}}})
            for answer in question.answers:
                exam_payload[question.id]['answers'].update(
                    {answer.id: {'answer': answer.answer_title, 'correct': answer.correct,
                                 'marked': str(answer.id) in answer_ids}})
        exam_payload = pickle.dumps(exam_payload)
        # Save exam to database
        exam = Exam(user_id=current_user.id, result_payload=exam_payload)
        db.session.add(exam)
        db.session.commit()
        return redirect(url_for('exam_bp.view_exam', id=exam.id))

    questions_dict = {}
    questions_model = Question()
    # Check if database has less then 20 questions
    if questions_model.count_records() < 20:
        flash('Exam fail to start, there is less then 20 questions.', 'danger')
        return redirect(url_for('exam_bp.exam_list'))
    for i in range(20):
        questions = questions_model.random_questions()
        # This needs to be optimized it can create a lot of query
        while questions_dict.get(questions.id) is not None:
            questions = questions_model.random_questions()
        questions_dict.update({questions.id: questions})
    return render_template('create_exam.html', questions=questions_dict)


@exam_bp.route('/<int:id>', methods=['GET'])
@login_required
def view_exam(id):
    exam = Exam.query.filter_by(id=id, user_id=current_user.get_id()).first_or_404()
    result_payload = pickle.loads(exam.result_payload)
    return render_template('view_exam.html', exam=exam, result_payload=result_payload)


@exam_bp.route('delete/<int:id>', methods=['GET'])
@login_required
def delete_exam(id):
    exam = Exam.query.filter_by(id=id, user_id=current_user.get_id()).first_or_404()
    db.session.delete(exam)
    db.session.commit()
    flash('Exam successfully deleted.', 'success')
    return redirect(url_for('exam_bp.exam_list'))


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
