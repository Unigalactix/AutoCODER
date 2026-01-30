import unittest
from unittest.mock import MagicMock, patch
from src.jira_handler import JiraHandler

class TestJiraHandler(unittest.TestCase):
    def setUp(self):
        self.mock_jira_lib = patch('src.jira_handler.JIRA').start()
        self.handler = JiraHandler('server', 'email', 'token')

    def tearDown(self):
        patch.stopall()

    def test_get_ticket_details_success(self):
        # Setup mock issue
        mock_issue = MagicMock()
        mock_issue.key = 'TEST-1'
        mock_issue.fields.summary = 'Test Summary'
        mock_issue.fields.description = 'Test Desc'
        mock_issue.fields.status.name = 'Open'
        
        self.handler.jira.issue.return_value = mock_issue

        result = self.handler.get_ticket_details('TEST-1')
        
        self.assertEqual(result['key'], 'TEST-1')
        self.assertEqual(result['summary'], 'Test Summary')
        self.handler.jira.issue.assert_called_with('TEST-1')

    def test_get_ticket_details_failure(self):
        self.handler.jira.issue.side_effect = Exception("API Error")
        result = self.handler.get_ticket_details('TEST-1')
        self.assertIsNone(result)

    def test_post_comment_success(self):
        result = self.handler.post_comment('TEST-1', 'Comment')
        self.assertTrue(result)
        self.handler.jira.add_comment.assert_called_with('TEST-1', 'Comment')

    def test_post_comment_failure(self):
        self.handler.jira.add_comment.side_effect = Exception("API Error")
        result = self.handler.post_comment('TEST-1', 'Comment')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
