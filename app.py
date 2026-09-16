"""
app.py
------
Professional Streamlit web interface for the Smart AI Chatbot.
"""

import streamlit as st

from src.chatbot import _get_bot_reply_result
from src.utils import is_empty, is_exit_command, normalize_text


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="Smart AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# Custom CSS
# ============================================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 90% 5%,
            rgba(79, 70, 229, 0.32),
            transparent 30%
        ),
        radial-gradient(
            circle at 70% 70%,
            rgba(37, 99, 235, 0.18),
            transparent 35%
        ),
        #020817;

    color: #f8fafc;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #020617 0%,
            #061331 100%
        );

    border-right:
        1px solid rgba(148, 163, 184, 0.15);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}


/* Brand */

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 28px;
}

.brand-icon {
    width: 44px;
    height: 44px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    box-shadow:
        0 0 28px rgba(99, 102, 241, 0.45);

    color: white;
    font-size: 22px;
    font-weight: 700;
}

.brand-name {
    color: white;
    font-size: 21px;
    font-weight: 700;
    line-height: 1.1;
}

.brand-subtitle {
    color: #64748b;
    font-size: 11px;
    margin-top: 3px;
}


/* Sidebar Cards */

.sidebar-card {
    margin-top: 18px;
    padding: 16px;

    border:
        1px solid rgba(148, 163, 184, 0.13);

    border-radius: 16px;

    background:
        rgba(15, 23, 42, 0.60);
}

.sidebar-card-title {
    color: #e2e8f0;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 7px;
}

.sidebar-card-text {
    color: #64748b;
    font-size: 12px;
    line-height: 1.55;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {
    width: 100%;

    border-radius: 12px;

    border:
        1px solid rgba(129, 140, 248, 0.25);

    background:
        linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.20),
            rgba(124, 58, 237, 0.20)
        );

    color: #f8fafc;
    font-weight: 500;

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        background 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);

    border-color:
        rgba(129, 140, 248, 0.60);

    background:
        linear-gradient(
            135deg,
            rgba(37, 99, 235, 0.35),
            rgba(124, 58, 237, 0.35)
        );

    color: white;
}


/* =========================================================
   HERO
========================================================= */

.hero {
    padding: 18px 0 25px 0;
}

.hero-title {
    color: #f8fafc;

    font-size: 46px;
    font-weight: 700;

    line-height: 1.08;

    letter-spacing: -1.5px;

    margin: 0;
}

.gradient-text {
    background:
        linear-gradient(
            90deg,
            #60a5fa,
            #818cf8,
            #c084fc
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    background-clip: text;
}

.hero-description {
    max-width: 620px;

    color: #94a3b8;

    font-size: 16px;

    line-height: 1.6;

    margin-top: 14px;
}


/* =========================================================
   CHAT HEADER
========================================================= */

.chat-header {
    display: flex;
    align-items: center;
    gap: 13px;

    padding: 14px 18px;

    margin-bottom: 14px;

    border:
        1px solid rgba(148, 163, 184, 0.16);

    border-radius: 18px;

    background:
        rgba(15, 23, 42, 0.62);

    backdrop-filter: blur(12px);
}

.chat-logo {
    width: 44px;
    height: 44px;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    box-shadow:
        0 0 24px rgba(99, 102, 241, 0.40);

    font-size: 21px;
}

.chat-title {
    color: white;

    font-size: 16px;
    font-weight: 600;
}

.ai-badge {
    display: inline-block;

    margin-left: 6px;

    padding: 2px 7px;

    border-radius: 8px;

    border:
        1px solid rgba(167, 139, 250, 0.35);

    background:
        rgba(124, 58, 237, 0.15);

    color: #c4b5fd;

    font-size: 10px;
}

.online-status {
    color: #64748b;
    font-size: 11px;
    margin-top: 3px;
}


/* =========================================================
   WELCOME CARD
========================================================= */

.welcome-card {
    padding: 42px 30px;

    margin: 12px 0 18px 0;

    border:
        1px solid rgba(148, 163, 184, 0.14);

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.72),
            rgba(8, 20, 50, 0.60)
        );

    text-align: center;
}

.welcome-icon {
    font-size: 42px;
    margin-bottom: 12px;

    filter:
        drop-shadow(
            0 0 14px
            rgba(99, 102, 241, 0.60)
        );
}

.welcome-title {
    color: white;

    font-size: 22px;
    font-weight: 600;

    margin-bottom: 8px;
}

.welcome-text {
    color: #64748b;

    font-size: 13px;

    max-width: 560px;

    margin: auto;

    line-height: 1.6;
}


/* =========================================================
   CHAT MESSAGES
========================================================= */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;

    padding-top: 6px !important;
    padding-bottom: 6px !important;
}

[data-testid="stChatMessageContent"] {
    border-radius: 17px !important;

    padding: 12px 17px !important;

    color: #f8fafc !important;

    border:
        1px solid rgba(148, 163, 184, 0.13) !important;

    background:
        rgba(30, 41, 59, 0.78) !important;
}


