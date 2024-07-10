from django.test import TestCase
from patients import gemini
from unittest.mock import patch, MagicMock
import json


class GeminiModuleTests(TestCase):
    def test_chat_fallback_when_no_genai(self):
        gemini._HAS_GENAI = False
        chat = gemini.Chat()
        res = chat.gemini_new_request('I feel sick')
        self.assertIn('error', res.lower())

    def test_chat_follow_up_fallback(self):
        gemini._HAS_GENAI = False
        chat = gemini.Chat()
        chat.messages = [{'role': 'user', 'parts': ['x']}]
        chat.response = 'prior'
        res = chat.gemini_request('again')
        self.assertIn('error', res.lower())

    def test_serialize_and_deserialize(self):
        chat = gemini.Chat()
        chat.messages = [{'role': 'user', 'parts': ['hello']}]
        chat.response = 'hi there'
        data = chat.serialize()
        restored = gemini.Chat.deserialize(data)
        self.assertEqual(restored.messages, chat.messages)

    @patch('patients.gemini.genai')
    def test_gemini_new_request_success(self, mock_genai):
        gemini._HAS_GENAI = True
        model = MagicMock()
        model.generate_content.return_value = MagicMock(text='Advice: rest')
        mock_genai.GenerativeModel.return_value = model
        chat = gemini.Chat()
        result = chat.gemini_new_request('I have a headache')
        self.assertEqual(result, 'Advice: rest')
        self.assertEqual(len(chat.messages), 1)

    @patch('patients.gemini.genai')
    def test_gemini_request_success(self, mock_genai):
        gemini._HAS_GENAI = True
        model = MagicMock()
        model.generate_content.return_value = MagicMock(text='More advice')
        mock_genai.GenerativeModel.return_value = model
        chat = gemini.Chat()
        chat.messages = [{'role': 'user', 'parts': ['first']}]
        chat.response = 'first reply'
        result = chat.gemini_request('second question')
        self.assertEqual(result, 'More advice')
        self.assertEqual(len(chat.messages), 3)
