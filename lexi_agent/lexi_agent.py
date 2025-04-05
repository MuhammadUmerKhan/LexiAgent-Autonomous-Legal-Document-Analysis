from langgraph.graph import StateGraph
from typing import Dict, Any
import logging
from document_loader import load_and_chunk
from classify_documents import classify_document
from scripts.clause_extractor import extract_clauses, merge_clause_chunks, parse_json_safely
from risk_detector import analyze_clause_risks
from summarizer import get_doc_summary, summarize_contract

logging.basicConfig(level=logging.INFO)

# Shared State
State = Dict[str, Any]

# Node functions
def load_and_prepare(state: State) -> State:
    file_path = state["file_path"]
    full_text, chunks = load_and_chunk(file_path)
    state["full_text"] = full_text
    state["chunks"] = chunks
    return state

def classify(state: State) -> State:
    state["doc_type"] = classify_document(state["full_text"])
    return state

def extract(state: State) -> State:
    raw_extracted = extract_clauses(state["file_path"], "./prompts/clause_extraction.txt")
    parsed = [parse_json_safely(c, idx) for idx, c in enumerate(raw_extracted) if parse_json_safely(c, idx)]
    state["clauses"] = merge_clause_chunks(parsed)
    return state

def detect_risks(state: State) -> State:
    state["risks"] = analyze_clause_risks(state["clauses"], "./prompts/risk_analysis.txt")
    return state

def summarize(state: State) -> State:
    state["doc_summary"] = get_doc_summary(state["chunks"])
    state["clause_summary"] = summarize_contract(state["clauses"])
    return state

# Build LangGraph
def build_graph() -> StateGraph:
    builder = StateGraph()

    builder.add_node("load", load_and_prepare)
    builder.add_node("classify", classify)
    builder.add_node("extract_clauses", extract)
    builder.add_node("risk_analysis", detect_risks)
    builder.add_node("summarization", summarize)

    builder.set_entry_point("load")

    builder.add_edge("load", "classify")
    builder.add_edge("classify", "extract_clauses")
    builder.add_edge("extract_clauses", "risk_analysis")
    builder.add_edge("risk_analysis", "summarization")

    builder.set_finish_point("summarization")

    return builder.compile()