/* User message */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stChatMessageContent"] {

    background:
        linear-gradient(
            135deg,
            #4338ca,
            #7c3aed
        ) !important;

    border:
        1px solid rgba(167, 139, 250, 0.30) !important;
}


/* =========================================================
   CHAT INPUT
========================================================= */

[data-testid="stChatInput"] {
    margin-top: 12px;
}

[data-testid="stChatInput"] > div {
    border-radius: 17px !important;

    border:
        1px solid rgba(129, 140, 248, 0.30) !important;

    background:
        rgba(15, 23, 42, 0.90) !important;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.22);
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}


/* =========================================================
   FOOTER
========================================================= */

.footer {
    text-align: center;

    color: #475569;

    font-size: 11px;

    margin-top: 13px;
}


/* =========================================================
   STREAMLIT BRANDING
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================================
# Session State
# ============================================================================

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================================
# Sidebar
# ============================================================================

with st.sidebar:

    st.html(
        """
        <div class="brand">

            <div class="brand-icon">
                ✦
            </div>

            <div>
                <div class="brand-name">
                    Smart AI
                </div>

                <div class="brand-subtitle">
                    Intelligent Assistant
                </div>
            </div>

        </div>
        """
    )


    # New Chat
    if st.button(
        "＋  New Chat",
        use_container_width=True,
    ):

        st.session_state.history = []

        st.rerun()


    st.html(
        """
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                ✦ AI Assistant
            </div>

            <div class="sidebar-card-text">
                A conversational AI assistant designed
                to provide helpful and accurate responses.
            </div>

        </div>
        """
    )


    message_count = len(
        st.session_state.history
    )


    st.html(
        f"""
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                Conversation
            </div>

            <div class="sidebar-card-text">
                {message_count} messages
                in the current session.
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                Technology
            </div>

            <div class="sidebar-card-text">
                Python<br>
                Streamlit<br>
                Cohere API
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                Session
            </div>

            <div class="sidebar-card-text">
                Your conversation is maintained
                during the current browser session.
            </div>

        </div>
        """
    )


# ============================================================================
# Hero Section
# ============================================================================

st.html(
    """
    <div class="hero">

        <h1 class="hero-title">
            AI that works<br>
            <span class="gradient-text">
                where you do.
            </span>
        </h1>

        <div class="hero-description">
            Your intelligent assistant for answers,
            insights, and everyday conversations.
        </div>

    </div>
    """
)


# ============================================================================
# Chat Header
# ============================================================================

st.html(
    """
    <div class="chat-header">

        <div class="chat-logo">
            ✦
        </div>

        <div>

            <div class="chat-title">
                Smart AI

                <span class="ai-badge">
                    AI
                </span>
            </div>

            <div class="online-status">
                Powered by Cohere
            </div>

        </div>

    </div>
    """
)


# ============================================================================
# Welcome Screen
# ============================================================================

if not st.session_state.history:

    st.html(
        """
        <div class="welcome-card">

            <div class="welcome-icon">
                ✦
            </div>

            <div class="welcome-title">
                How can I help you today?
            </div>

            <div class="welcome-text">
                Ask me anything and start a conversation.
                Your conversation context will be maintained
                throughout the current session.
            </div>

        </div>
        """
    )


# ============================================================================
# Display Conversation
# ============================================================================

for message in st.session_state.history:

    role = message["role"]
    content = message["content"]


    if role == "user":

        with st.chat_message(
            "user",
            avatar="👤",
        ):
            st.markdown(content)


    elif role == "assistant":

        with st.chat_message(
            "assistant",
            avatar="🤖",
        ):
            st.markdown(content)


# ============================================================================
# Chat Input
# ============================================================================

user_message = st.chat_input(
    "Ask anything..."
)


if user_message:

    # ---------------------------------------------------------
    # Normalize input
    # ---------------------------------------------------------

    user_message = normalize_text(user_message)


    # ---------------------------------------------------------
    # Empty input
    # ---------------------------------------------------------

    if is_empty(user_message):

        st.warning(
            "Please enter a message."
        )

        st.stop()


    # ---------------------------------------------------------
    # Exit command
    # ---------------------------------------------------------

    if is_exit_command(user_message):

        st.info("Goodbye! 👋")
        st.stop()


    # ---------------------------------------------------------
    # Preserve previous history
    # ---------------------------------------------------------

    previous_history = list(
        st.session_state.history
    )


    # ---------------------------------------------------------
    # Generate response
    # ---------------------------------------------------------

    with st.spinner("Thinking..."):

        reply, success = _get_bot_reply_result(
            previous_history,
            user_message,
        )


    # ---------------------------------------------------------
    # Store conversation only after success
    # ---------------------------------------------------------

    if not success:
        st.stop()

    st.session_state.history.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )


    # ---------------------------------------------------------
    # Refresh UI
    # ---------------------------------------------------------

    st.rerun()


# ============================================================================
# Footer
# ============================================================================

st.html(
    """
    <div class="footer">
        Smart AI may make mistakes.
        Please verify important information.
    </div>
    """
)