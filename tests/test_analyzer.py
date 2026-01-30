import unittest
from unittest.mock import MagicMock
from src.analyzer import analyze_repo

class TestAnalyzer(unittest.TestCase):
    def test_analyze_repo(self):
        mock_repo = MagicMock()
        mock_repo.language = 'Python'
        
        # Mocking root content
        mock_file = MagicMock()
        mock_file.name = 'password.txt'
        
        mock_workflow = MagicMock()
        mock_workflow.name = 'ci.yml'

        mock_repo.get_contents.side_effect = [
            [mock_file], # First call for root
            [mock_workflow]  # Second call for .github/workflows
        ]

        result = analyze_repo(mock_repo)
        
        self.assertEqual(result['language'], 'Python')
        self.assertIn("Suspicious file name found: password.txt", result['vulnerabilities'])
        self.assertIn("ci.yml", result['workflows'])

if __name__ == '__main__':
    unittest.main()
