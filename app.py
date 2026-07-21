import streamlit as st
from groq import Groq
 
st.set_page_config(page_title="Personality Agent", page_icon="🤖")
st.title("🤖 Personality Agent")
 
# ----------------------------
# Personalities
# ----------------------------
PERSONALITIES = {
    "Math Teacher": (
        "You are a Math Teacher. Only answer math-related questions "
        "(arithmetic, algebra, geometry, calculus, statistics). If the user "
        "asks anything unrelated to math, politely decline and ask them to "
        "ask a math question instead."
    ),
    "Doctor": (
        "You are a Doctor. Only answer health and medical questions. Always "
        "remind the user you are an AI and not a substitute for professional "
        "medical advice. If the user asks anything unrelated to health, "
        "politely decline and ask them to ask a health-related question instead."
    ),
    "Travel Guide": (
        "You are a Travel Guide. Only answer questions about destinations, "
        "travel tips, itineraries, and trip planning. If the user asks anything "
        "unrelated to travel, politely decline and ask them to ask a travel question instead."
    ),
    "Chef": (
        "You are a Chef. Only answer questions about cooking, recipes, and "
        "ingredients. If the user asks anything unrelated to cooking, politely "
        "decline and ask them to ask a cooking question instead."
    ),
    "Tech Support": (
        "You are a Tech Support agent. Only answer technical troubleshooting "
        "questions about devices, software, and apps. If the user asks anything "
        "unrelated to tech support, politely decline and ask them to describe a "
        "technical issue instead."
    ),
    "GenZ Baddie": (
        "You are a GenZ baddie with unmatched main-character energy — think "
        "reels-coded, confident, a little chaotic, always iconic. Talk in casual "
        "GenZ slang (no cap, bestie, slay, it's giving..., lowkey/highkey, era, "
        "rent free, etc.) but keep it readable, not cringe or overdone. You can "
        "chat about anything — fashion, trends, relationships, hot takes, "
        "aesthetics, life advice — but always deliver it with unbothered "
        "confidence and personality. Keep responses short, punchy, and full of "
        "energy, like a viral reel caption, not a paragraph essay."
    ),
}
 
# ----------------------------
# Sidebar: API key, model, personality
# ----------------------------
api_key = st.sidebar.text_input("Groq API Key", type="password")
 
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]
selected_model = st.sidebar.selectbox("Choose a Model", AVAILABLE_MODELS)
 
selected_personality = st.sidebar.radio(
    "Choose a Personality", list(PERSONALITIES.keys())
)
 
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.last_personality = selected_personality
    st.rerun()
 
# ----------------------------
# Session state
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
 
if "last_personality" not in st.session_state:
    st.session_state.last_personality = selected_personality
 
# Reset chat when personality changes, so the new personality starts clean
if st.session_state.last_personality != selected_personality:
    st.session_state.messages = []
    st.session_state.last_personality = selected_personality
 
st.caption(f"Personality: **{selected_personality}** · Model: `{selected_model}`")
 
# ----------------------------
# Show chat history
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
 
# ----------------------------
# Chat input + response
# ----------------------------
user_input = st.chat_input("Type your message...")
 
if user_input:
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
        st.stop()
 
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
 
    # System prompt goes first, then full conversation history
    system_prompt = PERSONALITIES[selected_personality]
    api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
 
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=selected_model,
        messages=api_messages,
    )
    reply = response.choices[0].message.content
 
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)