# main.py

import os
import sqlite3
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# In main.py

def get_db_schema(db_path: str) -> str:
    """Reads the database schema and returns it as a formatted string, ignoring SQLite internal tables."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_str = ""
    for table in tables:
        table_name = table[0]
        if table_name.startswith("sqlite_"):
            continue
            
        schema_str += f"Table '{table_name}':\n"
        
        # --- THIS IS THE CORRECTED LINE ---
        # We wrap table_name in quotes to handle spaces
        cursor.execute(f'PRAGMA table_info("{table_name}");')
        
        columns = cursor.fetchall()
        
        for column in columns:
            schema_str += f"  - {column[1]} ({column[2]})\n"
        schema_str += "\n"
        
    conn.close()
    return schema_str

def get_sql_from_gemini(full_prompt: str, retries=3, delay=5) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    for attempt in range(retries):
        try:
            response = model.generate_content(full_prompt)
            cleaned_response = response.text.strip()
            return cleaned_response.replace("```sql", "").replace("```", "").strip()
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit hit. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"An unexpected error occurred: {e}")
                return None
    print("Failed to get a response after several retries.")
    return None