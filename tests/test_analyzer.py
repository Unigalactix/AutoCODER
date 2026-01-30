import unittest
from unittest.mock import MagicMock
from src.analyzer import analyze_repo

class TestAnalyzer(unittest.TestCase):
    def test_analyze_repo_basic(self):
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

    def test_analyze_repo_with_llm(self):
        mock_repo = MagicMock()
        mock_repo.language = 'Python'
        
        mock_file = MagicMock()
        mock_file.name = 'script.py'
        mock_file.decoded_content = b'print("hello")'
        
        mock_workflow = MagicMock()
        mock_workflow.name = 'ci.yml'

        # Mocking get_contents behavior
        # analyze_repo calls get_contents("") first (index 0)
        # then if workflows, it might call again.
        mock_repo.get_contents.side_effect = [
            [mock_file], # Root
            [mock_workflow] # Workflows
        ]

        mock_llm = MagicMock()
        mock_llm.analyze_codebase.return_value = "Code looks good."

        result = analyze_repo(mock_repo, llm_handler=mock_llm)
        
        self.assertIn("LLM Analysis:\nCode looks good.", result['vulnerabilities'])
        mock_llm.analyze_codebase.assert_called_once()

if __name__ == '__main__':
    unittest.main()
