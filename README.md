
# QueryCraft 🤖: Conversational SQL Assistant

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)](https://ai.google.dev/)

**[Live Demo Link](https://querycraft-axecj58tb9tar6tzeqgmhe.streamlit.app/)**

QueryCraft is a smart SQL assistant that allows users to have a natural language conversation with their databases. Upload your own SQLite database or use the built-in Chinook music sample to get started. This project leverages Google's Gemini Pro to translate English questions into SQL queries, executes them, and displays the results in a user-friendly chat interface.

## Key Features

- **Natural Language to SQL:** Translates plain English questions into complex, executable SQL queries.
- **Dynamic Database Support:** Users can choose to interact with the built-in sample database or upload their own SQLite file for instant analysis.
- **Conversational Memory:** Remembers the context of the conversation to answer follow-up questions accurately.
- **Interactive UI:** A clean, chat-based interface built with Streamlit for a modern user experience.
- **Robust Query Generation:** The AI is prompted to handle complex schemas, including edge cases like spaces in table names.

## Tech Stack

- **AI Engine:** Google Gemini Pro (`gemini-1.5-flash-latest`)
- **Backend:** Python
- **Frontend:** Streamlit
- **Database:** SQLite
- **Deployment:** Docker, Streamlit Community Cloud

## How to Use

1.  Navigate to the **[Live Demo](https://your-deployed-streamlit-app-url.streamlit.app/)**.
2.  **To use the default database**, simply start typing your questions in the chat box.
3.  **To use your own database**, use the sidebar to upload your `.db`, `.sqlite`, or `.sqlite3` file. Once uploaded, you can begin asking questions about your own data.

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/querycraft.git](https://github.com/your-username/querycraft.git)
    cd querycraft
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your API key:
    ```
    GOOGLE_API_KEY="your-google-api-key"
    ```

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
