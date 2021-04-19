import unittest
from TAScheduler.viewsupport.errors import PageError

class TestBasicErrors(unittest.TestCase):

    def setUp(self):
        self.error = PageError('This is the body of the error')

    def test_creates(self):
        self.assertEqual(self.error.body(), 'This is the body of the error', 'Does not return correct body')

    def test_no_headline(self):
        self.assertEqual(self.error.has_headline(), False, 'Does not correctly indicate no error')

    def test_get_headline_raises(self):
        with self.assertRaises(TypeError, msg='Did not raise correct exception in case where tried to access nonexistant headline'):
            self.error.headline()

class TestHeadlineErrors(unittest.TestCase):

    def setUp(self) -> None:
        self.error = PageError('This is the body of the error', 'Headline')

    def test_creates(self):
        self.assertEqual(self.error.body(), 'This is the body of the error', 'Did not return correct body')

    def test_has_headline(self):
        self.assertTrue(self.error.has_headline(), 'Did not indicate existence of headline correctly')

    def test_returns_headline(self):
        self.assertEqual(self.error.headline(), 'Headline', 'Did not return correct headline')

if __name__ == '__main__':
    unittest.main()
