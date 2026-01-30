import os
from jira import JIRA

class JiraHandler:
    def __init__(self, server, email, api_token):
        self.jira = JIRA(server=server, basic_auth=(email, api_token))

    def get_ticket_details(self, ticket_id):
        try:
            issue = self.jira.issue(ticket_id)
            return {
                'key': issue.key,
                'summary': issue.fields.summary,
                'description': issue.fields.description,
                'status': issue.fields.status.name
            }
        except Exception as e:
            print(f"Error fetching Jira ticket {ticket_id}: {e}")
            return None

    def post_comment(self, ticket_id, comment):
        try:
            self.jira.add_comment(ticket_id, comment)
            print(f"Comment posted to {ticket_id}")
            return True
        except Exception as e:
            print(f"Error posting comment to {ticket_id}: {e}")
            return False
