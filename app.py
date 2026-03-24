import streamlit as st
from agents.orchestrator import run_market_research
from tools.pdf_export import export_pdf

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meridian · Market Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e2d9 !important;
}

[data-testid="stAppViewContainer"] > .main > div {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Layout shell ── */
.shell {
    min-height: 100vh;
    display: grid;
    grid-template-rows: auto 1fr auto;
    padding: 0 max(2rem, calc((100vw - 1100px) / 2));
    font-family: 'Instrument Sans', sans-serif;
    position: relative;
    overflow: hidden;
}

/* Ambient background orbs */
.shell::before {
    content: '';
    position: fixed;
    top: -20vh;
    right: -10vw;
    width: 60vw;
    height: 60vw;
    background: radial-gradient(circle at 60% 40%,
        rgba(196, 160, 100, 0.06) 0%,
        rgba(120, 90, 200, 0.04) 40%,
        transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}
.shell::after {
    content: '';
    position: fixed;
    bottom: -15vh;
    left: -5vw;
    width: 50vw;
    height: 50vw;
    background: radial-gradient(circle at 40% 60%,
        rgba(80, 160, 200, 0.05) 0%,
        transparent 65%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}

/* ── Header ── */
.site-header {
    position: relative;
    z-index: 10;
    padding: 2.5rem 0 2rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    border-bottom: 1px solid rgba(232, 226, 217, 0.08);
}

.logo-mark {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #c4a064;
    opacity: 0.9;
}

.brand-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.95rem;
    font-weight: 300;
    letter-spacing: 0.02em;
    color: #e8e2d9;
    line-height: 1;
    margin-top: 0.25rem;
}

.brand-name em {
    font-style: italic;
    color: #c4a064;
}

.header-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    color: rgba(232, 226, 217, 0.35);
    text-transform: uppercase;
    text-align: right;
}

/* ── Hero section ── */
.hero {
    position: relative;
    z-index: 10;
    padding: 5rem 0 3.5rem;
    text-align: center;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #c4a064;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
}
.hero-eyebrow::before, .hero-eyebrow::after {
    content: '';
    width: 2rem;
    height: 1px;
    background: #c4a064;
    opacity: 0.5;
}

.hero-headline {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.8rem, 5.5vw, 4.8rem);
    font-weight: 300;
    line-height: 1.1;
    letter-spacing: -0.01em;
    color: #e8e2d9;
    margin-bottom: 1.5rem;
    max-width: 820px;
    margin-inline: auto;
}

.hero-headline em {
    font-style: italic;
    color: #c4a064;
}

.hero-sub {
    font-size: 0.95rem;
    color: rgba(232, 226, 217, 0.5);
    max-width: 480px;
    margin-inline: auto;
    line-height: 1.7;
    font-weight: 400;
}

/* ── Input card ── */
.input-card {
    position: relative;
    z-index: 10;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(232, 226, 217, 0.1);
    border-radius: 2px;
    padding: 2.5rem 2.5rem 2rem;
    max-width: 760px;
    margin: 0 auto 1.5rem;
    backdrop-filter: blur(12px);
}

.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3rem; height: 1px;
    background: #c4a064;
}

.input-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(232, 226, 217, 0.45);
    margin-bottom: 1rem;
    display: block;
}

/* Override Streamlit text_input */
[data-testid="stTextInput"] > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: none !important;
    border-bottom: 1px solid rgba(232, 226, 217, 0.2) !important;
    border-radius: 0 !important;
    color: #e8e2d9 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.35rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.01em !important;
    padding: 0.6rem 0 !important;
    caret-color: #c4a064 !important;
    box-shadow: none !important;
    transition: border-color 0.3s ease !important;
}

[data-testid="stTextInput"] > div > div > input:focus {
    border-bottom-color: #c4a064 !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] > div > div > input::placeholder {
    color: rgba(232, 226, 217, 0.22) !important;
    font-style: italic;
}

