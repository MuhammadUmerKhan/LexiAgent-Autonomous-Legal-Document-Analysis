# 📑 LexiAgent – AI-Powered Autonomous Legal Document Agent

![](https://redblink.com/wp-content/uploads/2024/11/ai-agents-for-legal-document-management.png?x65848)

## 🌟 Overview

LexiAgent is an advanced AI-powered legal document analysis and assistant tool designed to automate and streamline the processing, understanding, and risk assessment of legal documents such as Non-Disclosure Agreements (NDAs), employment contracts, service agreements, and more. This project integrates Large Language Models (LLMs), natural language processing (NLP), and workflow orchestration to extract key clauses, classify document types, summarize content, detect risks, and provide an interactive chat interface for legal queries. LexiAgent is built to save time, reduce manual effort, and enhance accuracy for legal professionals, businesses, and researchers dealing with complex legal documents. 🚀

The system is modular, scalable, and user-friendly, offering both a web-based interface via Streamlit and a backend workflow managed by LangGraph. It logs all operations, handles errors gracefully, and provides detailed outputs in JSON or plain text, making it suitable for enterprise-level legal document management.

## 🎯 Purpose of the Project

The primary purpose of LexiAgent is to:

- **Automate Legal Document Analysis**: Extract specific clauses (e.g., Termination, Confidentiality, Payment Terms) from legal documents and present them in a structured format.
- **Classify Documents**: Identify the type of legal document (e.g., NDA, Employment Contract, Lease Agreement) to aid in organization and understanding.
- **Summarize Content**: Provide plain-English summaries of entire documents and individual clauses, making legal jargon accessible to non-experts.
- **Detect Risks**: Identify vague, ambiguous, or risky wording in clauses and suggest improvements to mitigate legal risks.
- **Enable Interaction**: Offer a chatbot interface for users to ask questions about uploaded documents, leveraging Retrieval-Augmented Generation (RAG) and tools for real-time analysis.
- **Enhance Efficiency**: Reduce the time and expertise required to review and understand legal agreements, minimizing human error and improving productivity.

LexiAgent addresses the challenges of manual legal document review, such as complexity, time consumption, and the risk of overlooking critical details, by combining AI automation with a user-friendly interface.  This system is tailored for legal firms, contract analysts, corporate compliance teams, and legal-tech platforms seeking AI-enhanced productivity.

---

## 🧠 **Core Features & Capabilities**

| Feature                        | Description |
|-------------------------------|-------------|
| 🧾 **Document Classification**     | Detect whether the document is an NDA, lease, employment contract, etc. |
| 📌 **Clause Extraction**          | Pull out specific clauses (e.g., confidentiality, dispute resolution) |
| 📝 **Summarization**             | Provide a human-readable summary |
| 🔍 **Risk Detection**            | Identify unusual, risky, or non-compliant clauses |
| 💬 **Q&A Interface**             | Users can query the document in plain English |
| 🧩 **Autonomous LLM Agent**      | Manages the flow of document processing using tools and memory |
| 🌐 **Multi-LLM Architecture**     | Uses the best LLM for each task (Qwen for summaries, LLaMA 4 for classification, etc.) |

---

## 🧬 **System Architecture**

```
[User Uploads Legal Document]
             |
             v
     [LLM Agent Workflow - LangGraph]
             |
    ┌────────┼─────────┬────────────────────┐────────────┐
    ▼        ▼         ▼                    ▼            ▼
[Classification] [Clause Extraction] [Summarization] [Risk Analysis]
             |
             v
   [Outputs Aggregated & Sent to UI]
             |
             v
     [User Queries (Optional)]
             |
             v
     [RAG-based Answer Generator]
```

---

## 🧠 **LLM Selection Strategy**

| Task | Model |
|------|-------|
| 🧾 Classification | `qwen/qwen2-72b-instruct` |
| 📜 Clause Extraction | `qwen/qwen2-72b-instruct` |
| ✂️ Summarization | `meta-llama/llama-4-scout-17b-16e-instruct` |
| ⚠️ Risk Analysis | `meta-llama/llama-4-scout-17b-16e-instruct` |
| 🤖 Agent Reasoning | `meta-llama/llama-4-scout-17b-16e-instruct` |
| 📚 RAG (Query Answering) | `meta-llama/llama-4-scout-17b-16e-instruct` |

---

## 🧰 **Technologies Used**

LexiAgent leverages a robust stack of modern technologies to achieve its goals. Here’s a detailed breakdown:

- **Programming Language**: Python 3.8+ (for backend logic, scripting, and web interface).
- **AI and NLP Libraries**:
  - **LangChain-Groq**: Integrates with the Grok API to use LLMs for clause extraction, summarization, classification, and risk analysis.
  - **SentenceTransformers**: Used for generating embeddings (if needed for future RAG or similarity searches).
- **Workflow Orchestration**:
  - **LangGraph**: Manages multi-step workflows (e.g., load, classify, extract, analyze, summarize) as autonomous agents, ensuring sequential and conditional processing.
- **Web Interface**:
  - **Streamlit**: Creates an interactive, user-friendly web interface for uploading documents, analyzing them, and chatting with the AI assistant.
- **Document Parsing**:
  - **pdfplumber**: Extracts text from PDF files.
  - **python-docx**: Handles DOCX files.
  - **Built-in Libraries**: `os`, `json` for file operations and data handling.
- **Text Processing**:
  - **LangChain Text Splitter**: Splits large documents into manageable chunks for processing (e.g., `RecursiveCharacterTextSplitter`).
- **Logging and Error Handling**:
  - **logging**: Built-in Python library for tracking operations, errors, and progress in log files.
- **Configuration Management**:
  - **dotenv**: Loads environment variables (e.g., API keys) from `.env` or `config.py`.
- **Data Structures and Typing**:
  - **typing**: Ensures type hints for better code clarity and maintainability.
  - **json**: Handles JSON data for structured outputs and inputs.

| Category | Technology |
|---------|------------|
| 🔄 **Agent Workflow** | [LangGraph](https://www.langgraph.dev/) |
| 🧠 **LLMs** | Qwen1.5-72B-Instruct, LLaMA 4 Scout 17B |
| 🧩 **Embedding Models** | BGE or E5 embeddings |
| 📚 **Vector Database (optional for RAG)** | FAISS or ChromaDB |
| 🎯 **Prompt Engineering** | Custom prompts per tool/task |
| 🎨 **Frontend** | Streamlit |
| 🧪 **Evaluation** | Logs, visual inspection, sample test cases |

These technologies work together to create a seamless, efficient, and scalable legal document analysis solution.

## ⚙️ How It Works

LexiAgent operates through a multi-step process, orchestrated by LangGraph and exposed via a Streamlit interface. Here’s a detailed breakdown of how it functions:

### 1. Document Loading and Chunking
- **File**: `document_loader.py`
- **Process**: 
  - Users upload legal documents (PDF, DOCX, TXT) via the Streamlit interface.
  - `load_document()` and `load_and_chunk()` in `document_loader.py` parse the document based on its format (e.g., using `pdfplumber` for PDFs).
  - The text is split into chunks using `RecursiveCharacterTextSplitter` with configurable `CHUNK_SIZE` and `CHUNK_OVERLAP` from `config.py`.
  - Logs are generated to track success or failure (e.g., `logs/document_classifier.log`).

### 2. Document Classification
- **File**: `classify_documents.py`
- **Process**:
  - The full text of the document is sent to an LLM (configured via `configure_llm` in `utils.utils.py`) using a prompt from `prompts/document_classification.txt`.
  - `classify_document()` uses the "qwen-2.5-32b" model to determine the document type (e.g., "Non Disclosure Agreement") and returns it as a string.
  - Logs track the classification process and any errors.

### 3. Clause Extraction
- **File**: `clause_extractor.py`
- **Process**:
  - Chunks of the document are processed by an LLM (e.g., "qwen-2.5-32b") using a prompt from `prompts/clause_extraction.txt`.
  - `extract_clauses()` extracts clauses like Termination, Confidentiality, etc., and `merge_clause_chunks()` combines results, filling missing clauses with "Not Found."
  - `parse_json_safely()` ensures JSON outputs are valid, using `json_fix` if necessary.
  - The final output is a JSON object mapping clause names to their text or "Not Found."

### 4. Risk Analysis
- **File**: `risk_detector.py`
- **Process**:
  - Extracted clauses are analyzed using an LLM (e.g., "meta-llama/llama-4-scout-17b-16e-instruct") and a prompt from `prompts/risk_analysis.txt`.
  - `analyze_clause_risks()` identifies vague or risky wording and suggests improvements, returning a JSON object with `ambiguous_clauses` and `suggestions`.
  - Only present clauses are analyzed; "Not Found" clauses are ignored.

### 5. Summarization
- **File**: `summarizer.py`
- **Process**:
  - `summarize_contract()` uses an LLM (e.g., "meta-llama/llama-4-scout-17b-16e-instruct") and a prompt from `prompts/summarization.txt` to create plain-English summaries of clauses and the entire document.
  - `get_doc_summary()` chunks the document, summarizes each chunk, and combines them into a final bullet-point summary.
  - Outputs are in JSON format for clauses and plain text for the document summary.

### 6. Workflow Orchestration
- **File**: `pdf_agent.py`
- **Process**:
  - Uses LangGraph to orchestrate the sequence: load document → classify → extract clauses → analyze risks → summarize.
  - `build_graph()` defines a state machine (`State`) with nodes for each step, ensuring sequential execution and error handling.
  - Logs track each step (e.g., `logs/langgraph.log`).

### 7. Chatbot Functionality
- **Files**: `chat_agent.py`, `utils/utils.py`
- **Process**:
  - `stream_chat_response()` in `chat_agent.py` builds a chatbot using LangGraph, binding tools like `ClassifyDocument`, `ExtractClauses`, `DetectRisks`, and `SummarizeDocument`.
  - Users can ask questions about uploaded documents, and the chatbot responds with formatted, emoji-enhanced text (e.g., 📄, ⚠️).
  - The chatbot uses the same LLMs and maintains a chat history via `enable_chat_history` in `utils/utils.py`.

### 8. User Interface
- **File**: `streamlit_app.py`
- **Process**:
  - Provides a Streamlit web interface with three modes: Overview, Document Analyzer, and AI Assistant.
  - Users upload PDFs, select analysis modes, and view results (e.g., document type, clauses, summaries, risks) or chat with the AI.
  - Custom CSS enhances the UI with a professional look (e.g., orange accents, boxed sections).

### Key Features
- **Upload Support**: Handles PDF, DOCX, and TXT files.
- **Real-Time Analysis**: Processes documents in seconds, logging progress and errors.
- **Interactive Chat**: Answers legal queries with formatted, professional responses.
- **Risk Mitigation**: Highlights ambiguous clauses and suggests improvements.
- **Modular Design**: Each component (loader, extractor, classifier, etc.) is separate, allowing easy updates or extensions.

## 📂 Files Included (Detailed)

Here’s a breakdown of each file and its role:

- **`document_loader.py`**: Loads and chunks documents (PDF, DOCX, TXT) using `pdfplumber`, `python-docx`, and `RecursiveCharacterTextSplitter`. Logs to `logs/document_classifier.log`.
- **`clause_extractor.py`**: Extracts legal clauses using LLMs and merges chunked results. Uses `qwen-2.5-32b`. Logs to `logs/clause_extractor.log`.
- **`classify_documents.py`**: Classifies documents into types (e.g., NDA) using `qwen-2.5-32b`. Logs to `logs/document_classifier.log`.
- **`summarizer.py`**: Summarizes documents and clauses using `meta-llama/llama-4-scout-17b-16e-instruct`. Logs to `logs/summarizer.log`.
- **`risk_detector.py`**: Analyzes clause risks using `meta-llama/llama-4-scout-17b-16e-instruct`. Logs to `logs/risk_detector.log`.
- **`pdf_agent.py`**: Orchestrates the workflow using LangGraph. Logs to `logs/langgraph.log`.
- **`chat_agent.py`**: Implements the chatbot with tools for analysis. Uses `meta-llama/llama-4-scout-17b-16e-instruct`. Logs to `logs/langgraph.log`.
- **`streamlit_app.py`**: Streamlit UI for uploading, analyzing, and chatting. Logs to `logs/langgraph.log`.
- **`config.py`**: Stores constants like API keys (`GROQ_API_KEY`), file paths (`CLAUSE_EXTRACTION_PROMPT_PATH`), and chunk sizes (`CHUNK_SIZE`, `CHUNK_OVERLAP`).
- **`utils/utils.py`**: Utility functions for configuring LLMs, loading prompts, and managing chat history.
- **prompts/**: Directory with prompt templates (e.g., `clause_extraction.txt`, `risk_analysis.txt`).
- **data/**: Sample legal documents (e.g., `Example-One-Way-Non-Disclosure-Agreement.pdf`).
- **logs/**: Directory for log files tracking all operations.

## 🛠️ Prerequisites

Ensure the following are installed and configured:

- **Python 3.8+**: Available on your system.
- **Pip**: For installing Python packages.
- **Dependencies** (install via `pip install -r requirements.txt` if you create one):
  - `langchain-groq`
  - `streamlit`
  - `langgraph`
  - `sentence-transformers`
  - `pdfplumber`
  - `python-docx`
  - `dotenv`
- **Environment**:
  - `config.py` or `.env` with `GROQ_API_KEY`.
  - `prompts` and `data` directories with files.
  - Write permissions for `logs` and `temp` directories.

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/MuhammadUmerKhan/LexiAgent-AI-Powered-Autonomous-Legal-Document-Analyst.git
cd <project-directory>
```

### 2. Install Dependencies
Create a `requirements.txt` (if not present) or run:
```bash
pip install langchain-groq streamlit langgraph sentence-transformers pdfplumber python-docx python-dotenv
```

### 3. Set Up Environment
Edit `config.py` to include your `GROQ_API_KEY` and ensure prompt and data files are in place.

### 4. Run the Application
Launch the Streamlit app:
```bash
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501` to use LexiAgent.

## 📝 Usage

### User Interface Modes
- **Overview**: Learn about LexiAgent’s features and technology.
- **Document Analyzer**: Upload a PDF, click "Start Analyzing" to see:
  - Document type (e.g., "Non Disclosure Agreement").
  - Extracted clauses (e.g., Termination, Confidentiality).
  - Document and clause summaries.
  - Identified risks and suggestions.

- **AI Assistant**: Ask questions like "What are the payment terms?" or "Are there risks?" The chatbot responds with formatted, emoji-enhanced text.

### Example Workflow
1. Upload a PDF (e.g., `data/Example-One-Way-Non-Disclosure-Agreement.pdf`) in the sidebar.
2. Select "Document Analyzer" to get a full analysis.
3. Switch to "AI Assistant" to query, e.g., "Summarize the confidentiality clause."

## 🤝 Contributing

Contribute by forking the repo, creating a branch, and submitting a pull request. Discuss major changes via issues.

## ⚠️ License

Specify your license here (e.g., MIT, Apache 2.0) in a `LICENSE` file.

## 📞 Contact

For support, contact [muhammadumerk546@gmail.com] or follow [@LinkedIn](inkedin.com/in/muhammad-umer-khan-61729b260/).

## 🔄 Updates

Check back for updates or watch the repository.

---

*Thank you for using LexiAgent! We’re committed to making legal document analysis smarter and faster.* 💬