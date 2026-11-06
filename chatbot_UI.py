import time

import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate


st.set_page_config(
    page_title="Jarvis • Local AI",
    page_icon="🤖",
    layout="centered",
)

# -------------------- Styling --------------------

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(ellipse at top left, #252249 0%, transparent 50%),
            #0c101b;
        color: #eef2ff;
    }

    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {
        background: #0c101b;
    }

    .hero {
        padding: 28px 0 32px;
        animation: rise 0.7s ease-out;
    }

    .eyebrow {
        color: #a5b4fc;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 3px;
    }

    .hero h1 {
        color: #f8fafc;
        font-size: clamp(36px, 7vw, 54px);
        font-weight: 750;
        letter-spacing: -2px;
        margin: 12px 0;
    }

    .hero p {
        color: #a6b0c5;
        font-size: 17px;
        line-height: 1.7;
    }

    .orb {
        display: inline-block;
        width: 12px;
        height: 12px;
        margin-right: 10px;
        border-radius: 50%;
        background: #a78bfa;
        box-shadow: 0 0 20px #8b5cf6;
        animation: pulse 2.5s infinite;
    }

    .welcome {
        padding: 24px;
        margin: 16px 0 28px;
        border: 1px solid #343653;
        border-radius: 20px;
        background: linear-gradient(120deg, #20203a, #141c2b);
        animation: rise 0.5s ease-out;
    }

    .welcome h3 {
        color: #e2e8f0;
        margin-top: 0;
    }

    .welcome p {
        color: #a6b0c5;
        margin-bottom: 0;
    }

    [data-testid="stChatMessage"] {
        background: #171e2e;
        border: 1px solid #2b344b;
        border-radius: 18px;
        margin-bottom: 16px;
        padding: 20px;
        animation: rise 0.35s ease-out;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        color: #eef2ff;
    }

    [data-testid="stChatInput"] {
        border: 1px solid #56517f;
        border-radius: 16px;
    }

    .stButton > button {
        background: #25283e;
        color: #e2e8f0;
        border: 1px solid #454968;
        border-radius: 12px;
        transition: transform 0.2s, border-color 0.2s;
    }

    .stButton > button:hover {
        border-color: #a78bfa;
        color: #ffffff;
        transform: translateY(-2px);
    }

    @keyframes rise {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 12px #8b5cf6; }
        50% { opacity: 0.5; box-shadow: 0 0 28px #8b5cf6; }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# -------------------- Prompt template --------------------

template = PromptTemplate(
    input_variables=["question"],
    template="""You are a helpful assistant. Answer the question as truthfully as possible.
If you don't know the answer, say "I don't know".
Always answer in the same language as the question.
Always greet the user with a friendly greeting like Hello Jiiii.
Always end your answer with a friendly farewell with a smile.
Always take examples from the question.
If any short forms are used in the question, expand them in your answer.
Use Hinglish in your answer.
Always end your response with the phrase "ATHARV JI KI JAI HO" in a new line.
Question: {question}
""",
)


# -------------------- Model and history --------------------

@st.cache_resource
def get_model():
    return ChatOllama(
        model="qwen2.5-coder:1.5b",
        temperature=1.7,
    )


def reset_chat():
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful assistant")
    ]
    st.session_state.chat_ended = False


if "chat_history" not in st.session_state:
    reset_chat()

model = get_model()


def typewriter(text):
    for position in range(0, len(text), 8):
        yield text[position:position + 8]
        time.sleep(0.015)


# -------------------- Header --------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow"><span class="orb"></span>JARVIS / LOCAL AI</div>
    <h1>A little curiosity.<br>A great conversation.</h1>
    <p>Ask a question, explore an idea, or work through a problem.</p>
</div>
""", unsafe_allow_html=True)

info_col, button_col = st.columns([3, 1])

with info_col:
    st.caption("Qwen 2.5 Coder · Running through local Ollama")

with button_col:
    if st.button("＋ New chat", use_container_width=True):
        reset_chat()
        st.rerun()

animate = st.toggle("Typing animation", value=True)

st.divider()


# -------------------- Previous messages --------------------

welcome = st.empty()

if len(st.session_state.chat_history) == 1:
    welcome.markdown("""
    <div class="welcome">
        <h3>✦ What’s on your mind?</h3>
        <p>Try “Explain Python decorators” or “Help me brainstorm an app”.</p>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.chat_history:
    if isinstance(message, SystemMessage):
        continue

    is_user = isinstance(message, HumanMessage)

    with st.chat_message(
        "user" if is_user else "assistant",
        avatar="👤" if is_user else "🤖",
    ):
        st.markdown(message.content)


# -------------------- New message --------------------

user_input = st.chat_input(
    "Write a message…",
    disabled=st.session_state.chat_ended,
)

if user_input and user_input.strip():
    welcome.empty()

    # Store the original question for display and conversation history.
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    if user_input.strip().lower() == "bye":
        st.session_state.chat_history.append(
            AIMessage(
                content="Goodbye! 👋 Start a new chat whenever you like."
            )
        )
        st.session_state.chat_ended = True
        st.rerun()

    with st.chat_message("assistant", avatar="🤖"):
        try:
            # Fill the template with the current question.
            formatted_prompt = template.invoke({
                "question": user_input
            })

            # Preserve previous messages and replace only the current
            # question with its formatted prompt for this model call.
            model_messages = [
                *st.session_state.chat_history[:-1],
                HumanMessage(content=formatted_prompt.to_string()),
            ]

            with st.spinner("Thinking…"):
                response = model.invoke(model_messages)

        except Exception as error:
            st.session_state.chat_history.pop()

            st.error(
                "Couldn’t get a response. Check that Ollama is running "
                "and qwen2.5-coder:1.5b is downloaded, then send again."
            )

            with st.expander("Error details"):
                st.code(str(error))

        else:
            st.session_state.chat_history.append(
                AIMessage(content=response.content)
            )

            if animate:
                st.write_stream(typewriter(response.content))
            else:
                st.markdown(response.content)

if st.session_state.chat_ended:
    st.info("Conversation ended. Click “New chat” to start again.")