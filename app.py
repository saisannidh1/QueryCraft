# app.py

import streamlit as st
import pandas as pd
import sqlite3
from main import get_db_schema, get_sql_from_gemini

DB_PATH = "chinook.db"

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

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me a question about the Chinook music database."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            db_schema = get_db_schema(DB_PATH)
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
                result_df, error = execute_query(generated_sql, DB_PATH)
                
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