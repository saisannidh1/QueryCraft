# app.py

import streamlit as st
import pandas as pd
import sqlite3
from main import get_db_schema, get_sql_from_gemini

# --- App Configuration ---
DB_PATH = "chinook.db"

def execute_query(query: str, db_path: str):
    """Executes an SQL query and returns the result as a Pandas DataFrame."""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, f"Execution failed on sql '{query}': {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="QueryCraft 🤖", layout="centered")
st.title("🤖 QueryCraft: Conversational SQL Assistant")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me a question about the Chinook music database."}]

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# In app.py, replace the final block with this

if prompt := st.chat_input("What would you like to know?"):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # --- THIS IS THE CORRECTED LOGIC ---
            # Step 1: Get the database schema
            db_schema = get_db_schema(DB_PATH)
            
            # Step 2: Construct the full prompt including history
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
            full_prompt = f"""
            You are an expert SQL assistant. Given the conversation history and the database schema, write a concise, correct, and executable SQL query to answer the user's latest question.
            Only output the SQL query and nothing else.

            ### Database Schema:
            {db_schema}

            ### Conversation History:
            {history_str}
            """
            
            # Step 3: Call the function with only ONE argument
            generated_sql = get_sql_from_gemini(full_prompt)
            # --- END OF CORRECTION ---

            if generated_sql:
                st.code(generated_sql, language="sql")
                result_df, error = execute_query(generated_sql, DB_PATH)
                
                if error:
                    st.error(error)
                    assistant_response = {"role": "assistant", "content": f"I encountered an error: {error}"}
                elif result_df is not None:
                    if result_df.empty:
                        st.warning("Query executed successfully, but returned no data.")
                        assistant_response = {"role": "assistant", "content": "I ran the query, but it returned no results."}
                    else:
                        st.dataframe(result_df)
                        # Create a summary for the chat history instead of the full dataframe
                        summary = f"I found {len(result_df)} results. Displaying them above."
                        assistant_response = {"role": "assistant", "content": summary, "results": result_df}
                
                st.session_state.messages.append(assistant_response)

            else:
                st.error("I couldn't generate a SQL query. Please try rephrasing.")
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't generate a SQL query for that."})