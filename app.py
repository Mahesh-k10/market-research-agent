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

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stMain"] {
    background: #f5f7fa !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #0f1923 !important;
}

#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

.block-container {
    padding: 0 !important;
    max-width: 860px !important;
    margin: 0 auto !important;
}
section.main > div { padding: 0 !important; }

/* ── NAVBAR ── */
.nx-navbar {
    background: #fff;
    border-bottom: 1px solid #e4e9f0;
    padding: 0 1.75rem;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}
.nx-logo { display: flex; align-items: center; gap: 0.55rem; }
.nx-logo-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #0052cc 0%, #0073e6 100%);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 800; color: #fff;
    box-shadow: 0 3px 10px rgba(0,82,204,0.28);
}
.nx-logo-text { font-size: 0.95rem; font-weight: 700; color: #0f1923; letter-spacing: -0.02em; }
.nx-logo-text span { color: #0052cc; }
.nx-nav-right { display: flex; align-items: center; gap: 1.5rem; }
.nx-nav-link { font-size: 0.78rem; font-weight: 500; color: #5a6a7a; }
.nx-nav-badge {
    background: #eef4ff; color: #0052cc;
    border: 1px solid #c0d8ff;
    font-size: 0.62rem; font-weight: 700;
    padding: 0.22rem 0.65rem; border-radius: 20px;
    letter-spacing: 0.06em; text-transform: uppercase;
}

/* ── COMPACT HERO ── */
.nx-hero {
    background: linear-gradient(135deg, #eef4ff 0%, #f0f7ff 100%);
    border-bottom: 1px solid #dce8f5;
    padding: 1.6rem 2rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
}
.nx-hero-left { flex: 1; }
.nx-hero-tag {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: #fff; border: 1px solid #c0d8ff; color: #0052cc;
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 0.22rem 0.7rem;
    border-radius: 20px; margin-bottom: 0.6rem;
}
.nx-hero-tag-dot {
    width: 5px; height: 5px; background: #0052cc;
    border-radius: 50%; animation: blink 1.6s ease infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

.nx-hero-h1 {
    font-size: 1.55rem; font-weight: 800; color: #0f1923;
    line-height: 1.2; letter-spacing: -0.03em; margin-bottom: 0.35rem;
}
.nx-hero-h1 em {
    font-family: 'Playfair Display', serif;
    font-style: italic; font-weight: 400; color: #0052cc;
}
.nx-hero-sub {
    font-size: 0.78rem; color: #4a5d70; line-height: 1.6; font-weight: 400;
}
.nx-hero-stats {
    display: flex; flex-direction: column; gap: 0.5rem;
    background: #fff; border: 1px solid #dce8f5;
    border-radius: 12px; padding: 1rem 1.2rem;
    min-width: 160px;
    box-shadow: 0 2px 12px rgba(0,82,204,0.07);
}
.nx-stat-row { display: flex; align-items: center; gap: 0.6rem; }
.nx-stat-num { font-size: 1rem; font-weight: 800; color: #0052cc; min-width: 40px; letter-spacing: -0.02em; }
.nx-stat-label { font-size: 0.65rem; color: #7a8fa0; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

/* ── MAIN CARD ── */
.nx-card {
    background: #fff;
    border: 1px solid #e4e9f0;
    border-radius: 14px;
    padding: 1.6rem 1.75rem 1.4rem;
    margin: 1.25rem 1.5rem 0;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
}
.nx-card-title {
    font-size: 0.95rem; font-weight: 700; color: #0f1923;
    letter-spacing: -0.01em; margin-bottom: 0.2rem;
}
.nx-card-desc {
    font-size: 0.75rem; color: #6a7f90; margin-bottom: 1rem; line-height: 1.5;
}

/* ── INPUT ── */
[data-testid="stTextInput"] label { display: none !important; }
[data-testid="stTextInput"] > div > div {
    background: #fff !important;
    border: 1.5px solid #c8d8ea !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 6px rgba(0,82,204,0.05) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: #0052cc !important;
    box-shadow: 0 0 0 3px rgba(0,82,204,0.1) !important;
}
[data-testid="stTextInput"] > div > div > input {
    background: transparent !important;
    color: #0f1923 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 0.78rem 1rem !important;
    border: none !important;
    box-shadow: none !important;
    caret-color: #0052cc !important;
}
[data-testid="stTextInput"] > div > div > input::placeholder {
    color: #9ab0c4 !important; font-weight: 400 !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0052cc 0%, #0073e6 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    padding: 0.82rem 2rem !important;
    border-radius: 10px !important;
    margin-top: 0.65rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 14px rgba(0,82,204,0.28) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #0047b3 0%, #0066cc 100%) !important;
    box-shadow: 0 6px 20px rgba(0,82,204,0.38) !important;
    transform: translateY(-1px) !important;
}

/* ── FEATURE PILLS ── */
.nx-pills {
    display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.9rem 0 0;
}
.nx-pill {
    background: #f0f6ff; border: 1px solid #cce0ff; color: #0052cc;
    font-size: 0.67rem; font-weight: 600; padding: 0.28rem 0.7rem;
    border-radius: 20px; letter-spacing: 0.03em;
}

/* ── PROGRESS ── */
[data-testid="stProgress"] { margin: 1rem 0 0.25rem !important; }
[data-testid="stProgress"] > div {
    background: #e8f0fe !important; border-radius: 4px !important; height: 4px !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #0052cc, #4da3ff) !important;
    border-radius: 4px !important; transition: width 0.5s ease !important;
}

/* ── AGENT CARDS ── */
.agent-card {
    display: flex; align-items: center; gap: 0.85rem;
    background: #f7faff; border: 1px solid #dce8f8;
    border-left: 3px solid #0052cc;
    border-radius: 8px; padding: 0.72rem 1rem;
    margin-bottom: 0.45rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    animation: cardIn 0.3s ease both;
}
@keyframes cardIn { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
.agent-icon {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #0052cc, #0073e6);
    border-radius: 7px; display: flex; align-items: center;
    justify-content: center; font-size: 0.8rem; flex-shrink: 0;
}
.agent-name { font-size: 0.76rem; font-weight: 700; color: #0f1923; }
.agent-desc { font-size: 0.65rem; color: #6a7f90; margin-top: 0.08rem; }
.agent-status {
    font-size: 0.6rem; font-weight: 700; color: #0052cc;
    background: #e8f0fe; padding: 0.18rem 0.5rem;
    border-radius: 20px; letter-spacing: 0.05em; text-transform: uppercase;
    animation: statusPulse 1.4s ease infinite; margin-left: auto; flex-shrink: 0;
}
@keyframes statusPulse { 0%,100%{opacity:1} 50%{opacity:0.45} }

/* ── ALERTS ── */
[data-testid="stAlert"] {
    margin: 0 1.5rem !important;
    border-radius: 8px !important; border: none !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
}
[data-testid="stSpinner"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.76rem !important; color: #0052cc !important; font-weight: 600 !important;
}

/* ── REPORT ── */
.nx-report-header {
    background: linear-gradient(135deg, #0052cc 0%, #0073e6 100%);
    border-radius: 12px 12px 0 0;
    padding: 1.1rem 1.4rem;
    display: flex; align-items: center; justify-content: space-between;
}
.nx-report-title { font-size: 0.92rem; font-weight: 700; color: #fff; }
.nx-report-sub { font-size: 0.68rem; color: rgba(255,255,255,0.68); margin-top: 0.15rem; }
.nx-report-icon {
    width: 36px; height: 36px; background: rgba(255,255,255,0.15);
    border-radius: 9px; display: flex; align-items: center;
    justify-content: center; font-size: 1.1rem;
}

[data-testid="stTextArea"] label { display: none !important; }
[data-testid="stTextArea"] > div {
    border-radius: 0 0 12px 12px !important;
    border: 1px solid #dce8f8 !important;
    border-top: none !important; overflow: hidden !important;
}
[data-testid="stTextArea"] textarea {
    background: #f9fbff !important; border: none !important;
    color: #1a2a3a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.855rem !important; line-height: 1.82 !important;
    padding: 1.2rem 1.4rem !important; box-shadow: none !important;
}
[data-testid="stTextArea"] textarea:focus { box-shadow: none !important; border: none !important; }

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    background: #fff !important;
    border: 1.5px solid #0052cc !important;
    color: #0052cc !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.8rem !important; font-weight: 700 !important;
    padding: 0.8rem 2rem !important; border-radius: 10px !important;
    margin-top: 0.65rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(0,82,204,0.08) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #f0f6ff !important;
    box-shadow: 0 4px 14px rgba(0,82,204,0.16) !important;
    transform: translateY(-1px) !important;
}

/* ── DIVIDER ── */
.nx-divider { border: none; border-top: 1px solid #e4e9f0; margin: 1.25rem 0; }

/* ── FOOTER ── */
.nx-footer {
    background: #fff; border-top: 1px solid #e4e9f0;
    padding: 1.25rem 1.75rem;
    display: flex; align-items: center; justify-content: space-between;
    margin-top: 2rem; flex-wrap: wrap; gap: 0.75rem;
}
.nx-footer-brand { display: flex; align-items: center; gap: 0.5rem; }
.nx-footer-logo {
    width: 26px; height: 26px;
    background: linear-gradient(135deg, #0052cc, #0073e6);
    border-radius: 6px; display: flex; align-items: center;
    justify-content: center; font-size: 0.65rem; color: #fff; font-weight: 800;
}
.nx-footer-name { font-size: 0.78rem; font-weight: 700; color: #0f1923; }
.nx-footer-copy { font-size: 0.63rem; color: #8a9aaa; }
.nx-footer-links { display: flex; gap: 1.25rem; font-size: 0.67rem; color: #6a7f90; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ──────────────────────────────────────────────────────────────────
st.markdown("""
<nav class="nx-navbar">
    <div class="nx-logo">
        <div class="nx-logo-icon">NX</div>
        <div class="nx-logo-text">Nexus <span>Intelligence</span></div>
    </div>
    <div class="nx-nav-right">
        <span class="nx-nav-link">Solutions</span>
        <span class="nx-nav-link">Industries</span>
        <span class="nx-nav-link">Insights</span>
        <span class="nx-nav-badge">🔷 AI Platform</span>
    </div>
</nav>
""", unsafe_allow_html=True)

# ── COMPACT HERO ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="nx-hero">
    <div class="nx-hero-left">
        <div class="nx-hero-tag">
            <span class="nx-hero-tag-dot"></span>
            AI-Powered Research Platform
        </div>
        <div class="nx-hero-h1">Market Intelligence,<br><em>Redefined by AI</em></div>
        <div class="nx-hero-sub">Four AI agents deliver boardroom-ready<br>market research in minutes.</div>
    </div>
    <div class="nx-hero-stats">
        <div class="nx-stat-row">
            <div class="nx-stat-num">4</div>
            <div class="nx-stat-label">AI Agents</div>
        </div>
        <div class="nx-stat-row">
            <div class="nx-stat-num">360°</div>
            <div class="nx-stat-label">Coverage</div>
        </div>
        <div class="nx-stat-row">
            <div class="nx-stat-num">&lt;3 min</div>
            <div class="nx-stat-label">Research Time</div>
        </div>
        <div class="nx-stat-row">
            <div class="nx-stat-num">PDF</div>
            <div class="nx-stat-label">Export Ready</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SEARCH CARD (immediately visible) ───────────────────────────────────────
st.markdown("""
<div class="nx-card">
    <div class="nx-card-title">🔍 &nbsp;Start Your Research</div>
    <div class="nx-card-desc">Enter a market topic — include industry, geography or technology for sharper insights.</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding: 0 1.5rem;">', unsafe_allow_html=True)

    topic = st.text_input(
        label="topic",
        placeholder="e.g.  Electric Vehicle Battery Market in Southeast Asia",
        label_visibility="collapsed",
    )
    run_clicked = st.button("🔷  Run AI Research  →")

    st.markdown("""
    <div class="nx-pills">
        <span class="nx-pill">🏭 Industry Analysis</span>
        <span class="nx-pill">🎯 Competitor Intel</span>
        <span class="nx-pill">📈 Trend Signals</span>
        <span class="nx-pill">📝 Executive Report</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── VALIDATION & AGENTS ──────────────────────────────────────────────────────
if run_clicked:
    if not topic.strip():
        st.warning("⚠️  Please enter a research topic before running.")
        st.stop()
    banned = ["sex", "porn", "terror", "kill"]
    if any(w in topic.lower() for w in banned):
        st.error("🚫  This topic is not permitted. Please enter a business or market-related topic.")
        st.stop()
    if len(topic.split()) < 2:
        st.warning("⚠️  Please be more specific (e.g. 'EV Battery Market in India').")
        st.stop()

    st.markdown('<div style="padding: 0 1.5rem;">', unsafe_allow_html=True)
    st.markdown('<hr class="nx-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#0f1923;margin-bottom:0.65rem;">⚡ Agent Workflow — Running</div>', unsafe_allow_html=True)

    progress = st.progress(0)

    s1 = st.empty()
    s1.markdown("""<div class="agent-card"><div class="agent-icon">🏭</div><div><div class="agent-name">Industry Research Agent</div><div class="agent-desc">Mapping sector landscape, market size &amp; key dynamics</div></div><div class="agent-status">Running</div></div>""", unsafe_allow_html=True)
    progress.progress(22)

    s2 = st.empty()
    s2.markdown("""<div class="agent-card"><div class="agent-icon">🎯</div><div><div class="agent-name">Competitor Analysis Agent</div><div class="agent-desc">Profiling key players, positioning &amp; strategic moves</div></div><div class="agent-status">Running</div></div>""", unsafe_allow_html=True)
    progress.progress(46)

    s3 = st.empty()
    s3.markdown("""<div class="agent-card"><div class="agent-icon">📈</div><div><div class="agent-name">Market Trends Agent</div><div class="agent-desc">Extracting emerging signals, disruptions &amp; growth vectors</div></div><div class="agent-status">Running</div></div>""", unsafe_allow_html=True)
    progress.progress(70)

    s4 = st.empty()
    s4.markdown("""<div class="agent-card"><div class="agent-icon">📝</div><div><div class="agent-name">Synthesis Agent</div><div class="agent-desc">Composing executive-grade intelligence report</div></div><div class="agent-status">Running</div></div>""", unsafe_allow_html=True)
    progress.progress(88)

    with st.spinner("AI agents collaborating — compiling your intelligence report…"):
        st.session_state["report"] = run_market_research(topic)
        st.session_state["topic"] = topic

    progress.progress(100)
    st.markdown('</div>', unsafe_allow_html=True)
    st.success("✅  Research complete! Your intelligence report is ready below.")

# ── REPORT ───────────────────────────────────────────────────────────────────
if "report" in st.session_state:
    report = st.session_state["report"]
    saved_topic = st.session_state.get("topic", "Research Report")
    badge = (saved_topic[:45] + "…") if len(saved_topic) > 48 else saved_topic

    st.markdown('<div style="padding: 0 1.5rem;">', unsafe_allow_html=True)
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

    st.text_area(label="report_output", value=report, height=500, label_visibility="collapsed")

    filename = export_pdf(report)
    with open(filename, "rb") as f:
        st.download_button(
            label="⬇️  Download Full Report as PDF",
            data=f, file_name=filename, mime="application/pdf",
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
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
