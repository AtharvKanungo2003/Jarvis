# Orbit — Local AI Chatbot

A Streamlit chatbot powered by LangChain and Ollama. Chat with a locally running Qwen model through an animated web interface.

## Features

- Dark interface with animated elements
- Conversation history during the Streamlit session
- Optional typewriter animation
- New chat button to reset the conversation
- Type `bye` to end the conversation
- Custom prompt instructions for Hinglish responses
- Local inference through Ollama—no Hugging Face API token required

## Tech Stack

- Python
- Streamlit
- LangChain
- Ollama
- Qwen 2.5 Coder (`qwen2.5-coder:1.5b`)

## Setup

Install Python and [Ollama](https://ollama.com/download), then open a terminal in the project folder.

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install streamlit langchain-ollama langchain-core
```

### 3. Download the model

```powershell
ollama pull qwen2.5-coder:1.5b
```

Make sure Ollama is running. If needed, start it in a separate terminal:

```powershell
ollama serve
```

### 4. Start the chatbot

```powershell
python -m streamlit run chatbot_UI.py
```

Open the local URL displayed in your terminal.

## Usage

1. Enter a message in the chat box and press Enter.
2. Wait for the model to generate its response.
3. Toggle **Typing animation** to control the response display.
4. Click **New chat** to clear the conversation.
5. Type `bye` to end the conversation.

## How It Works

The application stores messages in Streamlit session state. Each question is formatted using a LangChain `PromptTemplate` and sent to `ChatOllama` with previous conversation messages.

The model generates a complete answer before the optional typewriter animation displays it. The animation is a visual effect, not live token streaming.

The custom prompt requests friendly greetings, Hinglish explanations, expanded abbreviations, and the closing phrase:

> ATHARV JI KI JAI HO

Model adherence to these instructions can vary. The fixed farewell triggered by `bye` bypasses the model and prompt template.

## Configuration

The default model configuration is:

```python
ChatOllama(
    model="qwen2.5-coder:1.5b",
    temperature=1.7,
)
```

To change models, download the desired model through Ollama and update the model name in the code.

Conversation history is held in session memory; the app does not save it to a database.

## Troubleshooting

- **Connection error:** Make sure Ollama is running.
- **Model not found:** Run `ollama list` and verify the model name.
- **Missing Python package:** Activate your virtual environment and install the dependencies.
- **Slow responses:** Generation speed depends on your hardware and conversation length.
- **Avatar error:** Use supported emoji avatars such as `🤖` and `👤`.

## Author

Atharv Kanungo