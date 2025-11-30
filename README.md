📧 Prompt-Driven Email Productivity Agent

An intelligent, prompt-driven web application built with Streamlit and Groq (Llama 3.1) that automates core email productivity tasks: categorization, action item extraction, summarization, and auto-drafting replies.

The agent's entire behavior is governed by user-editable prompts (the "Prompt Brain"), ensuring flexibility and compliance with user-defined rules.

<p align="center">
<!-- Placeholder for a future live demo badge -->
<a href="#">
<img src="https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge&logo=streamlit" alt="Live Demo">
</a>
</p>

✨ Features and Workflow

This application implements the three required phases of the assignment:

Phase 1: Ingestion & Prompt Configuration

Load Inbox: Loads a mock inbox from a local JSON file into the Streamlit state.

Prompt Brain: A dedicated sidebar panel where the user can view, edit, and save four core prompt templates:

Categorization Prompt

Action Item Extraction Prompt (Designed for JSON output)

Auto-Reply Draft Prompt

Summarization Prompt

Prompt-Driven Architecture: All LLM calls dynamically pull the latest saved prompt from the state, ensuring the agent's behavior changes instantly upon user modification.

Phase 2: Automated Processing

Pipeline Execution: On click, the agent iterates through all loaded emails.

LLM Processing: Each email is sent to the Groq LLM (Llama 3.1) using the user-defined prompts to perform:

Categorization: Tags the email (e.g., To-Do, Important).

Action Item Extraction: Extracts structured data (e.g., {task: "...", deadline: "..."}).

Data Persistence: Results are safely stored in the DataService state, ready for fast retrieval.

Phase 3: Interactive Agent Chat & Drafting

Email Agent Chat: A conversational interface for interacting with a selected email.

Structured Queries: Ask questions like "What tasks do I need to do?" (retrieves saved JSON) or "Summarize this email" (runs LLM with Summarization Prompt).

Draft Generation (Safety First): Ask the agent to "draft a reply." The agent generates the complete reply draft using the Auto-Reply Draft Prompt, but it never sends the email.

Draft Review: All drafts are stored and displayed in the "Generated Drafts" tab for user review and editing.

🛠 Tech Stack

Core Language: Python 3.9+

Web App Framework: Streamlit

Data Handling: Pandas, built-in Python json

AI/LLM: Groq SDK (using the high-speed Llama 3.1 model)

Environment: python-dotenv for secure API key management

📁 Project Structure

email-agent-project/
├── .env                  # Stores API keys (GROQ_API_KEY)
├── main_app.py           # Streamlit UI, controls flow, and handles state
├── requirements.txt      # List of all dependencies for Streamlit Cloud
├── assets/
│   ├── mock_inbox.json   # Mock email data (10-20 sample emails)
│   └── default_prompts.json # Default prompt strings
└── services/
    ├── llm_service.py    # Handles Groq API calls and model configuration
    ├── data_service.py   # Manages loading/saving prompts and storing processed data/drafts
    └── agent_logic.py    # Orchestrates the LLM pipelines and chat interactions


🚀 Installation & Setup

Clone the repository:

git clone your_repository_url
cd email-agent-project


Create a Virtual Environment (Recommended):

python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate # On Linux/macOS


Install dependencies:

pip install -r requirements.txt


(Note: The requirements.txt file should contain: streamlit, pandas, pydantic, python-dotenv, groq)

Configure API Key (Mandatory):

Obtain a free API key from GroqCloud.

Create a file named .env in the root of the project folder (email-agent-project/).

Add your key to the file:

# .env
GROQ_API_KEY="gsk_your_secret_key_here"


🎮 How to Use the Agent

Run the application:

streamlit run main_app.py
