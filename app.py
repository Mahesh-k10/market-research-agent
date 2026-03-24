import streamlit as st
from agents.orchestrator import run_market_research
from tools.pdf_export import export_pdf

st.set_page_config(
    page_title="Nexus Intelligence · Market Research",
    page_icon="🔷",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

/* ══════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stMain"] {
    background: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #0f1923 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

/* Main container */
.block-container {
    padding: 0 !important;
    max-width: 860px !important;
    margin: 0 auto !important;
}

section.main > div { padding: 0 !important; }

/* ══════════════════════════════════════════
   TOP NAV BAR
══════════════════════════════════════════ */
.nx-navbar {
    background: #ffffff;
    border-bottom: 1px solid #e8edf2;
    padding: 0 2rem;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 12px rgba(0,0,0,0.06);
}

.nx-logo {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.nx-logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #0052cc 0%, #0073e6 100%);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    color: white;
    font-weight: 800;
    letter-spacing: -0.05em;
    box-shadow: 0 4px 12px rgba(0,82,204,0.3);
}

.nx-logo-text {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f1923;
    letter-spacing: -0.02em;
}

.nx-logo-text span {
    color: #0052cc;
}

.nx-nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: #5a6a7a;
    letter-spacing: 0.01em;
}

.nx-nav-badge {
    background: #f0f6ff;
    color: #0052cc;
    border: 1px solid #cce0ff;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════
   HERO BANNER
══════════════════════════════════════════ */
.nx-hero {
    background: linear-gradient(135deg, #f7faff 0%, #eef4ff 50%, #f0f7ff 100%);
    border-bottom: 1px solid #dde8f5;
    padding: 3.5rem 2.5rem 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

/* Decorative circles */
.nx-hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(0,82,204,0.08) 0%, transparent 65%);
    border-radius: 50%;
}
.nx-hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -40px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(0,115,230,0.06) 0%, transparent 65%);
    border-radius: 50%;
}

.nx-hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: #fff;
    border: 1px solid #cce0ff;
    color: #0052cc;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    margin-bottom: 1.4rem;
    box-shadow: 0 2px 8px rgba(0,82,204,0.08);
}

.nx-hero-tag::before {
    content: '';
    width: 6px; height: 6px;
    background: #0052cc;
    border-radius: 50%;
    animation: blink 1.6s ease infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.nx-hero-h1 {
    font-size: clamp(1.9rem, 4vw, 2.9rem);
    font-weight: 800;
    color: #0f1923;
    line-height: 1.18;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}

.nx-hero-h1 em {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-weight: 400;
    color: #0052cc;
}

.nx-hero-sub {
    font-size: 0.95rem;
    color: #4a5d70;
    line-height: 1.75;
    max-width: 520px;
    margin: 0 auto 2rem;
    font-weight: 400;
}

/* Stats row */
.nx-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    flex-wrap: wrap;
}

.nx-stat {
    text-align: center;
}

.nx-stat-num {
    font-size: 1.4rem;
    font-weight: 800;
    color: #0052cc;
    letter-spacing: -0.03em;
    line-height: 1;
}

.nx-stat-label {
    font-size: 0.68rem;
    color: #7a8fa0;
    font-weight: 500;
    margin-top: 0.2rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════
   CONTENT AREA
══════════════════════════════════════════ */
.nx-content {
    padding: 2.5rem 2.5rem 0;
}

/* Section label */
.nx-section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #0052cc;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.nx-section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e0eaf5;
}

.nx-section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f1923;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
}

.nx-section-desc {
    font-size: 0.84rem;
    color: #5a6e80;
    margin-bottom: 1.25rem;
    line-height: 1.6;
}

/* ══════════════════════════════════════════
   TEXT INPUT OVERRIDE
══════════════════════════════════════════ */
[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stTextInput"] > div > div {
    background: #ffffff !important;
    border: 1.5px solid #c8d8ea !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(0,82,204,0.05) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

[data-testid="stTextInput"] > div > div:focus-within {
    border-color: #0052cc !important;
    box-shadow: 0 0 0 3px rgba(0,82,204,0.1), 0 2px 8px rgba(0,82,204,0.08) !important;
}

[data-testid="stTextInput"] > div > div > input {
    background: transparent !important;
    color: #0f1923 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0.85rem 1.1rem !important;
    border: none !important;
    box-shadow: none !important;
    caret-color: #0052cc !important;
}

[data-testid="stTextInput"] > div > div > input::placeholder {
    color: #9ab0c4 !important;
    font-weight: 400 !important;
}

/* ══════════════════════════════════════════
   PRIMARY BUTTON
══════════════════════════════════════════ */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0052cc 0%, #0073e6 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 0.9rem 2rem !important;
    border-radius: 10px !important;
    margin-top: 0.75rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 16px rgba(0,82,204,0.3) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #0047b3 0%, #0066cc 100%) !important;
    box-shadow: 0 6px 20px rgba(0,82,204,0.4) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) scale(0.99) !important;
}

