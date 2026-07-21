
# Personality AI Agent
 
A Streamlit chatbot powered by Groq's fast LLM inference. Pick a model, pick a personality Math Teacher, Doctor, Travel Guide, Chef, Tech Support, or GenZ Baddie and chat. Each personality stays in character and (where applicable) politely declines off-topic questions.
 
## Features
- Real-time chat interface built with Streamlit
- Model selector (Llama 3.3, Llama 3.1, Gemma2 — all hosted on Groq)
- 6 personalities, each enforced through a dedicated system prompt
- Session memory conversation context persists while you chat
- Chat automatically clears when you switch personality
- Free to deploy on Streamlit Cloud
## 1. Setup
 
Clone or download this project, then open it in VS Code.
 
Create and activate a virtual environment (recommended):
 
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```
 
Install dependencies:
 
```powershell
pip install -r requirements.txt
```
 
## 2. Get a Groq API Key
1. Go to https://console.groq.com/keys
2. Sign up or log in (free)
3. Click **Create API Key**, copy it (starts with `gsk_...`)
You'll paste this into the app's sidebar when you run it.
 
## 3. Run Locally
 
```powershell
python -m streamlit run app.py
```
 
This opens the app in your browser (usually `http://localhost:8501`). Paste your Groq API key into the sidebar, pick a model and personality, and start chatting.
 
## 4. Deploy to Streamlit Cloud (Free)
 
1. Push this project to a **public GitHub repo**:
```powershell
   git init
   git add .
   git commit -m "Initial commit: personality chatbot"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
```
2. Go to https://share.streamlit.io and sign in with GitHub
3. Click **New app**, select your repo, branch (`main`), and main file (`app.py`)
4. Click **Deploy**
You'll get a public link like `https://your-app-name.streamlit.app` that anyone can use they just need to paste in their own Groq API key.
 
## Project Structure
```
PersonalityAgent/
├── app.py               # Main Streamlit app
├── requirements.txt      # Python dependencies
└── README.md
```
 
## How Personality Enforcement Works
Each personality has a system prompt describing what it should (and shouldn't) talk about. That prompt is sent to Groq with every message alongside the chat history, so the model stays consistently in character for the whole session.
 
## Personalities
 
| Personality | Behavior |
|---|---|
| Math Teacher | Only answers math questions |
| Doctor | Only answers health/medical questions (with AI disclaimer) |
| Travel Guide | Only answers travel-related questions |
| Chef | Only answers cooking/recipe questions |
| Tech Support | Only answers tech troubleshooting questions |
| GenZ Baddie | Talks about anything, but always in confident GenZ slang, reels-caption style |
 
## Customization
- Add new personalities by adding an entry to the `PERSONALITIES` dict in `app.py`
- Swap or add models in the `AVAILABLE_MODELS` list (check https://console.groq.com/docs/models for the current list, since Groq updates it periodically)
- Add avatars with `st.chat_message(role, avatar=...)`
