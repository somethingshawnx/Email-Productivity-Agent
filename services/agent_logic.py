import json
from services.llm_service import LLMService
from services.data_service import DataService

class AgentLogic:
    def __init__(self, data_service: DataService):
        self.llm_service = LLMService()
        self.data_service = data_service
        
    def run_ingestion_pipeline(self, emails: list):
        """Phase 2: Automated Categorization and Action Item Extraction."""
        prompts = self.data_service.get_prompts()
        
        for email in emails:
            # 1. Categorization (Text Mode)
            category = self.llm_service.process_with_prompt(
                system_prompt=prompts['categorization'], 
                content=email['body']
            )
            
            # 2. Action Item Extraction (JSON Mode)
            actions_json_str = self.llm_service.process_with_prompt(
                system_prompt=prompts['action_item_extraction'], 
                content=email['body'],
                json_mode=True
            )
            
            # 3. Save results
            self.data_service.save_processed_data(
                email_id=email['id'], 
                category=category, 
                actions=actions_json_str
            )
        
    def handle_chat_query(self, query: str, email_content: dict):
        """Phase 2: Handles ad-hoc user queries on a selected email."""
        
        # --- Pre-defined/Structured Queries ---
        if "what tasks do i need to do" in query.lower():
            processed_data = self.data_service.get_processed_data(email_content['id'])
            actions = processed_data.get('actions', '[]')
            return f"**Extracted Tasks (from processing pipeline):**\n\n{actions}"

        if "summarize this email" in query.lower():
            # Use the dedicated summarization prompt
            prompts = self.data_service.get_prompts()
            summary_prompt = prompts['summarization']
            
            summary = self.llm_service.process_with_prompt(
                system_prompt=summary_prompt,
                content=email_content['body']
            )
            return f"**Summary:** {summary}"

        # --- General/Ad-hoc Queries ---
        else:
            # Fallback to general LLM query
            system_prompt = f"You are a helpful email assistant. Answer the user's question about the following email content: {query}"
            
            response = self.llm_service.process_with_prompt(
                system_prompt=system_prompt,
                content=email_content['body']
            )
            return response
        
    def draft_reply(self, email_content: dict):
        """Phase 3: Generates a reply draft using the Auto-Reply prompt."""
        prompts = self.data_service.get_prompts()
        draft_prompt = prompts['auto_reply_draft']
        
        # Combine the user prompt with the email content
        system_instruction = f"You are drafting an email reply. Follow this instruction: {draft_prompt}"
        
        draft_body = self.llm_service.process_with_prompt(
            system_prompt=system_instruction, 
            content=email_content['body']
        )
        
        # Generate a subject line
        subject_prefix = "RE: "
        if not email_content['subject'].startswith(subject_prefix):
             subject_prefix = "Draft: Re: "

        draft_data = {
            "from": "Agent (Drafted)",
            "to": email_content['sender'],
            "subject": f"{subject_prefix}{email_content['subject']}",
            "body": draft_body,
            "status": "DRAFT - NEVER SENT AUTOMATICALLY",
            "suggested_follow_ups": "Ensure an agenda is requested or provided."
        }
        
        # Store draft for user review
        self.data_service.save_draft(draft_data)
        return draft_data