# 📑 Project Documentation: LexiAgent - Legal Document Analysis System

## 🌟 Overview

This repository contains the "LexiAgent" system, an AI-powered legal document analysis and assistant tool. LexiAgent is designed to automate and streamline the analysis of legal documents (e.g., NDAs, contracts, agreements) by extracting clauses, classifying document types, summarizing content, detecting risks, and providing a chat interface for user interaction. The system leverages Large Language Models (LLMs), LangGraph for workflow orchestration, and Streamlit for a user-friendly web interface. 🚀

LexiAgent is ideal for legal professionals, businesses, and researchers who need to quickly understand, summarize, and assess legal documents while identifying potential risks and ambiguities.

## 📂 Files Included

This repository includes the following key components:

- **`document_loader.py`**: Loads and chunks various document types (PDF, DOCX, TXT) for analysis.
- **`clause_extractor.py`**: Extracts specific clauses (e.g., Termination, Confidentiality) from legal documents in JSON format.
- **`classify_documents.py`**: Classifies documents into categories (e.g., Non Disclosure Agreement, Service Agreement).
- **`summarizer.py`**: Summarizes legal contracts and their clauses in plain English, returning results in JSON.
- **`risk_detector.py`**: Analyzes legal clauses for vague or risky wording and provides improvement suggestions.
- **`pdf_agent.py`**: Orchestrates a multi-step workflow using LangGraph to process documents (load, classify, extract, analyze risks, summarize).
- **`chat_agent.py`**: Implements a chatbot for interactive queries about legal documents using tools and LLMs.
- **`streamlit_app.py`**: A Streamlit-based web interface ("LexiAgent") for uploading documents, analyzing them, and chatting with an AI assistant.
- **`config.py`**: Configuration file containing API keys, file paths, and constants (e.g., `GROQ_API_KEY`, prompt paths).
- **`utils/utils.py`**: Utility functions for configuring LLMs, loading prompts, and managing chat history.
- **prompts directory**: Contains text files for prompts used in AI interactions (e.g., `clause_extraction.txt`, `risk_analysis.txt`).
- **data directory**: Includes sample legal documents (e.g., `Example-One-Way-Non-Disclosure-Agreement.pdf`) for testing.
- **logs directory**: Automatically created to store log files (e.g., `document_classifier.log`, `langgraph.log`).

## 🎯 Purpose

The purpose of LexiAgent is to:

- Automate the extraction, classification, summarization, and risk analysis of legal documents.
- Provide a user-friendly interface for uploading and analyzing PDFs via Streamlit.
- Enable interactive querying of legal documents through a chatbot powered by Retrieval-Augmented Generation (RAG) and LLMs.
- Identify and mitigate risks in legal clauses by highlighting ambiguities and suggesting improvements.
- Support legal professionals and businesses in efficiently reviewing and managing legal agreements.

## 🛠️ Prerequisites

Before running the LexiAgent system, ensure you have the following:

- **Python**: Version 3.8 or higher. 📋
- **Dependencies**:
  - `langchain-groq`: For interacting with the Grok API.
  - `streamlit`: For the web interface.
  - `langgraph`: For workflow orchestration.
  - `sentence-transformers`: For embeddings (if used).
  - `pdfplumber`: For PDF parsing.
  - `python-docx`: For DOCX parsing.
  - `json`: For JSON handling (built-in).
  - `os`, `logging`: For file operations and logging (built-in).
- **Environment**:
  - A `config.py` or `.env` file with your `GROQ_API_KEY`.
  - The `prompts` and `data` directories with the required files.
  - Write permissions to create `logs` and `temp` directories.

## 🚀 Getting Started

Follow these steps to set up and run LexiAgent:

1. **Clone the Repository**:
   Use the following command to clone this repository to your local machine:
   ```bash
   git clone https://github.com/MuhammadUmerKhan/LexiAgent-AI-Powered-Autonomous-Legal-Document-Analyst.git
   ```
   (Replace `https://github.com/MuhammadUmerKhan/LexiAgent-AI-Powered-Autonomous-Legal-Document-Analyst.git` with the actual URL if applicable.)

2. **Install Dependencies**:
   Navigate to the project directory and install required packages:
   ```bash
   cd <project-directory>
   pip install langchain-groq streamlit langgraph sentence-transformers pdfplumber python-docx
   ```

3. **Set Up Environment Variables**:
   Ensure your `config.py` contains the necessary configurations, such as:
   ```python
   GROQ_API_KEY = "your_api_key_here"
   ```
   Replace `"your_api_key_here"` with your actual Grok API key.

4. **Verify File Structure**:
   Ensure the following directories and files exist:
   - `prompts/clause_extraction.txt`, `prompts/risk_analysis.txt`, etc.
   - `data/Example-One-Way-Non-Disclosure-Agreement.pdf` (or similar sample documents).
   - `config.py` with API keys and constants.

5. **Run the Streamlit App**:
   Launch the LexiAgent web interface using:
   ```bash
   streamlit run streamlit_app.py
   ```
   (Replace `streamlit_app.py` with the actual script name if different.) Open your web browser to the provided Streamlit URL (usually `http://localhost:8501`).

## 📝 Usage

LexiAgent offers two main modes via the Streamlit interface:

- **Document Analyzer**: Upload a PDF, and LexiAgent will:
  - Classify the document type (e.g., "Non Disclosure Agreement").
  - Extract key clauses (e.g., Termination, Confidentiality).
  - Summarize the document and clauses in plain English.
  - Identify risks and suggest improvements.

- **AI Assistant**: Interact with a chatbot to ask specific questions about the uploaded document. The chatbot uses tools to classify, extract, summarize, and analyze risks, returning formatted responses with emojis (e.g., 📄, ⚠️).

Example workflow:
1. Upload a legal PDF in the sidebar.
2. Choose "LexiAgent: Document Analyzer" to see a detailed analysis.
3. Switch to "LexiAgent: AI Assistant" to ask questions like, "What are the payment terms?" or "Are there any risky clauses?"

All interactions and errors are logged to the `logs` directory.

## 🤝 Contributing

Contributions to improve LexiAgent are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with your changes.

For major changes, please open an issue to discuss your ideas first. 💡
