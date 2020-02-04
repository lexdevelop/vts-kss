from flask_wtf import FlaskForm
from wtforms.fields import FormField, FieldList, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class AnswerForm(FlaskForm):
    answer_title = StringField('Answer', validators=[DataRequired()])
    correct = BooleanField('Correct')


class QuestionForm(FlaskForm):
    question_title = StringField('Question', validators=[DataRequired()])
    answers = FieldList(FormField(AnswerForm), min_entries=4, max_entries=4)
    submit = SubmitField('Save')

    def validate_answers(self, answers):
        correct = 0
        for answer in answers.data:
            if answer['correct']:
                correct += 1
        if correct == 0:
            raise ValidationError('At least one answer must be marked correct.')
