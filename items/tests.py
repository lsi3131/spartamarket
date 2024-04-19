from django.test import TestCase


# Create your tests here.
class ItemTestCase(TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        self.assertEqual(1, 1)
