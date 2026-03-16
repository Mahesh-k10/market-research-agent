import streamlit as st
from agents.orchestrator import run_market_research
from tools.pdf_export import export_pdf

st.title("Market Research AI")

topic = st.text_input("Enter Research Topic")

if st.button("Run Research"):

    with st.spinner("Running AI agents..."):
        report = run_market_research(topic)

    st.success("Research completed")

    st.text_area("Report", report, height=500)

    if st.button("Export PDF"):
        filename = export_pdf(report)

        with open(filename, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name=filename
            )