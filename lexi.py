import streamlit as st
import os, logging
from pdf_agent import build_graph
from utils import utils
from chat_agent import stream_chat_response

# Setup
st.set_page_config(page_title="LexiAgent: Legal Document Assistant", page_icon="📄", layout="wide")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/langgraph.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# CSS
st.markdown("""
<style>
    .main-title {
        color: #FF6B00;
        font-family: 'Trebuchet MS', sans-serif;
        text-align: center;
        margin-bottom: 0;
        font-size: 2.8em;
    }
    .section-block {
        background-color: #fffaf0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #FF6B00;
    }
    .sidebar-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .subheadline {
            font-size: 1.3rem;
            color: #444;
            text-align: center;
        }
    
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #FF6B00;'>🤖 LexiAgent: AI-Powered Legal Document Analyst 📄</h1>", unsafe_allow_html=True)
st.markdown("<div class='subheadline'>Revolutionizing Legal Document Understanding with Generative AI & Autonomous Agents</div>", unsafe_allow_html=True)
# Sidebar
with st.sidebar:
    st.markdown("<div><h1>📎 Upload Legal Document</h1></div>", unsafe_allow_html=True)
    uploaded_file = st.sidebar.file_uploader("📤 **Upload PDF Files**", type=["pdf"], accept_multiple_files=True)
    page_choice = st.radio("🔀 **Select Mode**", ["**📘 LexiAgent - Overview**", "📊 **LexiAgent: Document Analyzer**", "💬 **LexiAgent: AI Assistant**"])

    if uploaded_file:
        os.makedirs("temp", exist_ok=True)
        first_file = uploaded_file[0]  # Get the first uploaded file
        file_path = os.path.join("temp", first_file.name)
        with open(file_path, "wb") as f:
            f.write(first_file.getbuffer())
        st.success(f"✅ Uploaded: {first_file.name}")
    else:
        file_path = None

def home():
    # Custom CSS
    st.markdown("""
    <style>
        .headline {
            font-size: 2.5rem;
            color: #FF6B00;
            font-weight: bold;
            text-align: center;
        }
        .subheadline {
            font-size: 1.3rem;
            color: #444;
            text-align: center;
        }
        .section-title {
            font-size: 1.6rem;
            margin-top: 30px;
            color: #FF6B00;
            border-left: 5px solid #FF6B00;
            padding-left: 10px;
        }
        .info-box {
            # background-color: #fffaf0;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0 30px 0;
            border: 1px solid #f0e5d8;
        }
    </style>
    """, unsafe_allow_html=True)

    # About the Project
    st.markdown("<div class='section-title'>📘 About LexiAgent</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    LexiAgent is an <b>AI-powered autonomous legal document assistant</b> designed to analyze legal contracts, extract important clauses, summarize contents, classify document types, and detect potential risks—all using state-of-the-art Large Language Models (LLMs) and intelligent agent workflows.
    <br><br>
    Whether you're a lawyer, paralegal, contract manager, or startup founder—LexiAgent saves hours of manual reading by transforming legal documents into actionable insights in seconds.
    """, unsafe_allow_html=True)

    # How it Works
    st.markdown("<div class='section-title'>⚙️ How It Works</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    LexiAgent uses a <b>multi-step AI agent workflow</b>, powered by <b>LangGraph</b>, to autonomously:<br><br>
    1. 🧠 <b>Classify</b> the document type.<br>
    2. 🔍 <b>Extract important clauses</b> from the legal content.<br>
    3. 📝 <b>Generate concise summaries</b> of each clause and the full document.<br>
    4. ⚠️ <b>Identify ambiguities and risky clauses</b>.<br>
    5. 💬 Optionally enable a chatbot that understands the document and answers legal queries using <b>RAG (Retrieval-Augmented Generation)</b>.<br><br>

    Each step is managed by specialized tools and autonomous logic, mimicking a human legal assistant—only faster and smarter.
    </div>
    """, unsafe_allow_html=True)

    # Technologies Used
    st.markdown("<div class='section-title'>🧰 Technologies Used</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    1. 🦜 <b>LangGraph</b> – Multi-step autonomous agents and workflows  <br>
    2. 🦙 <b>LLMs</b> – Advanced Large Language Models (Open Source / API)  <br>
    3. 🗂️ <b>PDF Parsing</b> – Converts PDFs into structured, readable text  <br>
    4. 🧾 <b>NLP & Text Processing</b> – Summarization, clause extraction, classification  <br>
    5. 🔗 <b>Retrieval-Augmented Generation (RAG)</b> – For chatbot functionality  <br>
    6. 🌐 <b>Streamlit</b> – Fast and beautiful UI/UX  <br>
    7. 🛠️ <b>Custom Tools</b> – Clause summarizer, risk detector, doc classifier<br>
    </div>
    """, unsafe_allow_html=True)

    # Key Features
    st.markdown("<div class='section-title'>🚀 Key Features</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    1. ✅ <b>Upload and Analyze Legal PDFs</b>  <br>
    2. ✅ <b>Document Classification</b> (e.g., NDA, Service Agreement, Lease)  <br>
    3. ✅ <b>Clause Extraction & Explanation</b>  <br>
    4. ✅ <b>Document and Clause-Level Summaries</b>  <br>
    5. ✅ <b>Risk Detection: Ambiguous Terms, Legal Red Flags<b>  <br>
    6. ✅ <b>Conversational AI Assistant</b> that understands the contract  <br>
    7. ✅ <b>Modular & Extendable Architecture</b> for enterprise workflows <br>
    </div>
    """, unsafe_allow_html=True)

    # Why It Matters
    st.markdown("<div class='section-title'>💡 Why It Matters</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    Legal documents are often complex, time-consuming, and hard to understand. LexiAgent simplifies this by making legal analysis <b>faster</b>, <b>smarter</b>, and <b>accessible</b> for everyone—lawyers and non-lawyers alike.
    <br><br>
    With <b>LexiAgent</b>, you can:<br>
    1. Save time and reduce manual legal review<br>
    2. Understand contract terms without legal expertise<br>
    3. Identify and avoid risky clauses before signing<br>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'>Built with ❤️ by Muhammad Umer Khan | 2025</div>", unsafe_allow_html=True)


# 📊 Page 1: Analyzer
def show_document_analyzer():
    if not file_path:
        st.warning("📎 Please upload a PDF to start analysis.")
        return

    st.markdown("### 🛠️ Click below to start analyzing your legal document:")
    if st.button("🚀 Start Analyzing"):
        with st.spinner("⚙️ Analyzing your document with LexiAgent..."):
            agent = build_graph()
            result = agent.invoke({
                "file_path": file_path,
                "query": "What are the key terms and risks in this document?"
            })

        # Display Results
        st.markdown("<div class='section-block'>", unsafe_allow_html=True)
        st.markdown("### 📄 Document Type")
        st.write(f"- {result['doc_type']}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-block'>", unsafe_allow_html=True)
        st.markdown("### 📌 Found Clauses")
        for clause, detail in result["clauses"].items():
            st.write(f"- **{clause}**: {detail}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-block'>", unsafe_allow_html=True)
        st.markdown("### 📝 Document Summary")
        bullets = [line.strip() for line in result["doc_summary"].split("\n") if line.strip().startswith("-")]
        for bullet in bullets:
            st.write(bullet)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-block'>", unsafe_allow_html=True)
        st.markdown("### 📑 Clause Summaries")
        st.write(f"- {result['clause_summary']['overall_summary']}")
        for clause, summary in result["clause_summary"]["clause_summaries"].items():
            st.write(f"- **{clause}**: {summary}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-block'>", unsafe_allow_html=True)
        st.markdown("### ⚠️ Risks Identified")

        st.markdown("#### 🌀 Ambiguous Clauses")
        for clause, issue in result["risks"]["ambiguous_clauses"].items():
            st.write(f"- **{clause}**: {issue}")

        st.markdown("#### 💡 Suggestions")
        for clause, suggestion in result["risks"]["suggestions"].items():
            st.write(f"- **{clause}**: {suggestion}")
        st.markdown("</div>", unsafe_allow_html=True)

        if "error" in result:
            st.error(f"❌ Error: {result['error']}")



# 💬 Page 2: Chatbot
@utils.enable_chat_history
def show_chatbot():
    if not file_path:
        st.warning("📎 Please upload a PDF to interact with the chatbot.")
        return

    user_input = st.chat_input(placeholder="💬 Ask anything about the uploaded legal document...")

    if user_input:
        utils.display_msg(user_input, "user")

        with st.chat_message("assistant"):
            try:
                with st.spinner("⚙️ LexiAgent is analyzing your document..."):
                    response = stream_chat_response(user_input, file_path)
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    utils.print_qa(show_chatbot, user_input, response)

            except Exception as e:
                error_msg = f"⚠️ Error processing request: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})


# 🔄 Switch Pages
if page_choice == "📊 **LexiAgent: Document Analyzer**":
    show_document_analyzer()
elif page_choice == "💬 **LexiAgent: AI Assistant**":
    show_chatbot()
elif page_choice == "**📘 LexiAgent - Overview**":
    home()