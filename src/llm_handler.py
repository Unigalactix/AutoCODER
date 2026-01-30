import requests
import json
import os

class LLMHandler:
    def __init__(self, api_key, model="z-ai/glm-4.5-air:free"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def _call_api(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": messages
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"LLM API Error: {e}")
            return "Error calling LLM."

    def analyze_codebase(self, file_data):
        """
        file_data: dict of {filename: content}
        """
        prompt = "Analyze the following code files for potential security vulnerabilities and suggest improvements:\n\n"
        for fname, content in file_data.items():
            prompt += f"--- {fname} ---\n{content}\n"
        
        messages = [{"role": "user", "content": prompt}]
        return self._call_api(messages)

    def generate_fix(self, issue_description, file_content):
        prompt = (
            f"Given the following code and issue description, provide a corrected version of the code.\n"
            f"Issue: {issue_description}\n\n"
            f"Current Code:\n{file_content}\n\n"
            f"Return ONLY the corrected code content, no markdown formatting if possible."
        )
        messages = [{"role": "user", "content": prompt}]
        return self._call_api(messages)
