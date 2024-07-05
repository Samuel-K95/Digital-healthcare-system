from django.test import TestCase
from patients import gemini


class GeminiBehaviorTests(TestCase):
    def test_gemini_new_request_handles_missing_genai(self):
        chat = gemini.Chat()
        resp = chat.gemini_new_request('I feel unwell')
        self.assertIsInstance(resp, str)
        self.assertIn('error', resp.lower())

    def test_serialize_deserialize_roundtrip(self):
        chat = gemini.Chat()
        chat.messages = [{'role':'user','parts':['hello']}]
        chat.response = 'ok'
        data = chat.serialize()
        self.assertIsInstance(data, str)
        new = gemini.Chat.deserialize(data)
        # messages should roundtrip
        self.assertEqual(new.messages, chat.messages)
