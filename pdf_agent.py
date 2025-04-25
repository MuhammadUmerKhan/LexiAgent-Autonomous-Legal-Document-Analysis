import logging, time
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END

# Import your existing scripts
from document_loader import load_and_chunk
from classify_documents import get_classified_doc
from clause_extractor import get_clause_extracted
from risk_detector import get_clause_risks
from summarizer import get_summary

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

# Define State Schema using TypedDict for clarity
class State(TypedDict):
    file_path: str
    full_text: str
    chunks: list
    doc_type: str
    clauses: Dict[str, str]
    risks: Dict[str, Any]
    doc_summary: str
    clause_summary: str
    error: str
    query: str  # Optional, for future RAG integration

# Node functions
def load_and_prepare(state: State) -> State:
    try:
        file_path = state["file_path"]
        full_text, chunks = load_and_chunk(file_path)
        state["full_text"] = full_text
        state["chunks"] = chunks
        logger.info(f"Loaded and chunked {file_path} into {len(chunks)} chunks")
        return state
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}")
        state["error"] = str(e)
        return state

def classify(state: State) -> State:
    try:
        state["doc_type"] = get_classified_doc(state["file_path"])
        logger.info(f"Classified document as: {state['doc_type']}")
        time.sleep(3)
        return state
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        state["error"] = str(e)
        return state

def extract(state: State) -> State:
    try:
        state["clauses"] = get_clause_extracted(state["file_path"])
        logger.info("Clauses extracted")
        time.sleep(3)
        return state
    except Exception as e:
        logger.error(f"Clause extraction failed: {e}")
        state["error"] = str(e)
        return state

def detect_risks(state: State) -> State:
    try:
        state["risks"] = get_clause_risks(state["file_path"])
        logger.info("Risks detected")
        time.sleep(3)
        return state
    except Exception as e:
        logger.error(f"Risk detection failed: {e}")
        state["error"] = str(e)
        return state

def summarize(state: State) -> State:
    try:
        state["clause_summary"], state["doc_summary"] = get_summary(state["file_path"])
        logger.info("Document and clauses summarized")
        time.sleep(5)
        return state
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        state["error"] = str(e)
        return state

# Build LangGraph
def build_graph() -> StateGraph:
    builder = StateGraph(state_schema=State)  # Pass the state schema

    builder.add_node("load", load_and_prepare)
    builder.add_node("classify", classify)
    builder.add_node("extract_clauses", extract)
    builder.add_node("risk_analysis", detect_risks)
    builder.add_node("summarization", summarize)

    builder.set_entry_point("load")

    # Corrected edges (removed non-existent 'retrieve')
    builder.add_edge("load", "classify")
    builder.add_edge("classify", "extract_clauses")
    builder.add_edge("extract_clauses", "risk_analysis")
    builder.add_edge("risk_analysis", "summarization")
    builder.add_edge("summarization", END)

    return builder.compile()

if __name__ == "__main__":
    # Use absolute path for robustness
    file_path ="./data/Example-One-Way-Non-Disclosure-Agreement.pdf"

    agent = build_graph()
    result = agent.invoke({"file_path": file_path, "query": "What are the key terms and risks in this document?"})

    if "error" not in result:
        print("\n📄 Document Type:", result["doc_type"])
        print("\n📌 Found Clauses:\n", result['clauses'])
        print("\n📝 Summary:\n", result["doc_summary"])
        print("\n📑 Clause Summaries:\n", result["clause_summary"])
        print("\n⚠️ Risks:\n", result["risks"])
    else:
        print(f"Error occurred: {result['error']}")