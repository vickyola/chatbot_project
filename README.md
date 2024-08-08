# Vicky's Chatbot README

## Introduction
Vicky's Chatbot is an interactive web application built using Streamlit, designed to create engaging conversations with users. The chatbot allows users to interact with three distinct characters: **Feind**, **Freund**, and **Fragefuchs**. Each character has a unique personality and responds differently based on the user's input. The chatbot is powered by the Ollama language model, specifically the `llama3` model, to generate conversational responses.

## Features
- **Three Unique Characters**:
  - **Feind**: A mean and sarcastic character that doesn't like the user.
  - **Freund**: A friendly and humorous character who always tries to make the user smile.
  - **Fragefuchs**: A clever character who answers questions with more questions to encourage deeper thinking.
  
- **Interactive Chat Interface**: Users can select a character and start a conversation. The chatbot responds based on the selected character's personality.

- **Chat History Management**: Users can clear the chat history through a sidebar button, resetting the conversation.

- **Customizable Language Model**: The chatbot uses the `Ollama` class from the `llama_index` library, allowing for easy switching of models if desired.

## Requirements
- Python 3.8+
- Streamlit
- llama_index
- Ollama language model (llama3 by default)

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install dependencies**:
    ```bash
    pip install streamlit llama-index
    ```

3. **Set up Ollama**:
   - Ensure that the Ollama model (`llama3`) is properly set up and accessible in your environment. You may need to configure API keys or other authentication methods depending on your setup.

## Usage

1. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

2. **Select a Character**: Choose one of the characters (Feind, Freund, or Fragefuchs) from the dropdown menu.

3. **Start Chatting**: Type your message in the chat input box and press Enter. The chatbot will respond based on the selected character's personality.

4. **Clear Chat History**: If you want to start a new conversation, use the "History Löschen!" button in the sidebar.

## Customization

### Switching Models
If you want to try a different model, such as `mistral:instruct`, modify the following line in the code:
llm = Ollama(model="mistral:instruct", request_timeout=400.0)


### Adding New Characters

To add new characters, update the following sections in the code:

    characters dictionary: Define the character's behavior.
    character_greetings dictionary: Set the initial greeting message.
    character_avatar dictionary: Choose an emoji or icon to represent the character.
    characters_labels dictionary: Provide a user-friendly label for the character.

## Credits

This project is inspired and partially refactored from a16z-infra/llama2-chatbot.
## License

This project is licensed under the MIT License. 
