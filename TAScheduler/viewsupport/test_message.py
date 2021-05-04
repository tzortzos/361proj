from django.test import TestCase, Client
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


class TestMessageQueue(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.sesion = self.client.session

        self.msg_text = 'This is a test message'

        self.reg_message = Message(self.msg_text)
        self.err_message = Message(self.msg_text, Message.Type.ERROR)

    def test_maps_serializable(self):
        pass

    def test_maps_deserializable(self):
        pass

    def test_pushes(self):
        pass

    def test_returns_pushed(self):
        pass

    def test_drain_all(self):
        pass

    def test_drain_fewer(self):
        pass

    def test_get_all(self):
        pass

    def test_set_directly(self):
        pass
