import unittest
from unittest.mock import MagicMock, patch
from src.llm_handler import LLMHandler

class TestLLMHandler(unittest.TestCase):
    def setUp(self):
        self.handler = LLMHandler('fake-key')

    @patch('src.llm_handler.requests.post')
    def test_call_api_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Generated Text'}}]
        }
        mock_post.return_value = mock_response
        
        result = self.handler._call_api([{'role': 'user', 'content': 'test'}])
        self.assertEqual(result, 'Generated Text')

    @patch('src.llm_handler.requests.post')
    def test_call_api_failure(self, mock_post):
        mock_post.side_effect = Exception("Network Error")
        result = self.handler._call_api([])
        self.assertEqual(result, "Error calling LLM.")

    def test_analyze_codebase(self):
        with patch.object(self.handler, '_call_api', return_value="Analysis Result") as mock_call:
            result = self.handler.analyze_codebase({'file.py': 'content'})
            self.assertEqual(result, "Analysis Result")
            mock_call.assert_called_once()

    def test_generate_fix(self):
        with patch.object(self.handler, '_call_api', return_value="Fixed Code") as mock_call:
            result = self.handler.generate_fix("Fix the bug", "broken code")
            self.assertEqual(result, "Fixed Code")
            mock_call.assert_called_once()

if __name__ == '__main__':
    unittest.main()
