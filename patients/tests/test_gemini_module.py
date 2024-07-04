from django.test import TestCase
from patients import gemini


class GeminiModuleTests(TestCase):
    def test_chat_fallback_when_no_genai(self):
        # Force the module to behave as if genai is unavailable
        gemini._HAS_GENAI = False
        chat = gemini.Chat()
        res = chat.gemini_new_request('I feel sick')
        self.assertIn('error', res.lower())
