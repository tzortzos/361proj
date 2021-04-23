from django.test import TestCase
from TAScheduler.viewsupport.message import Message


class TestMessage(TestCase):
    def test_sets_message(self):
        m = 'This is a message to the user'
        message = Message(m)
        self.assertEqual(message.message(), m, 'Did not return correct message from object')

    def test_default_type(self):
        message = Message('message')
        self.assertTrue(message.type() is Message.Type.REGULAR, 'Did not default type correctly')

    def test_override_type(self):
        message = Message('m', Message.Type.ERROR)
        self.assertTrue(message.type() is Message.Type.ERROR, 'Did not override type correctly')


# TODO add tests for message queue in sessions