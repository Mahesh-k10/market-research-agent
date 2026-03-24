import streamlit as st
from agents.orchestrator import run_market_research
from tools.pdf_export import export_pdf

st.set_page_config(
    page_title="Meridian · Market Intelligence",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0c0c10 !important;
    color: #e8e2d9 !important;
    font-family: 'Instrument Sans', sans-serif;
}

/* Ambient orbs */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -200px; right: -150px;
    width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(196,160,100,0.06) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -200px; left: -100px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(80,140,200,0.05) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"], [data-testid="stToolbar"] { display: none !important; }

/* ── Main container ── */
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 780px !important;
}

/* ── Header ── */
.meridian-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    border-bottom: 1px solid rgba(232,226,217,0.09);
    padding-bottom: 1.25rem;
    margin-bottom: 3.5rem;
}
.meridian-logo-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #c4a064;
    margin-bottom: 0.3rem;
}
.meridian-logo-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 300;
    color: #e8e2d9;
    line-height: 1;
}
.meridian-logo-name span { font-style: italic; color: #c4a064; }
.meridian-header-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.56rem;
    letter-spacing: 0.16em;
    color: rgba(232,226,217,0.28);
    text-transform: uppercase;
    text-align: right;
    line-height: 1.8;
}

/* ── Hero text ── */
.meridian-hero {
    text-align: center;
    margin-bottom: 2.5rem;
}
.meridian-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #c4a064;
    margin-bottom: 1.2rem;
}
.meridian-headline {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 300;
    line-height: 1.15;
    color: #e8e2d9;
    margin-bottom: 1rem;
}
.meridian-headline em { font-style: italic; color: #c4a064; }
.meridian-subtext {
    font-size: 0.88rem;
    color: rgba(232,226,217,0.45);
    line-height: 1.75;
    max-width: 500px;
    margin: 0 auto;
}

/* ── Input label override ── */
.input-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(232,226,217,0.4);
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
}

/* ── Streamlit text_input ── */
[data-testid="stTextInput"] > div > div {
    background: transparent !important;
}
[data-testid="stTextInput"] > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(232,226,217,0.13) !important;
    border-radius: 2px !important;
    color: #e8e2d9 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.25rem !important;
    font-weight: 300 !important;
    padding: 0.85rem 1.1rem !important;
    caret-color: #c4a064 !important;
    box-shadow: none !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: rgba(196,160,100,0.5) !important;
    box-shadow: 0 0 0 3px rgba(196,160,100,0.06) !important;
}
[data-testid="stTextInput"] > div > div > input::placeholder {
    color: rgba(232,226,217,0.2) !important;
    font-style: italic;
}
[data-testid="stTextInput"] label { display: none !important; }

/* ── Run button ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: transparent !important;
    border: 1px solid rgba(196,160,100,0.45) !important;
    color: #c4a064 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.62rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    padding: 0.95rem 2rem !important;
    border-radius: 2px !important;
    margin-top: 0.75rem !important;
    cursor: pointer !important;
    transition: all 0.22s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: rgba(196,160,100,0.09) !important;
    border-color: #c4a064 !important;
    box-shadow: 0 0 28px rgba(196,160,100,0.12) !important;
    color: #d4b474 !important;
}
[data-testid="stButton"] > button:active {
    transform: scale(0.985) !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] {
    margin: 1.25rem 0 0.5rem !important;
}
[data-testid="stProgress"] > div {
    background: rgba(232,226,217,0.07) !important;
    border-radius: 0 !important;
    height: 2px !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #c4a064, #e8c98a) !important;
    border-radius: 0 !important;
}

/* ── Agent step cards ── */
.agent-step {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 0.75rem 1rem;
    border: 1px solid rgba(232,226,217,0.06);
    border-left: 2px solid rgba(196,160,100,0.4);
    background: rgba(255,255,255,0.015);
    margin-bottom: 0.5rem;
    border-radius: 1px;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    color: rgba(232,226,217,0.6);
    animation: stepIn 0.35s ease both;
}
.agent-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #c4a064;
    box-shadow: 0 0 6px rgba(196,160,100,0.7);
    animation: dotPulse 1.3s ease infinite;
    flex-shrink: 0;
}
@keyframes dotPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.65); }
}
@keyframes stepIn {
    from { opacity: 0; transform: translateX(-6px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ── Divider ── */
.meridian-divider {
    border: none;
    border-top: 1px solid rgba(232,226,217,0.08);
    margin: 2.5rem 0;
}

/* ── Report header ── */
.report-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.report-title-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.45rem;
    font-weight: 300;
    color: #e8e2d9;
}
.report-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c4a064;
    border: 1px solid rgba(196,160,100,0.3);
    padding: 0.28rem 0.7rem;
    border-radius: 1px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 260px;
}

/* ── Text area (report) ── */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(232,226,217,0.09) !important;
    border-radius: 2px !important;
    color: #e0dbd2 !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 0.875rem !important;
    line-height: 1.85 !important;
    padding: 1.25rem !important;
    box-shadow: none !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(196,160,100,0.25) !important;
    box-shadow: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    background: rgba(196,160,100,0.07) !important;
    border: 1px solid rgba(196,160,100,0.35) !important;
    color: #c4a064 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 2rem !important;
    border-radius: 2px !important;
    margin-top: 0.75rem !important;
    transition: all 0.22s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(196,160,100,0.14) !important;
    border-color: #c4a064 !important;
    box-shadow: 0 0 20px rgba(196,160,100,0.1) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(232,226,217,0.1) !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.15em !important;
    color: rgba(232,226,217,0.5) !important;
}

