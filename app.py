# app.py

import streamlit as st
import pandas as pd
import sqlite3
import tempfile # <-- New import for handling temporary files
import os # <-- New import for file operations
from main import get_db_schema, get_sql_from_gemini

# --- App Configuration & Helper Functions ---
# (These functions remain the same)
def execute_query(query: str, db_path: str):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, f"Execution failed on sql '{query}': {e}"

st.set_page_config(page_title="QueryCraft 🤖", layout="centered")
st.title("🤖 QueryCraft: Conversational SQL Assistant")

# --- NEW: Sidebar for Database Selection ---
with st.sidebar:
    st.header("Database Configuration")
    uploaded_file = st.file_uploader(
        "Upload your SQLite database",
        type=["db", "sqlite", "sqlite3"]
    )

    # --- NEW: Logic to handle uploaded file vs. default ---
    if uploaded_file is not None:
        # Create a temporary file to store the uploaded DB
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            # Store the path to this temporary file in the session state
            st.session_state.db_path = tmp_file.name
        st.success("Database uploaded successfully! You can now ask questions.")
    else:
        # Use the default Chinook database if no file is uploaded
        st.session_state.db_path = "chinook.db"

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Upload your own SQLite database in the sidebar, or ask me a question about the default Chinook music database."}]

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# Get user input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Use the db_path from session state
            db_path = st.session_state.db_path
            db_schema = get_db_schema(db_path)
            
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
            
            full_prompt = f"""
            You are an expert SQL assistant. Given the conversation history and the database schema, write a SQL query to answer the user's latest question.
            Only output the SQL query.

            ### Database Schema:
            {db_schema}

            ### Conversation History:
            {history_str}
            """
            
            generated_sql = get_sql_from_gemini(full_prompt)

            if generated_sql:
                st.code(generated_sql, language="sql")
                result_df, error = execute_query(generated_sql, db_path)
                
                if error:
                    st.error(error)
                    assistant_response = {"role": "assistant", "content": f"I encountered an error: {error}"}
                elif result_df is not None:
                    st.dataframe(result_df)
                    summary = f"I found {len(result_df)} results."
                    assistant_response = {"role": "assistant", "content": summary, "results": result_df}
                st.session_state.messages.append(assistant_response)
            else:
                st.error("I couldn't generate a SQL query.")
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't generate a SQL query."})