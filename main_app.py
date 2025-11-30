import streamlit as st
import pandas as pd
import json
# Assuming services files (data_service, agent_logic) are correctly placed
from services.data_service import DataService
from services.agent_logic import AgentLogic

# --- Initialization and State Management ---
if 'data_service' not in st.session_state:
    st.session_state.data_service = DataService()
    st.session_state.agent = AgentLogic(st.session_state.data_service)
    st.session_state.emails = []
    st.session_state.selected_email_id = None
    st.session_state.chat_history = {} # {email_id: [messages]}

st.set_page_config(layout="wide", page_title="Email Productivity Agent")

# --- Helper Functions ---
def get_email_display_list(emails):
    """Prepares email data for the table display, including processed info."""
    data = []
    for email in emails:
        processed = st.session_state.data_service.get_processed_data(email['id'])
        data.append({
            "ID": email['id'],
            "Sender": email['sender'].split('<')[0].strip(),
            "Subject": email['subject'],
            "Timestamp": email['timestamp'],
            # Show the category tag, or an error/unprocessed status
            "Category": processed.get('category', 'Error processing...'), 
        })
    return pd.DataFrame(data)

def display_selected_email(email):
    """Displays the full content of the selected email."""
    st.subheader(email['subject'])
    st.markdown(f"**From:** {email['sender']} | **Time:** {email['timestamp']}")
    st.divider()
    st.code(email['body'], language="text")

def get_selected_email():
    """Retrieves the currently selected email object from the state."""
    if st.session_state.selected_email_id is not None:
        return next((e for e in st.session_state.emails if e['id'] == st.session_state.selected_email_id), None)
    return None

# --- UI Components ---
def prompt_configuration_panel():
    """Phase 1: Panel to create, edit, and save prompts (Prompt Brain)."""
    st.sidebar.header("⚙️ Prompt Brain Configuration")
    prompts = st.session_state.data_service.get_prompts()
    
    st.sidebar.subheader("Categorization Prompt")
    cat_prompt = st.sidebar.text_area("Category (Text Output)", prompts.get("categorization"), height=100, key="cat_prompt")
    
    st.sidebar.subheader("Action Item Prompt")
    action_prompt = st.sidebar.text_area("Action Item (JSON Output)", prompts.get("action_item_extraction"), height=100, key="action_prompt")
    
    st.sidebar.subheader("Auto-Reply Draft Prompt")
    reply_prompt = st.sidebar.text_area("Auto-Reply", prompts.get("auto_reply_draft"), height=100, key="reply_prompt")
    
    st.sidebar.subheader("Summarization Prompt")
    sum_prompt = st.sidebar.text_area("Summarization", prompts.get("summarization"), height=100, key="sum_prompt")
    
    if st.sidebar.button("💾 Save All Prompts", use_container_width=True):
        st.session_state.data_service.save_prompts({
            "categorization": cat_prompt,
            "action_item_extraction": action_prompt,
            "auto_reply_draft": reply_prompt,
            "summarization": sum_prompt,
        })
        st.sidebar.success("Prompts Updated!")

def email_ingestion_panel():
    """Phase 1: Loading and Processing controls."""
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("📥 Load Mock Inbox", use_container_width=True):
            st.session_state.emails = st.session_state.data_service.load_mock_inbox()
            st.session_state.selected_email_id = None # Reset selection on new load
            st.success(f"Loaded {len(st.session_state.emails)} sample emails.")

    with col2:
        # Only show processing button if emails are loaded
        if st.session_state.emails:
            if st.button("🧠 Process Emails (Run LLM Agent)", use_container_width=True):
                with st.spinner("Running categorization and action extraction via LLM..."):
                    st.session_state.agent.run_ingestion_pipeline(st.session_state.emails)
                st.success("Processing Complete. Categories and Actions stored.")
                # Reload emails to update the table display with processed data
                st.session_state.emails = st.session_state.data_service.load_mock_inbox()

def inbox_viewer_tab():
    """Phase 1: Main table and selection logic."""
    if not st.session_state.emails:
        st.info("Click 'Load Mock Inbox' to begin.")
        return

    df = get_email_display_list(st.session_state.emails)
    
    # Allow selection of a row. The key is CRITICAL for st.session_state access.
    # The return value is ignored, as we rely on session state for selection data.
    st.dataframe( 
        df,
        selection_mode="single-row",
        use_container_width=True,
        hide_index=True,
        key="inbox_dataframe" 
    )

    # --- RELIABLE SELECTION LOGIC USING ST.SESSION_STATE ---
    
    # Access the selection details directly via the key defined in st.dataframe
    # Use .get() chaining to safely handle missing keys (no selection made yet)
    selection_details = st.session_state.get('inbox_dataframe', {}).get('selection', {})

    if selection_details and selection_details.get('rows'):
        selected_rows = selection_details['rows']
        
        if selected_rows:
            # Get the first selected row
            selected_row_data = selected_rows[0]
            
            # Retrieve the 'ID' we put into the DataFrame
            selected_id = selected_row_data.get('ID')
            
            if selected_id is not None:
                st.session_state.selected_email_id = selected_id
            
    elif st.session_state.emails and st.session_state.selected_email_id is None:
        # Default to the first email if none selected upon initial load
        st.session_state.selected_email_id = st.session_state.emails[0]['id']

