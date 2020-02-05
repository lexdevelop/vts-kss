import random
from application import app
from sqlalchemy.orm.collections import InstrumentedList


@app.template_filter('shuffle_answers')
def shuffle_answers(answers):
    """Shuffle answers keys."""
    answer_tmp = answers[:]
    random.shuffle(answer_tmp)
    results = InstrumentedList(answer_tmp)
    return results