/* ── Footer ── */
.meridian-footer {
    border-top: 1px solid rgba(232,226,217,0.06);
    padding-top: 1.5rem;
    margin-top: 3rem;
    display: flex;
    justify-content: space-between;
    font-family: 'DM Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(232,226,217,0.18);
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="meridian-header">
    <div>
        <div class="meridian-logo-sub">◈ Intelligence Platform</div>
        <div class="meridian-logo-name">Meri<span>dian</span></div>
    </div>
    <div class="meridian-header-meta">
        Multi-Agent Research System<br>Powered by AI
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="meridian-hero">
    <div class="meridian-eyebrow">◈ &nbsp; Deep Market Intelligence &nbsp; ◈</div>
    <div class="meridian-headline">
        Uncover the forces<br>shaping <em>your market</em>
    </div>
    <p class="meridian-subtext">
        Four AI agents work in concert — analysing industries, benchmarking competitors,
        tracking trends, and distilling findings into a publication-ready report.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input ───────────────────────────────────────────────────────────────────
st.markdown('<div class="input-eyebrow">Research Topic</div>', unsafe_allow_html=True)

topic = st.text_input(
    label="Research Topic",
    placeholder="e.g.  Generative AI in Healthcare Diagnostics",
    label_visibility="collapsed",
)

run_clicked = st.button("◈  Initiate Research")

# ── Validation & agents ─────────────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    banned_words = ["sex", "porn", "terror", "kill"]
    if any(word in topic.lower() for word in banned_words):
        st.error("This topic is not permitted. Please enter a business or market-related topic.")
        st.stop()

    if len(topic.split()) < 2:
        st.warning("Please enter a more descriptive topic (e.g. 'AI in Healthcare Market').")
        st.stop()

    st.markdown("<hr class='meridian-divider'>", unsafe_allow_html=True)

    progress = st.progress(0)

    s1 = st.empty()
    s1.markdown('<div class="agent-step"><span class="agent-dot"></span>Industry Research Agent — mapping the competitive landscape…</div>', unsafe_allow_html=True)
    progress.progress(22)

    s2 = st.empty()
    s2.markdown('<div class="agent-step"><span class="agent-dot"></span>Competitor Analysis Agent — profiling key players &amp; positioning…</div>', unsafe_allow_html=True)
    progress.progress(46)

    s3 = st.empty()
    s3.markdown('<div class="agent-step"><span class="agent-dot"></span>Market Trends Agent — extracting signals from the noise…</div>', unsafe_allow_html=True)
    progress.progress(70)

    s4 = st.empty()
    s4.markdown('<div class="agent-step"><span class="agent-dot"></span>Synthesis Agent — composing final intelligence report…</div>', unsafe_allow_html=True)
    progress.progress(88)

    with st.spinner("Agents collaborating · please wait…"):
        st.session_state["report"] = run_market_research(topic)
        st.session_state["topic"] = topic

    progress.progress(100)
    st.success("✦  Analysis complete — your report is ready below.")

# ── Report ───────────────────────────────────────────────────────────────────
if "report" in st.session_state:
    report = st.session_state["report"]
    saved_topic = st.session_state.get("topic", "")
    badge_label = (saved_topic[:38] + "…") if len(saved_topic) > 40 else saved_topic

    st.markdown("<hr class='meridian-divider'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="report-meta">
        <div class="report-title-text">Intelligence Report</div>
        <div class="report-badge">◈ &nbsp;{badge_label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        label="report",
        value=report,
        height=520,
        label_visibility="collapsed",
    )

    filename = export_pdf(report)
    with open(filename, "rb") as f:
        st.download_button(
            label="◈  Download Full Report · PDF",
            data=f,
            file_name=filename,
            mime="application/pdf",
        )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="meridian-footer">
    <span>Meridian · Market Intelligence</span>
    <span>Confidential · AI-Generated</span>
</div>
""", unsafe_allow_html=True)
