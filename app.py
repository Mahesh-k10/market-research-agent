import streamlit as st
from agents.orchestrator import run_market_research
from tools.pdf_export import export_pdf

st.title("Market Research AI")

topic = st.text_input("Enter Research Topic")

# Run research
if st.button("Run Research"):

    # ---- Input Validation ----
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    banned_words = ["sex", "porn", "terror", "kill"]

    if any(word in topic.lower() for word in banned_words):
        st.error("This topic is not allowed. Please enter a business or market-related topic.")
        st.stop()

    if len(topic.split()) < 2:
        st.warning("Please enter a more descriptive research topic (e.g., 'AI in Healthcare Market').")
        st.stop()

    # ---- Agent Progress Display ----
    st.subheader("AI Agent Workflow")

    progress = st.progress(0)

    status1 = st.empty()
    status1.write("🔎 Running Industry Research Agent...")
    progress.progress(25)

    status2 = st.empty()
    status2.write("🏢 Running Competitor Analysis Agent...")
    progress.progress(50)

    status3 = st.empty()
    status3.write("📈 Running Market Trends Agent...")
    progress.progress(75)

    status4 = st.empty()
    status4.write("📝 Generating Final Report...")
    progress.progress(90)

    # ---- Run Agents ----
    with st.spinner("Running AI agents..."):
        st.session_state["report"] = run_market_research(topic)

    progress.progress(100)

    st.success("Research completed")


# ---- Show Report ----
if "report" in st.session_state:

    report = st.session_state["report"]

    st.subheader("Market Research Report")

    st.text_area("Report", report, height=500)

    # ---- Generate PDF ----
    filename = export_pdf(report)

    with open(filename, "rb") as f:
        st.download_button(
            label="📄 Download PDF",
            data=f,
            file_name=filename,
            mime="application/pdf"
        )