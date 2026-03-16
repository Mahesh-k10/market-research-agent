import streamlit as st
from agents.orchestrator import run_market_research
from tools.pdf_export import export_pdf

st.title("Market Research AI")

topic = st.text_input("Enter Research Topic")

# Run research
if st.button("Run Research"):
    with st.spinner("Running AI agents..."):
        st.session_state["report"] = run_market_research(topic)

    st.success("Research completed")


# Show report if it exists
if "report" in st.session_state:

    report = st.session_state["report"]

    st.text_area("Report", report, height=500)

    # Generate PDF
    filename = export_pdf(report)

    with open(filename, "rb") as f:
        st.download_button(
            label="📄 Download PDF",
            data=f,
            file_name=filename,
            mime="application/pdf"
        )