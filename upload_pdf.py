import streamlit as st
import os
import logging

# Adjust system path for imports
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agent import build_graph

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/langgraph.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Streamlit App
st.title("LexiAgent: AI-Powered Legal Document Analyzer")

# Sidebar for PDF upload
with st.sidebar:
    st.header("Upload Legal Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded: {uploaded_file.name}")

# Main page content
if uploaded_file is not None:
    with st.spinner("Analyzing document..."):
        agent = build_graph()
        result = agent.invoke({
            "file_path": file_path,
            "query": "What are the key terms and risks in this document?"
        })

    # Display results
    st.subheader("Analysis Results")

    # Document Type
    st.markdown("### 📄 Document Type")
    doc_type = result["doc_type"]  # No default, assuming always present
    st.write(f"- {doc_type}")

    # Found Clauses
    st.markdown("### 📌 Found Clauses")
    clauses = result["clauses"]  # Assuming this is always returned
    for clause, detail in clauses.items():
        st.write(f"- **{clause}**: {detail}")

    # Summary
    st.markdown("### 📝 Summary")
    doc_summary = result["doc_summary"]  # Assuming always a string
    bullets = [line.strip() for line in doc_summary.split("\n") if line.strip().startswith("-")]
    for bullet in bullets:
        st.write(bullet)

    # Clause Summaries
    st.markdown("### 📑 Clause Summaries")
    clause_summary = result["clause_summary"]  # Assuming always a dict
    overall_summary = clause_summary["overall_summary"]
    st.write(f"- {overall_summary}")
    clause_summaries = clause_summary["clause_summaries"]
    for clause, summary in clause_summaries.items():
        st.write(f"- **{clause}**: {summary}")

    # Risks
    st.markdown("### ⚠️ Risks")
    risks = result["risks"]  # Assuming always a dict
    # Ambiguous Clauses
    st.markdown("#### Ambiguous Clauses")
    ambiguous_clauses = risks["ambiguous_clauses"]
    for clause, issue in ambiguous_clauses.items():
        st.write(f"- **{clause}**: {issue}")
    # Suggestions
    st.markdown("#### Suggestions")
    suggestions = risks["suggestions"]
    for clause, suggestion in suggestions.items():
        st.write(f"- **{clause}**: {suggestion}")

    # Error (if any)
    if "error" in result:
        st.error(f"❌ Error: {result['error']}")
else:
    st.info("Please upload a PDF file to analyze.")