# 🤖 QueryCraft: Conversational SQL Assistant

**[Live Demo Link](https://your-deployed-streamlit-app-url.streamlit.app/)**

![QueryCraft Demo GIF](link-to-your-demo-gif-or-screenshot)

A conversational AI application that allows users to query a database using natural language. This project leverages Google's Gemini Pro to translate English questions into SQL queries, executes them, and displays the results in a user-friendly chat interface.

## Tech Stack

- **AI:** Google Gemini Pro
- **Backend:** Python
- **Frontend:** Streamlit
- **Database:** SQLite
- **Deployment:** Streamlit Community Cloud, Docker

## Features

- **Natural Language to SQL:** Translates plain English into complex SQL queries.
- **Conversational Memory:** Remembers the context of the conversation to answer follow-up questions.
- **Interactive UI:** A clean, chat-based interface built with Streamlit.
- **Real-time Query Execution:** Runs the generated SQL against the database and displays the results instantly.

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/querycraft.git](https://github.com/your-username/querycraft.git)
    cd querycraft
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file and add your API key:
    ```
    GOOGLE_API_KEY="your-google-api-key"
    ```

5.  **Run the app:**
    ```bash
    streamlit run app.py
    ```
