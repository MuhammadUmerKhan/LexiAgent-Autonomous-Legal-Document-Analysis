## 📑 Project Documentation : Legal Document Analysis System Prompts

## 📂 Files Included

This repository includes the following key components:

- **`clause_extraction.py`**: Extracts specific clauses (e.g., Termination, Confidentiality) from legal documents in JSON format.
- **`summarizer.py`**: Summarizes legal contracts and their clauses in plain English, returning results in JSON.
- **`classifier.py`**: Classifies documents into categories like Non Disclosure Agreement, Employment Contract, etc., returning a single category.
- **`risk_analyzer.py`**: Analyzes legal clauses for vague or risky wording and provides improvement suggestions in JSON format.
- **`config.py`**: Configuration file containing API keys, file paths, and constants (e.g., model names, logging settings).
- **prompts directory**: Contains text files for prompts used in AI interactions (e.g., `clause_extraction.txt`, `risk_analysis.txt`).
- **data directory**: Includes sample legal documents (e.g., PDFs or text files) for testing, such as `Example-One-Way-Non-Disclosure-Agreement.pdf`.
- **logs directory**: Automatically created to store log files (e.g., `document_analyzer.log`).

## 🎯 Purpose

The purpose of this project is to:

- Automate the extraction of key clauses from legal documents (e.g., Termination, Confidentiality).
- Provide clear, plain-English summaries of contracts and their clauses.
- Classify documents into specific types (e.g., NDA, Service Agreement) for better organization and understanding.
- Identify and mitigate risks in legal clauses by highlighting vague wording and suggesting improvements.
- Support legal professionals and businesses in efficiently reviewing and managing legal agreements.

## 🛠️ Prerequisites

Before using the files in this repository, ensure you have the following:

- **Python**: Version 3.8 or higher. 📋
- **Dependencies**:
  - `langchain-groq`: For interacting with AI models (e.g., Grok API).
  - `streamlit`: For any web-based interfaces (optional, if included).
  - `sentence-transformers`: For generating embeddings (if used in classification).
  - `json`: For handling JSON outputs (built-in).
  - `os` and `logging`: For file operations and logging (built-in).
- **Environment**:
  - A `config.py` or `.env` file with your API key (e.g., `GROK_API_KEY`).
  - The `prompts` and `data` directories with the required files.
  - Write permissions to create a `logs` directory.

## 🚀 Getting Started

Follow these steps to set up and use the legal document analysis tools:

1. **Install Dependencies**:
   Navigate to the project directory and install required packages:
   ```bash
   pip install langchain-groq streamlit sentence-transformers
   ```

2. **Set Up Environment Variables**:
   Ensure your `config.py` contains the necessary configurations, such as:
   ```python
   GROQ_API_KEY = "your_api_key_here"
   ```
   Replace `"your_api_key_here"` with your actual Grok API key.

3. **Verify File Structure**:
   Ensure the following directories and files exist:
   - `prompts/clause_extraction.txt`, `prompts/risk_analysis.txt`, etc.
   - `data/Example-One-Way-Non-Disclosure-Agreement.pdf` (or similar sample documents).
   - `config.py` with API keys and constants.

## 📝 Usage

Each script serves a specific purpose:

- **Clause Extraction**: Use `clause_extraction.py` to extract clauses like Termination, Confidentiality, etc., from a legal document. Output is in JSON format.
- **Summarization**: Use `summarizer.py` to generate a plain-English summary of the contract and its clauses. Ignores "Not Found" clauses.
- **Classification**: Use `classifier.py` to categorize the document (e.g., "Non Disclosure Agreement"). Returns only the category name.
- **Risk Analysis**: Use `risk_analyzer.py` to identify vague or risky wording in clauses and suggest improvements. Ignores "Not Found" clauses.

Example inputs and outputs are logged and can be found in the `logs` directory.

## 🤝 Contributing

We welcome contributions to improve this legal document analysis system! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with your changes.

For major changes, please open an issue to discuss your ideas first. 💡