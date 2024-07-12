''' Sample test'''


from django.test import SimpleTestCase 
from .calc import add

class TestCalc(SimpleTestCase):
    def test_add_numbers(self):
        res = add(5,6)
        self.assertEqual(res,11)