/* ══════════════════════════════════════════
   AGENT CARDS
══════════════════════════════════════════ */
.nx-agents-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #0f1923;
    letter-spacing: 0.02em;
    margin: 1.5rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.agent-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #f7faff;
    border: 1px solid #dce8f8;
    border-left: 3px solid #0052cc;
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.5rem;
    animation: cardIn 0.3s ease both;
}

@keyframes cardIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

.agent-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #0052cc, #0073e6);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(0,82,204,0.2);
}

.agent-info { flex: 1; }

.agent-name {
    font-size: 0.78rem;
    font-weight: 700;
    color: #0f1923;
    margin-bottom: 0.1rem;
}

.agent-desc {
    font-size: 0.68rem;
    color: #6a7f90;
    font-weight: 400;
}

.agent-status {
    font-size: 0.62rem;
    font-weight: 700;
    color: #0052cc;
    background: #e8f0fe;
    padding: 0.2rem 0.55rem;
    border-radius: 20px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    animation: statusPulse 1.4s ease infinite;
}

@keyframes statusPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}

/* ══════════════════════════════════════════
   PROGRESS BAR
══════════════════════════════════════════ */
[data-testid="stProgress"] {
    margin: 1rem 0 0.25rem !important;
}

[data-testid="stProgress"] > div {
    background: #e8f0fe !important;
    border-radius: 4px !important;
    height: 5px !important;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #0052cc, #4da3ff) !important;
    border-radius: 4px !important;
    transition: width 0.6s ease !important;
}

/* ══════════════════════════════════════════
   ALERTS
══════════════════════════════════════════ */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: none !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* ══════════════════════════════════════════
   SPINNER
══════════════════════════════════════════ */
[data-testid="stSpinner"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.78rem !important;
    color: #0052cc !important;
    font-weight: 600 !important;
}

/* ══════════════════════════════════════════
   REPORT SECTION
══════════════════════════════════════════ */
.nx-report-header {
    background: linear-gradient(135deg, #0052cc 0%, #0073e6 100%);
    border-radius: 12px 12px 0 0;
    padding: 1.4rem 1.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nx-report-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.01em;
}

.nx-report-sub {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.7);
    margin-top: 0.2rem;
    font-weight: 400;
}

.nx-report-icon {
    width: 40px; height: 40px;
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

/* TEXT AREA */
[data-testid="stTextArea"] label { display: none !important; }

[data-testid="stTextArea"] > div {
    border-radius: 0 0 12px 12px !important;
    border: 1px solid #dce8f8 !important;
    border-top: none !important;
    overflow: hidden !important;
}

[data-testid="stTextArea"] > div > div {
    background: #f9fbff !important;
}

[data-testid="stTextArea"] textarea {
    background: #f9fbff !important;
    border: none !important;
    border-radius: 0 !important;
    color: #1a2a3a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.875rem !important;
    line-height: 1.85 !important;
    padding: 1.4rem 1.6rem !important;
    box-shadow: none !important;
}

[data-testid="stTextArea"] textarea:focus {
    box-shadow: none !important;
    border: none !important;
}

/* ══════════════════════════════════════════
   DOWNLOAD BUTTON
══════════════════════════════════════════ */
[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    background: #ffffff !important;
    border: 1.5px solid #0052cc !important;
    color: #0052cc !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 0.85rem 2rem !important;
    border-radius: 10px !important;
    margin-top: 0.75rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(0,82,204,0.1) !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: #f0f6ff !important;
    box-shadow: 0 4px 16px rgba(0,82,204,0.18) !important;
    transform: translateY(-1px) !important;
}

/* ══════════════════════════════════════════
   FEATURE CARDS (below hero)
══════════════════════════════════════════ */
.nx-features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
    border: 1px solid #e0eaf5;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2rem;
}

