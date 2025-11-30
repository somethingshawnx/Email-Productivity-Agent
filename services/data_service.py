import json
import os
import pandas as pd

class DataService:
    def __init__(self):
        # File paths
        self.PROMPTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'default_prompts.json')
        self.INBOX_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'mock_inbox.json')
        
        # Internal storage for processed data and drafts
        self._processed_data = {}  # {email_id: {category, actions}}
        self._drafts = []

    # --- Prompt Configuration Methods ---
    def get_prompts(self):
        """Loads the current prompt configurations."""
        try:
            with open(self.PROMPTS_PATH, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "categorization": "Default Categorization Prompt.",
                "action_item_extraction": "Default Action Extraction Prompt.",
                "auto_reply_draft": "Default Auto-Reply Prompt.",
                "summarization": "Default Summarization Prompt."
            }

    def save_prompts(self, prompts: dict):
        """Saves updated prompts."""
        with open(self.PROMPTS_PATH, 'w') as f:
            json.dump(prompts, f, indent=4)
            
    # --- Inbox Methods ---
    def load_mock_inbox(self):
        """Loads the raw email data."""
        try:
            with open(self.INBOX_PATH, 'r') as f:
                emails = json.load(f)
                
                # Initialize processed data structure for new load
                for email in emails:
                    email['category'] = self._processed_data.get(email['id'], {}).get('category', 'Unprocessed')
                    email['actions'] = self._processed_data.get(email['id'], {}).get('actions', '[]')
                    
                return emails
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # --- Processed Data Methods ---
    def save_processed_data(self, email_id, category, actions):
        """Stores the LLM output for an email."""
        try:
            # Ensure actions is valid JSON string or handle it
            json.loads(actions) 
        except json.JSONDecodeError:
            actions = json.dumps([{"task": "Failed to extract due to LLM error", "deadline": "N/A"}])
        
        self._processed_data[email_id] = {
            "category": category,
            "actions": actions
        }
        
    def get_processed_data(self, email_id):
        """Retrieves processed data for a single email."""
        return self._processed_data.get(email_id, {"category": "Unprocessed", "actions": "[]"})

    # --- Draft Methods (Phase 3) ---
    def save_draft(self, draft_data: dict):
        """Saves a generated email draft."""
        self._drafts.append(draft_data)

    def get_drafts(self):
        """Returns all generated drafts."""
        return self._drafts