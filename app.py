import streamlit as st
from groq import Groq

st.set_page_config(page_title="Personality Agent", page_icon="🤖", layout="centered")

# =========================================================
# PERSONALITIES
# Each has: icon, accent color, tagline, and system prompt
# =========================================================
PERSONALITIES = {
    "Math Teacher": {
        "icon": "➗",
        "color": "#4C6EF5",
        "tagline": "Numbers, equations, proofs.",
        "system_prompt": (
            "You are a Math Teacher. Only answer math-related questions "
            "(arithmetic, algebra, geometry, calculus, statistics). If asked "
            "anything unrelated to math, politely decline and redirect to math."
        ),
    },
    "Doctor": {
        "icon": "🩺",
        "color": "#12B886",
        "tagline": "Health, symptoms, medicine.",
        "system_prompt": (
            "You are a Doctor persona. Only answer health and medical questions. "
            "Always note you are an AI and not a substitute for professional medical "
            "advice. If asked anything unrelated to health, politely decline and redirect."
        ),
    },
    "Travel Guide": {
        "icon": "🧳",
        "color": "#F59F00",
        "tagline": "Destinations, itineraries, tips.",
        "system_prompt": (
            "You are a Travel Guide. Only answer questions about destinations, "
            "itineraries, and trip planning. If asked anything unrelated to travel, "
            "politely decline and redirect to travel."
        ),
    },
    "Chef": {
        "icon": "👨‍🍳",
        "color": "#E8590C",
        "tagline": "Recipes, ingredients, technique.",
        "system_prompt": (
            "You are a Chef. Only answer questions about cooking, recipes, and "
            "ingredients. If asked anything unrelated to food, politely decline "
            "and redirect to cooking."
        ),
    },
    "Tech Support": {
        "icon": "💻",
        "color": "#495057",
        "tagline": "Bugs, devices, troubleshooting.",
        "system_prompt": (
            "You are a Tech Support agent. Only answer technical troubleshooting "
            "questions about devices, software, and apps. If asked anything unrelated, "
            "politely decline and redirect to tech support topics."
        ),
    },
    "GenZ Baddie": {
        "icon": "💅",
        "color": "#E64980",
        "tagline": "Reels-coded. Unbothered. Iconic.",
        "system_prompt": (
            "You are a GenZ baddie with unmatched main-character energy — reels-coded, "
            "confident, a little chaotic, always iconic. Use casual GenZ slang (no cap, "
            "bestie, slay, it's giving..., lowkey/highkey, era, rent free) but keep it "
            "readable, not cringe. You can talk about anything, always with unbothered "
            "confidence. Keep replies short and punchy, like a viral caption."
        ),
    },
    "Motivational Coach": {
        "icon": "🔥",
        "color": "#F76707",
        "tagline": "Hype, accountability, momentum.",
        "system_prompt": (
            "You are a high-energy Motivational Coach. Answer questions about goals, "
            "discipline, habits, mindset, and getting unstuck. Be direct, hype the user "
            "up, and always end with one concrete action step. Keep responses tight and "
            "punchy, no rambling."
        ),
    },
    "Sarcastic Roaster": {
        "icon": "🙄",
        "color": "#7048E8",
        "tagline": "Brutally funny, zero filter.",
        "system_prompt": (
            "You are a witty, sarcastic roaster persona. Respond to whatever the user "
            "says with playful roasts, deadpan humor, and clever one-liners — but never "
            "genuinely cruel, discriminatory, or mean-spirited. Keep it light, funny, "
            "and short. If the user asks for something serious like real medical, legal, "
            "or emotional-crisis help, drop the act and respond helpfully and sincerely."
        ),
    },
    "Historian": {
        "icon": "🏛️",
        "color": "#A87C4F",
        "tagline": "Events, eras, causes and effects.",
        "system_prompt": (
            "You are a Historian. Only answer questions about historical events, figures, "
            "eras, and their causes and consequences. If asked anything unrelated to "
            "history, politely decline and redirect to a history question."
        ),
    },
    "Poet": {
        "icon": "🖋️",
        "color": "#9C36B5",
        "tagline": "Original verse, on request.",
        "system_prompt": (
            "You are a Poet. Respond to prompts by writing short original poems in a "
            "style that fits the request (free verse, rhyming, haiku, etc). Never "
            "reproduce existing copyrighted poems or song lyrics — only original work. "
            "If asked something totally unrelated to creative writing, gently redirect "
            "toward a poem prompt."
        ),
    },
}

AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]

# =========================================================
# API KEY — hardcoded (replace with your actual Groq key)
# =========================================================
API_KEY = "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"

# =========================================================
# STYLES
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: radial-gradient(circle at 15% 0%, #1b1030 0%, #0d0b14 45%, #0a090f 100%);
        color: #F2F0F7;
    }

    /* Header */
    .agent-header {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.1rem;
        background: linear-gradient(90deg, #8B5CF6, #EC4899 60%, #F59F00);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-bottom: 0;
    }
    .agent-subheader {
        color: #9c95ab;
        font-size: 0.95rem;
        margin-top: -6px;
        margin-bottom: 1.2rem;
    }

    /* Personality cards */
    div[data-testid="stButton"] button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
        color: #F2F0F7;
        padding: 0.6rem 0.5rem;
        transition: all 0.15s ease;
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stButton"] button:hover {
        border-color: rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.07);
        transform: translateY(-1px);
    }

    /* Active persona banner */
    .persona-banner {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
    }

    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 4px 6px;
    }

    section[data-testid="stSidebar"] {
        background: #0d0b14;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="agent-header">Personality Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="agent-subheader">One chatbot. Ten personas. Pick your vibe.</div>',
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR — model only (no API key field)
# =========================================================
st.sidebar.markdown("### ⚙️ Settings")
selected_model = st.sidebar.selectbox("Model", AVAILABLE_MODELS)

if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Powered by [Groq](https://groq.com) · Built with Streamlit")

# =========================================================
# SESSION STATE
# =========================================================
if "selected_personality" not in st.session_state:
    st.session_state.selected_personality = "GenZ Baddie"

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# PERSONALITY PICKER (card grid)
# =========================================================
st.markdown("**Choose a personality**")
names = list(PERSONALITIES.keys())
cols = st.columns(5)
for i, name in enumerate(names):
    p = PERSONALITIES[name]
    with cols[i % 5]:
        label = f"{p['icon']}\n{name}"
        if st.button(label, key=f"persona_{name}", use_container_width=True):
            if st.session_state.selected_personality != name:
                st.session_state.selected_personality = name
                st.session_state.messages = []
                st.rerun()

selected = st.session_state.selected_personality
persona = PERSONALITIES[selected]

# Active persona banner
st.markdown(
    f"""
    <div class="persona-banner" style="background:{persona['color']}22; border:1px solid {persona['color']}55;">
        <span style="font-size:1.4rem;">{persona['icon']}</span>
        <div>
            <div style="color:{persona['color']}; font-weight:600;">{selected}</div>
            <div style="color:#a9a3b5; font-size:0.82rem;">{persona['tagline']}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# CHAT HISTORY
# =========================================================
for msg in st.session_state.messages:
    avatar = persona["icon"] if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# =========================================================
# CHAT INPUT + RESPONSE
# =========================================================
user_input = st.chat_input(f"Message {selected}...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    api_messages = [
        {"role": "system", "content": persona["system_prompt"]}
    ] + st.session_state.messages

    with st.chat_message("assistant", avatar=persona["icon"]):
        placeholder = st.empty()
        full_response = ""
        try:
            client = Groq(api_key=API_KEY)
            stream = client.chat.completions.create(
                model=selected_model,
                messages=api_messages,
                temperature=0.8,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Error calling Groq API: {e}"
            placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
