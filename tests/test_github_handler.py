import unittest
from unittest.mock import MagicMock, patch
from src.github_handler import GithubHandler

class TestGithubHandler(unittest.TestCase):
    def setUp(self):
        self.mock_github_lib = patch('src.github_handler.Github').start()
        self.handler = GithubHandler('token')

    def tearDown(self):
        patch.stopall()

    def test_verify_access_success(self):
        mock_repo = MagicMock()
        mock_repo.full_name = 'owner/repo'
        self.handler.g.get_repo.return_value = mock_repo
        
        result = self.handler.verify_access('owner/repo')
        self.assertEqual(result, mock_repo)

    def test_verify_access_failure(self):
        self.handler.g.get_repo.side_effect = Exception("Not Found")
        result = self.handler.verify_access('owner/repo')
        self.assertIsNone(result)

    def test_create_branch_success(self):
        mock_repo = MagicMock()
        mock_sb = MagicMock()
        mock_sb.commit.sha = 'sha123'
        mock_repo.get_branch.return_value = mock_sb
        
        result = self.handler.create_branch(mock_repo, 'new-branch')
        self.assertTrue(result)
        mock_repo.create_git_ref.assert_called_with(ref='refs/heads/new-branch', sha='sha123')

    def test_create_pull_request_success(self):
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_repo.create_pull.return_value = mock_pr
        
        result = self.handler.create_pull_request(mock_repo, 'head', 'Title', 'Body')
        self.assertEqual(result, mock_pr)

    def test_check_workflow_status(self):
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_pr.head.sha = 'sha123'
        mock_repo.get_pull.return_value = mock_pr
        
        mock_run = MagicMock()
        mock_run.name = 'Test Run'
        mock_run.status = 'completed'
        mock_run.conclusion = 'success'
        
        mock_repo.get_check_runs.return_value = [mock_run]
        
        # Patch time.sleep to speed up test
        with patch('time.sleep'):
            result = self.handler.check_workflow_status(mock_repo, 1)
        
        self.assertIn("Test Run: completed - success", result)

if __name__ == '__main__':
    unittest.main()
