import re
import streamlit as st
from pipeline import YouTubeAgentPipeline

st.set_page_config(
    page_title="AI YouTube Summarizer",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------------
# GLOBAL STYLES
# ---------------------------------------------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #1e293b 0%, #050816 45%, #020308 100%);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 2.5rem;
    max-width: 1100px;
}

/* ---------- Hero ---------- */
.hero {
    text-align: center;
    padding: 10px 0 30px 0;
}

.hero .badge {
    display: inline-block;
    background: rgba(124, 92, 255, 0.12);
    border: 1px solid rgba(124, 92, 255, 0.35);
    color: #b9a6ff;
    font-size: 0.8rem;
    padding: 6px 16px;
    border-radius: 999px;
    margin-bottom: 18px;
    letter-spacing: 0.3px;
}

.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero p {
    color: #94a3b8;
    font-size: 1.1rem;
    margin: 0;
}

/* ---------- Glass input card ---------- */
.glass {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 28px 28px 8px 28px;
    border: 1px solid rgba(255,255,255,0.12);
    margin: 0 auto 28px auto;
    max-width: 760px;
}

.glass label { color: #cbd5e1 !important; font-weight: 500; }

.stTextInput > div > div > input {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 14px;
    color: #f1f5f9;
    padding: 14px 16px;
    font-size: 0.95rem;
}
.stTextInput > div > div > input:focus { border-color: #7c5cff; box-shadow: 0 0 0 1px #7c5cff; }
.stTextInput > div > div > input::placeholder { color: #64748b; }

.stButton > button {
    background: linear-gradient(90deg, #7c5cff, #4f8cff);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px 0;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    margin-top: 14px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(124, 92, 255, 0.35); color: white; }
.stButton > button:active { transform: translateY(0px) scale(0.99); }

/* ---------- Tabs ---------- */
[data-testid="stTabs"] button {
    color: #94a3b8;
    font-weight: 500;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #c4b5fd;
}

/* ---------- Reading surface — fixes the "wall of text" feel ---------- */
.reading {
    background: rgba(255,255,255,0.05);
    padding: 28px 32px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 18px;
}
.reading p { color: #cbd5e1; line-height: 1.85; margin: 0 0 14px 0; font-size: 0.97rem; }
.reading h1, .reading h2, .reading h3, .reading h4 {
    color: #f1f5f9;
    margin: 22px 0 10px 0;
    font-size: 1.05rem;
}
.reading strong { color: #c4b5fd; }
.reading ul, .reading ol { color: #cbd5e1; line-height: 1.85; margin: 0 0 16px 0; padding-left: 22px; }
.reading li { margin-bottom: 6px; }
.reading li::marker { color: #7c5cff; }

/* ---------- Keyword pills ---------- */
.pill-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin: 6px 0 20px 0; }
.pill {
    background: rgba(124, 92, 255, 0.14);
    border: 1px solid rgba(124, 92, 255, 0.3);
    color: #b9a6ff;
    font-size: 0.82rem;
    padding: 5px 14px;
    border-radius: 999px;
}

/* ---------- Quiz cards ---------- */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    margin-bottom: 10px;
}
[data-testid="stExpander"] summary { color: #e2e8f0; font-size: 0.92rem; }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HELPERS — turn flat LLM text into structured UI pieces
# ---------------------------------------------------------
def render_markdown_card(text: str):
    st.markdown(f"<div class='reading'>{_md_to_html(text)}</div>", unsafe_allow_html=True)


def _md_to_html(text: str) -> str:
    import markdown as _md_lib  # pip install markdown
    return _md_lib.markdown(text, extensions=["extra"])


def extract_keywords_section(text: str):
    """Pull out a '...Keywords:... <bullets>' block -> (pills_list, remaining_text)."""
    match = re.search(r"keywords?:\s*\n((?:\s*[-•*]\s*.+\n?)+)", text, re.IGNORECASE)
    if not match:
        return [], text
    bullets_block = match.group(1)
    pills = [b.strip("-•* ").strip() for b in bullets_block.splitlines() if b.strip()]
    cleaned = text[: match.start()] + text[match.end():]
    return pills, cleaned


def split_learning_sections(text: str):
    """Split the learning-material blob into (interview_qs, quiz_block, notes)."""
    quiz_start = re.search(r"quiz\s+questions?:?", text, re.IGNORECASE)
    notes_start = re.search(r"important\s+notes:?", text, re.IGNORECASE)

    if quiz_start:
        interview = text[:quiz_start.start()]
        if notes_start and notes_start.start() > quiz_start.start():
            quiz = text[quiz_start.end():notes_start.start()]
            notes = text[notes_start.end():]
        else:
            quiz = text[quiz_start.end():]
            notes = ""
    else:
        interview = text
        quiz = ""
        notes = ""

    return interview.strip(), quiz.strip(), notes.strip()


def parse_quiz_block(quiz_text: str):
    """Pull (question, answer) pairs out of the quiz text block."""
    pattern = re.compile(
        r"\d+\.\s*(.+?)\s*Answer:\s*(.+?)(?=\n\s*\d+\.|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    items = []
    for q_match in pattern.finditer(quiz_text):
        question = q_match.group(1).strip().replace("\n", " ")
        answer = q_match.group(2).strip().replace("\n", " ")
        items.append((question, answer))
    return items


def chunk_into_paragraphs(text: str, sentences_per_para: int = 4) -> str:
    """Raw transcripts come as one continuous blob with no paragraph breaks.
    Split on sentence-ending punctuation and group every N sentences into
    a paragraph so it's actually readable, instead of one giant wall of text."""
    text = text.strip()
    if not text:
        return text
    sentences = re.split(r'(?<=[.!?])\s+', text)
    paragraphs = [
        " ".join(sentences[i:i + sentences_per_para])
        for i in range(0, len(sentences), sentences_per_para)
    ]
    return "\n\n".join(paragraphs)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------
st.markdown("""
<div class='hero'>
    <span class='badge'>⚡ Multi-Agent System</span>
    <h1>Agentic AI YouTube Summarizer</h1>
    <p>Multi-Agent Learning Assistant Powered by Groq</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
youtube_url = st.text_input("Paste YouTube URL", placeholder="https://youtube.com/watch?v=...")
generate = st.button("🚀 Analyze Video", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------
if generate and youtube_url:

    with st.spinner("AI Agents Working..."):
        pipeline = YouTubeAgentPipeline()
        result = pipeline.run(youtube_url)

    tab0, tab1, tab2, tab3 = st.tabs(
        ["📜 Transcript", "📊 Analysis", "📝 Summary", "🎓 Learning"]
    )

    # ---------------- Transcript tab (raw TranscriptAgent output) ----------------
    with tab0:
        st.caption(f"{len(result['transcript'].split())} words — raw output from TranscriptAgent")
        readable_transcript = chunk_into_paragraphs(result["transcript"])
        render_markdown_card(readable_transcript)

    # ---------------- Analysis tab (raw AnalyzerAgent output) ----------------
    with tab1:
        st.caption("Raw output from AnalyzerAgent")
        keywords, remaining = extract_keywords_section(result["analysis"])
        render_markdown_card(remaining)
        if keywords:
            st.markdown(
                "<div class='pill-wrap'>" +
                "".join(f"<span class='pill'>{k}</span>" for k in keywords) +
                "</div>",
                unsafe_allow_html=True,
            )

    # ---------------- Summary tab (raw SummaryAgent output) ----------------
    with tab2:
        st.caption("Raw output from SummaryAgent")
        render_markdown_card(result["summary"])

    # ---------------- Learning tab (raw LearningAgent output) ----------------
    with tab3:
        st.caption("Raw output from LearningAgent")
        interview, quiz_block, notes = split_learning_sections(result["learning"])

        if interview:
            st.markdown("#### Interview questions")
            render_markdown_card(interview)

        quiz_items = parse_quiz_block(quiz_block) if quiz_block else []
        if quiz_items:
            st.markdown("#### Quiz — tap to reveal answer")
            for i, (question, answer) in enumerate(quiz_items, start=1):
                with st.expander(f"{i}. {question}"):
                    st.markdown(f"**Answer:** {answer}")
        elif quiz_block:
            st.markdown("#### Quiz")
            render_markdown_card(quiz_block)

        if notes:
            st.markdown("#### Important notes")
            render_markdown_card(notes)

elif generate and not youtube_url:
    st.warning("Pehle YouTube URL daal bhai 👆")