def processed_data_viewer(email):
    """Displays processed LLM data (Category & Actions)."""
    st.subheader("🤖 Processed Data")
    data = st.session_state.data_service.get_processed_data(email['id'])

    col_cat, col_action = st.columns([1, 2])
    with col_cat:
        st.info(f"**Category:** {data['category']}")
    with col_action:
        # Safely display the action items as JSON
        try:
            st.json(json.loads(data['actions']))
        except json.JSONDecodeError:
            st.error("Action item extraction failed: Invalid JSON output from LLM or API key error.")
            st.code(data['actions']) # Show raw output for debugging

def agent_chat_and_draft_panel(email):
    """Phase 2 & 3: Chat interaction and drafting."""
    st.subheader("💬 Email Agent Chat & Draft")
    
    # Initialize chat history for this email
    if email['id'] not in st.session_state.chat_history:
        st.session_state.chat_history[email['id']] = []

    # Display chat history
    for message in st.session_state.chat_history[email['id']]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Chat Input
    prompt = st.chat_input("Ask the agent to summarize, list tasks, or draft a reply...", key=f"chat_input_{email['id']}")

    if prompt:
        # 1. Store user message
        st.session_state.chat_history[email['id']].append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)

        # 2. Get Agent response (using AgentLogic)
        with st.spinner("Agent is thinking..."):
            if "draft a reply" in prompt.lower() or "write a response" in prompt.lower():
                # Phase 3: Drafting
                draft_data = st.session_state.agent.draft_reply(email)
                response = f"Draft created successfully for '{draft_data['subject']}'! Please check the **Drafts** tab."
            else:
                # Phase 2: Ad-hoc Query
                response = st.session_state.agent.handle_chat_query(prompt, email)

        # 3. Store and display Agent message
        st.session_state.chat_history[email['id']].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

def drafts_tab():
    """Phase 3: Displays generated drafts."""
    drafts = st.session_state.data_service.get_drafts()
    st.header("📝 Drafts for Review (NEVER SENT)")
    
    if not drafts:
        st.info("No drafts have been generated yet. Use the 'Email Agent Chat' to generate one.")
        return
        
    for i, draft in enumerate(drafts):
        # Use an expander for clean display of multiple drafts
        with st.expander(f"Draft {i+1}: {draft['subject']}"):
            st.warning(f"Status: **{draft['status']}**", icon="🔒")
            st.markdown(f"**To:** `{draft['to']}`")
            st.markdown(f"**Subject:** `{draft['subject']}`")
            
            # Allow user to edit the draft body
            st.text_area("Body", draft['body'], height=250, key=f"draft_body_{i}")
            
            st.markdown(f"**Suggested Follow-up:** {draft.get('suggested_follow_ups', 'N/A')}")
            
            # Simple save button (saves to Streamlit state, not file in this mock)
            if st.button("Save Edits (To State)", key=f"save_draft_{i}"):
                st.success(f"Draft {i+1} saved locally to state.")

# --- Main Application Layout ---
prompt_configuration_panel()

st.title("📧 Prompt-Driven Email Productivity Agent")
st.markdown("---")

# Tabbed Interface
tab_inbox, tab_drafts = st.tabs(["Inbox & Agent", "Generated Drafts"])

with tab_inbox:
    email_ingestion_panel()
    st.markdown("---")
    
    col_list, col_details = st.columns([1, 1], gap="large")
    
    with col_list:
        st.subheader("📬 Inbox List")
        inbox_viewer_tab()
        
    with col_details:
        selected_email = get_selected_email()
        if selected_email:
            st.subheader("Email Details")
            display_selected_email(selected_email)
            
            # Display processed data below the email content
            with st.expander("Show Processed Data (Category & Actions)"):
                processed_data_viewer(selected_email)
            
            st.markdown("---")
            # The chat interface
            agent_chat_and_draft_panel(selected_email)
        else:
            st.info("Select an email from the list to view details and chat with the Agent.")

with tab_drafts:
    drafts_tab()