## 📧 Prompt-Driven Email Productivity Agent

An intelligent, prompt-driven web application built with Streamlit and Groq (Llama 3.1) that automates core email productivity tasks: categorization, action item extraction, summarization, and auto-drafting replies.
The agent's entire behavior is governed by user-editable prompts (the "Prompt Brain"), ensuring flexibility and compliance with user-defined rules.

<p align="center">
  <a href="https://email-appuctivity-agent-npkivcs3xe9b7qttazxawn.streamlit.app/">
    <img src="https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
</p>

### ✨ Features and Workflow

#### **Phase 1: Ingestion & Prompt Configuration**

* **Load Inbox:** Loads a mock inbox dataset from a local **JSON file** into the Streamlit application state.
* **Prompt Brain:** A dedicated **sidebar panel** for user interaction with the core LLM templates:
    * **View, Edit, and Save** four primary prompt templates:
        * **Categorization Prompt**
        * **Action Item Extraction Prompt** (Designed specifically for **JSON output**)
        * **Auto-Reply Draft Prompt**
        * **Summarization Prompt**
* **Prompt-Driven Architecture:** All LLM calls dynamically pull the **latest saved prompt** from the state. This enables the agent's behavior to change **instantly** upon user modification.

---

#### **Phase 2: Automated Processing**

* **Pipeline Execution:** On user click, the agent initiates a process to iterate through **all loaded emails**.
* **LLM Processing:** Each email is sent to the **Groq LLM (Llama 3.1)**, which performs multiple tasks using the user-defined prompts:
    * **Categorization:** Tags the email (e.g., *To-Do*, *Important*).
    * **Action Item Extraction:** Extracts structured data, such as `{"task": "...", "deadline": "..."}`.
* **Data Persistence:** All results from the LLM processing are safely stored in the **DataService state**, ensuring fast retrieval and consistency.

---

#### **Phase 3: Interactive Agent Chat & Drafting**

* **Email Agent Chat:** A conversational interface for interacting with a **selected email**.
* **Structured Queries:** The agent can handle specific, information-retrieval queries:
    * Queries like *"What tasks do I need to do?"* retrieve the **saved JSON** action items.
    * Queries like *"Summarize this email"* trigger an LLM call using the **Summarization Prompt**.
* **Draft Generation (Safety First):** When asked to *"draft a reply,"* the agent generates a complete reply using the **Auto-Reply Draft Prompt**, but **it never sends the email**.
* **Draft Review:** All generated drafts are stored and displayed in the **"Generated Drafts" tab** for user review and editing before they are sent.

---

### 🛠 Tech Stack
<pre>
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Core Language** | Python 3.9+ | Main development environment. |
| **Web App Framework** | Streamlit | Frontend interface and state management. |
| **Data Handling** | Pandas, Python `json` | Structuring, manipulation, and serialization of data. |
| **AI/LLM** | Groq SDK (Llama 3.1) | High-speed LLM processing for all agent tasks. |
| **Environment** | `python-dotenv` | Secure management of API keys and environment variables. |
</pre>
📁 Project Structure

<pre>
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
</pre>


🚀 Installation & Setup

Clone the repository:
<pre>
git clone your_repository_url
cd email-agent-project
</pre>



Create a Virtual Environment (Recommended):
<pre>
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate # On Linux/macOS
</pre>


Install dependencies:
<pre>
pip install -r requirements.txt
</pre>



(Note: The requirements.txt file should contain: streamlit, pandas, pydantic, python-dotenv, groq)

Configure API Key (Mandatory):

Obtain a free API key from GroqCloud.

Create a file named .env in the root of the project folder (email-agent-project/).

Add your key to the file:
<pre>
# .env
GROQ_API_KEY="gsk_your_secret_key_here"
</pre>pre>



🎮 How to Use the Agent

Run the application:
<pre>
streamlit run main_app.py
</pre>

