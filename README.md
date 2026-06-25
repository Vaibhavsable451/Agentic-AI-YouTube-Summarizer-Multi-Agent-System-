# Agentic-AI-YouTube-Summarizer-Multi-Agent-System-
:

🚀 Agentic AI YouTube Summarizer (Multi-Agent System)

An AI-powered multi-agent system that takes a YouTube video link and automatically:

🎥 Extracts transcript
🧠 Analyzes content
📝 Generates summaries
🎓 Creates learning material (notes, Q&A, quizzes)
⚡ Powered by Groq LLM + Agentic AI pipeline
🧠 Project Architecture
User Input (YouTube URL)
        │
        ▼
Transcript Agent
        │
        ▼
Analyzer Agent
        │
        ▼
Summary Agent
        │
        ▼
Learning Agent
        │
        ▼
Streamlit Dashboard
✨ Features
🎥 YouTube Processing
Supports any YouTube video link
Extracts auto-generated captions
🧠 AI Agents
Transcript Agent → Extract video text
Analyzer Agent → Extract topic & keywords
Summary Agent → Generate short & detailed summary
Learning Agent → Generate Q&A + notes + quizzes
⚡ AI Engine
Groq LLaMA 3.3 70B
Fast inference
High-quality responses
🎨 UI
Streamlit interactive dashboard
Simple and clean interface
Easy user experience
🏗️ Tech Stack
Python 🐍
Streamlit 🎨
Groq API ⚡
LangChain 🤖
YouTube Transcript API 🎥
dotenv 🔐
📁 Project Structure
youtube-agent/
│
├── app.py
├── pipeline.py
├── config.py
│
├── agents/
│   ├── transcript_agent.py
│   ├── analyzer_agent.py
│   ├── summary_agent.py
│   └── learning_agent.py
│
├── services/
│   └── groq_service.py
│
├── .env
├── requirements.txt
└── README.md
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/youtube-agent.git
cd youtube-agent
2️⃣ Create Virtual Environment
python -m venv .venv

Activate:

.venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup Environment Variables

Create .env file:

GROQ_API_KEY=your_groq_api_key

👉 Get API Key: https://console.groq.com

5️⃣ Run Application
streamlit run app.py
🧪 How It Works
Paste YouTube URL
Transcript Agent extracts video text
Analyzer Agent detects topic & keywords
Summary Agent generates insights
Learning Agent creates:
Notes
Quiz questions
Interview questions
Results shown in UI
📌 Example Output
🧠 Analysis
Topic: LangGraph Agents
Keywords: workflows, state management, AI agents
📝 Summary

Explains video content in simple structured format...

🎓 Learning Material
What is LangGraph?
Difference between LangChain & LangGraph
MCQ Questions
🚀 Future Improvements
🔥 RAG-based video chat system
🎙️ Audio summary (TTS)
📄 PDF export of notes
🤖 Multi-video comparison agent
🧾 YouTube playlist summarizer
🌐 React + FastAPI version
💡 Why This Project is Special

✔ Multi-Agent AI System
✔ Real-world LLM application
✔ RAG-ready architecture
✔ Production-style pipeline
✔ Resume-ready GenAI project

👨‍💻 Author

Your Name
AI Engineer | GenAI Developer | MCA Student