[data-testid="stTextInput"] > label { display: none !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid rgba(196, 160, 100, 0.5) !important;
    color: #c4a064 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 2.5rem !important;
    border-radius: 1px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    display: block !important;
    margin: 0 auto !important;
}

[data-testid="stButton"] > button:hover {
    background: rgba(196, 160, 100, 0.1) !important;
    border-color: #c4a064 !important;
    box-shadow: 0 0 24px rgba(196, 160, 100, 0.12) !important;
}

[data-testid="stButton"] > button:active {
    transform: scale(0.98) !important;
}

/* ── Progress / status ── */
.workflow-shell {
    max-width: 760px;
    margin: 1.5rem auto 0;
    position: relative;
    z-index: 10;
}

[data-testid="stProgress"] > div > div {
    background: rgba(232, 226, 217, 0.08) !important;
    border-radius: 0 !important;
    height: 2px !important;
}

[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #c4a064, #e8c98a) !important;
    border-radius: 0 !important;
    transition: width 0.5s ease !important;
}

/* Agent status lines */
.agent-step {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.85rem 0;
    border-bottom: 1px solid rgba(232, 226, 217, 0.05);
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: rgba(232, 226, 217, 0.55);
    animation: fadeSlide 0.4s ease both;
}

@keyframes fadeSlide {
    from { opacity: 0; transform: translateX(-8px); }
    to   { opacity: 1; transform: translateX(0); }
}

.agent-step .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #c4a064;
    box-shadow: 0 0 8px rgba(196,160,100,0.6);
    animation: pulse 1.4s ease infinite;
    flex-shrink: 0;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}

/* Override st.write() inside status areas */
[data-testid="stMarkdownContainer"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    color: rgba(232, 226, 217, 0.6) !important;
    line-height: 2.2 !important;
}

/* Success / warning / error */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 1px !important;
    border: 1px solid rgba(232,226,217,0.1) !important;
    max-width: 760px;
    margin-inline: auto !important;
}

/* ── Report section ── */
.report-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 900px;
    margin: 3rem auto 1.5rem;
    position: relative;
    z-index: 10;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(232, 226, 217, 0.1);
}

.report-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 300;
    letter-spacing: 0.01em;
    color: #e8e2d9;
}

.report-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c4a064;
    border: 1px solid rgba(196,160,100,0.35);
    padding: 0.3rem 0.75rem;
    border-radius: 1px;
}

/* Override text_area */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(232,226,217,0.08) !important;
    border-radius: 2px !important;
    color: #e8e2d9 !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.8 !important;
    padding: 1.5rem !important;
    max-width: 900px !important;
    box-shadow: none !important;
    resize: vertical !important;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(196,160,100,0.3) !important;
    box-shadow: none !important;
}

[data-testid="stTextArea"] > label { display: none !important; }

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: rgba(196,160,100,0.08) !important;
    border: 1px solid rgba(196,160,100,0.4) !important;
    color: #c4a064 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    border-radius: 1px !important;
    display: block !important;
    margin: 1.5rem auto 0 !important;
    transition: all 0.25s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(196,160,100,0.16) !important;
    box-shadow: 0 0 20px rgba(196,160,100,0.1) !important;
}

/* Spinner */
[data-testid="stSpinner"] > div {
    color: #c4a064 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
}

/* ── Footer ── */
.site-footer {
    position: relative;
    z-index: 10;
    padding: 2rem 0;
    margin-top: 4rem;
    border-top: 1px solid rgba(232,226,217,0.06);
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.18em;
    color: rgba(232,226,217,0.2);
    text-transform: uppercase;
}

/* ── Horizontal rule ── */
[data-testid="stMarkdownContainer"] hr {
    border: none;
    border-top: 1px solid rgba(232,226,217,0.07);
    margin: 2rem auto;
    max-width: 900px;
}

