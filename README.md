# Chatbot with LangGraph and Streamlit

This project demonstrates a simple chatbot implemented using LangGraph for managing the conversation flow and Streamlit for the user interface.

## Overview

The chatbot uses a Google Gemini model to generate responses to user input. It leverages LangGraph to maintain the conversation state and an in-memory checkpointer to store message history. Streamlit provides an easy-to-use interface for interacting with the chatbot.

## Key Components

*   `backend.py`: Defines the LangGraph workflow, including the chatbot logic, graph structure, and checkpointer configuration.
*   `frontend.py`: Implements the Streamlit user interface for the chatbot.

## Prerequisites

*   Python 3.10
*   Pip
*   API keys for Google Gemini (set as environment variables)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Linux/macOS
    venv\Scripts\activate.bat  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Set the environment variables:

    *   `GOOGLE_API_KEY`: Your Google Gemini API key.

## Usage

1.  Run the Streamlit app:

    ```bash
    streamlit run frontend.py
    ```

2.  Open the app in your browser (usually at `http://localhost:8501`).

3.  Start chatting with the bot!

## Code Structure

### `backend.py`

*   Imports necessary libraries: `langgraph`, `langchain`, `google-generativeai`, etc.
*   Defines the `CHATBOT` TypedDict to represent the state of the conversation.
*   Implements the `bot` function, which takes the current state and generates a response using the Google Gemini model.
*   Creates a LangGraph graph with a single node (`chat`) and edges connecting the start and end of the graph to the `chat` node.
*   Compiles the graph using an `InMemorySaver` for checkpointing.
*   Defines a `configuration` dictionary containing the `thread_id` for the conversation.

### `frontend.py`

*   Imports `streamlit`, `langchain`, and the `workflow` and `configuration` from `backend.py`.
*   Initializes the message history in Streamlit's session state.
*   Displays the message history in the chat interface.
*   Gets user input from the chat input box.
*   Invokes the LangGraph workflow with the user input and the `configuration` dictionary.
*   Appends the user and bot messages to the message history and displays them in the chat interface.

## Notes

*   The `InMemorySaver` is used for checkpointing in this example, which means the message history will be lost when the Streamlit app restarts. For a production application, you should use a persistent checkpointer like Redis or a database.
*   The `thread_id` in the `configuration` dictionary is used to uniquely identify each conversation. In this example, a single `thread_id` is used, which means all users will share the same conversation history. For a multi-user application, you should generate a unique `thread_id` for each user.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.
```

**To generate a `requirements.txt` file:**

```bash
pip freeze >requirements.txt