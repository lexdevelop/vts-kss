import unittest
from application.util.jinja_filters import shuffle_answers
from sqlalchemy.orm.collections import InstrumentedList


class TestJinjaFilters(unittest.TestCase):
    def test_shuffle(self):
        test_list = InstrumentedList([55, 6, 3, 100, 22, 18, 33, 10])
        result = shuffle_answers(test_list)
        self.assertIsInstance(result, InstrumentedList)
        self.assertNotEqual([55, 6, 3, 100, 22, 18, 33, 10], result)