/* Remove Streamlit default block padding */
.block-container { padding: 0 !important; }
section.main > div { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="shell">
<header class="site-header">
    <div>
        <div class="logo-mark">◈ Intelligence Platform</div>
        <div class="brand-name">Meri<em>dian</em></div>
    </div>
    <div class="header-meta">
        Multi-Agent Research System<br>
        v2.0 · Powered by AI
    </div>
</header>
""", unsafe_allow_html=True)

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="hero">
    <div class="hero-eyebrow">Deep Market Intelligence</div>
    <h1 class="hero-headline">
        Uncover the forces<br>shaping <em>your market</em>
    </h1>
    <p class="hero-sub">
        Four specialized AI agents work in concert — analysing industries, benchmarking competitors,
        tracking trends, and distilling findings into a publication-ready report.
    </p>
</section>
""", unsafe_allow_html=True)

# ── Input card ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="input-card">
    <span class="input-label">Research Topic</span>
""", unsafe_allow_html=True)

topic = st.text_input(
    label="topic",
    placeholder="e.g. Generative AI in Healthcare Diagnostics",
    key="topic_input",
    label_visibility="collapsed",
)

st.markdown("</div>", unsafe_allow_html=True)

run_clicked = st.button("◈ Initiate Research", use_container_width=False)

# ── Validation & agent workflow ─────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    banned_words = ["sex", "porn", "terror", "kill"]
    if any(word in topic.lower() for word in banned_words):
        st.error("This topic is not permitted. Please enter a business or market-related topic.")
        st.stop()

    if len(topic.split()) < 2:
        st.warning("Please enter a more descriptive research topic (e.g. 'AI in Healthcare Market').")
        st.stop()

    st.markdown('<div class="workflow-shell">', unsafe_allow_html=True)

    progress = st.progress(0)

    status1 = st.empty()
    status1.markdown("""
    <div class="agent-step">
        <span class="dot"></span>
        Industry Research Agent — mapping the competitive landscape…
    </div>""", unsafe_allow_html=True)
    progress.progress(20)

    status2 = st.empty()
    status2.markdown("""
    <div class="agent-step" style="animation-delay:0.1s">
        <span class="dot"></span>
        Competitor Analysis Agent — profiling key players &amp; positioning…
    </div>""", unsafe_allow_html=True)
    progress.progress(45)

    status3 = st.empty()
    status3.markdown("""
    <div class="agent-step" style="animation-delay:0.2s">
        <span class="dot"></span>
        Market Trends Agent — extracting signals from the noise…
    </div>""", unsafe_allow_html=True)
    progress.progress(70)

    status4 = st.empty()
    status4.markdown("""
    <div class="agent-step" style="animation-delay:0.3s">
        <span class="dot"></span>
        Synthesis Agent — composing final intelligence report…
    </div>""", unsafe_allow_html=True)
    progress.progress(88)

    with st.spinner("Agents collaborating · please wait…"):
        st.session_state["report"] = run_market_research(topic)
        st.session_state["topic"] = topic

    progress.progress(100)
    st.markdown('</div>', unsafe_allow_html=True)
    st.success("✦ Analysis complete — your report is ready below.")

# ── Report display ───────────────────────────────────────────────────────────
if "report" in st.session_state:
    report = st.session_state["report"]
    saved_topic = st.session_state.get("topic", "")

    st.markdown(f"""
    <div class="report-header">
        <div class="report-title">Intelligence Report</div>
        <div class="report-badge">◈ {saved_topic[:40] + "…" if len(saved_topic) > 40 else saved_topic}</div>
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        label="report_output",
        value=report,
        height=520,
        label_visibility="collapsed",
    )

    filename = export_pdf(report)
    with open(filename, "rb") as f:
        st.download_button(
            label="◈ Download Full Report · PDF",
            data=f,
            file_name=filename,
            mime="application/pdf",
        )

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<footer class="site-footer">
    <span>Meridian · Market Intelligence Platform</span>
    <span>Confidential · AI-Generated Research</span>
</footer>
</div>
""", unsafe_allow_html=True)