.nx-feature {
    padding: 1.2rem 1.3rem;
    background: #ffffff;
    border-right: 1px solid #e0eaf5;
}
.nx-feature:last-child { border-right: none; }

.nx-feature-icon {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.nx-feature-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #0f1923;
    margin-bottom: 0.3rem;
    letter-spacing: -0.01em;
}

.nx-feature-desc {
    font-size: 0.7rem;
    color: #6a7f90;
    line-height: 1.55;
}

/* ══════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════ */
.nx-divider {
    border: none;
    border-top: 1px solid #e8edf2;
    margin: 2rem 0;
}

/* ══════════════════════════════════════════
   FOOTER
══════════════════════════════════════════ */
.nx-footer {
    background: #f4f7fb;
    border-top: 1px solid #e0eaf5;
    padding: 1.75rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 3rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.nx-footer-brand {
    display: flex;
    align-items: center;
    gap: 0.55rem;
}

.nx-footer-logo {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #0052cc, #0073e6);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    color: white;
    font-weight: 800;
}

.nx-footer-name {
    font-size: 0.82rem;
    font-weight: 700;
    color: #0f1923;
}

.nx-footer-copy {
    font-size: 0.68rem;
    color: #8a9aaa;
    font-weight: 400;
}

.nx-footer-links {
    display: flex;
    gap: 1.5rem;
    font-size: 0.7rem;
    color: #6a7f90;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════
st.markdown("""
<nav class="nx-navbar">
    <div class="nx-logo">
        <div class="nx-logo-icon">NX</div>
        <div class="nx-logo-text">Nexus <span>Intelligence</span></div>
    </div>
    <div class="nx-nav-links">
        <span>Solutions</span>
        <span>Industries</span>
        <span>Insights</span>
        <span class="nx-nav-badge">🔷 AI Platform</span>
    </div>
</nav>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# HERO
# ══════════════════════════════════════════
st.markdown("""
<div class="nx-hero">
    <div class="nx-hero-tag">AI-Powered Research Platform</div>
    <div class="nx-hero-h1">
        Market Intelligence,<br><em>Redefined by AI</em>
    </div>
    <p class="nx-hero-sub">
        Deploy four specialized AI agents to uncover competitive insights, emerging trends,
        and strategic opportunities — delivered as a boardroom-ready report in minutes.
    </p>
    <div class="nx-stats">
        <div class="nx-stat">
            <div class="nx-stat-num">4</div>
            <div class="nx-stat-label">AI Agents</div>
        </div>
        <div class="nx-stat">
            <div class="nx-stat-num">360°</div>
            <div class="nx-stat-label">Market Coverage</div>
        </div>
        <div class="nx-stat">
            <div class="nx-stat-num">&lt;3 min</div>
            <div class="nx-stat-label">Research Time</div>
        </div>
        <div class="nx-stat">
            <div class="nx-stat-num">PDF</div>
            <div class="nx-stat-label">Export Ready</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# FEATURE CARDS
# ══════════════════════════════════════════
st.markdown("""
<div style="padding: 2rem 2.5rem 0;">
<div class="nx-features">
    <div class="nx-feature">
        <div class="nx-feature-icon">🏭</div>
        <div class="nx-feature-title">Industry Deep Dive</div>
        <div class="nx-feature-desc">Comprehensive sector analysis with market sizing and key dynamics</div>
    </div>
    <div class="nx-feature">
        <div class="nx-feature-icon">🎯</div>
        <div class="nx-feature-title">Competitor Intelligence</div>
        <div class="nx-feature-desc">Benchmark key players, positioning maps, and strategic gaps</div>
    </div>
    <div class="nx-feature">
        <div class="nx-feature-icon">📈</div>
        <div class="nx-feature-title">Trend Forecasting</div>
        <div class="nx-feature-desc">Emerging signals, disruption indicators, and growth vectors</div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════
st.markdown("""
<div class="nx-content">
    <div class="nx-section-label">Start Your Research</div>
    <div class="nx-section-title">What market do you want to explore?</div>
    <div class="nx-section-desc">
        Enter a specific topic for the most accurate intelligence. Include industry verticals,
        geography, or technology focus for sharper results.
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding: 0 2.5rem;">', unsafe_allow_html=True)

    topic = st.text_input(
        label="Research Topic",
        placeholder="e.g.  Electric Vehicle Battery Market in Southeast Asia",
        label_visibility="collapsed",
    )

    run_clicked = st.button("🔷  Run AI Research   →")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# VALIDATION & AGENT WORKFLOW
# ══════════════════════════════════════════
if run_clicked:
    if not topic.strip():
        st.warning("⚠️  Please enter a research topic before running.")
        st.stop()

    banned_words = ["sex", "porn", "terror", "kill"]
    if any(word in topic.lower() for word in banned_words):
        st.error("🚫  This topic is not permitted. Please enter a business or market-related topic.")
        st.stop()

    if len(topic.split()) < 2:
        st.warning("⚠️  Please be more specific (e.g. 'EV Battery Market in India').")
        st.stop()

    st.markdown('<div style="padding: 0 2.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="nx-agents-title">⚡ AI Agent Workflow — Running</div>', unsafe_allow_html=True)

    progress = st.progress(0)

    s1 = st.empty()
    s1.markdown("""
    <div class="agent-card">
        <div class="agent-icon">🏭</div>
        <div class="agent-info">
            <div class="agent-name">Industry Research Agent</div>
            <div class="agent-desc">Mapping sector landscape, market size & key dynamics</div>
        </div>
        <div class="agent-status">Running</div>
    </div>""", unsafe_allow_html=True)
    progress.progress(22)

    s2 = st.empty()
    s2.markdown("""
    <div class="agent-card" style="animation-delay:0.1s">
        <div class="agent-icon">🎯</div>
        <div class="agent-info">
            <div class="agent-name">Competitor Analysis Agent</div>
            <div class="agent-desc">Profiling key players, positioning & strategic moves</div>
        </div>
        <div class="agent-status">Running</div>
    </div>""", unsafe_allow_html=True)
    progress.progress(46)

    s3 = st.empty()
    s3.markdown("""
    <div class="agent-card" style="animation-delay:0.2s">
        <div class="agent-icon">📈</div>
        <div class="agent-info">
            <div class="agent-name">Market Trends Agent</div>
            <div class="agent-desc">Extracting emerging signals, disruptions & growth vectors</div>
        </div>
        <div class="agent-status">Running</div>
    </div>""", unsafe_allow_html=True)
    progress.progress(70)

    s4 = st.empty()
    s4.markdown("""
    <div class="agent-card" style="animation-delay:0.3s">
        <div class="agent-icon">📝</div>
        <div class="agent-info">
            <div class="agent-name">Synthesis Agent</div>
            <div class="agent-desc">Composing executive-grade intelligence report</div>
        </div>
        <div class="agent-status">Running</div>
    </div>""", unsafe_allow_html=True)
    progress.progress(88)

    with st.spinner("AI agents collaborating — compiling your intelligence report…"):
        st.session_state["report"] = run_market_research(topic)
        st.session_state["topic"] = topic

    progress.progress(100)
    st.markdown('</div>', unsafe_allow_html=True)
    st.success("✅  Research complete! Your intelligence report is ready below.")

# ══════════════════════════════════════════
# REPORT OUTPUT
# ══════════════════════════════════════════
if "report" in st.session_state:
    report = st.session_state["report"]
    saved_topic = st.session_state.get("topic", "Research Report")
    badge = (saved_topic[:45] + "…") if len(saved_topic) > 48 else saved_topic

    st.markdown('<div style="padding: 0 2.5rem;">', unsafe_allow_html=True)
    st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="nx-report-header">
        <div>
            <div class="nx-report-title">Intelligence Report</div>
            <div class="nx-report-sub">{badge}</div>
        </div>
        <div class="nx-report-icon">📊</div>
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
            label="⬇️  Download Full Report as PDF",
            data=f,
            file_name=filename,
            mime="application/pdf",
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown("""
<div class="nx-footer">
    <div class="nx-footer-brand">
        <div class="nx-footer-logo">NX</div>
        <div>
            <div class="nx-footer-name">Nexus Intelligence</div>
            <div class="nx-footer-copy">© 2025 · AI Market Research Platform</div>
        </div>
    </div>
    <div class="nx-footer-links">
        <span>Privacy Policy</span>
        <span>Terms of Use</span>
        <span>Contact</span>
    </div>
</div>
""", unsafe_allow_html=True)
