import os, json, logging
from typing import Dict, Optional
from utils.utils import configure_llm, load_prompt_template
from clause_extractor import parse_json_safely
from clause_extractor import extract_clauses, merge_clause_chunks, parse_json_safely
from document_loader import load_and_chunk
from json_fix import fix_it
from config import config as CONFIG

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/summarizer.log"),
        logging.StreamHandler()
    ]
)

def summarize_contract(clauses: Dict[str, str]) -> Optional[Dict]:
    try:
        prompt_template = load_prompt_template(CONFIG.DOC_SUMMARIZER_PATH)
        clause_json = json.dumps(clauses, indent=2)
        prompt = prompt_template.replace("{clauses}", clause_json)

        llm = configure_llm()
        logging.info("📝 Sending clauses to LLM for summarization...")
        response = llm.invoke(prompt)
        raw_output = str(response.content if hasattr(response, "content") else response)
        try:
            json_start = raw_output.find('{')
            json_end = raw_output.rfind('}') + 1
            json_text = raw_output[json_start:json_end]
            parsed = json.loads(json_text)
            
            logging.info("✅ Summarization complete.")
            return parsed
        except Exception as parse_err:
            logging.warning("⚠️ Failed to parse JSON. Returning raw response.")
            return {"raw_response": str(raw_output)}
    except Exception as e:
        logging.error(f"❌ Summarization failed: {e}")
        return None

def get_doc_summary(file_path):
    doc_chunks = load_and_chunk(file_path)
    chunk_summaries = []
    for i, chunk in enumerate(doc_chunks):
        prompt = f"""
        You are a legal document assistant. Summarize the following legal text in plain English as bullet points:
        {chunk}    
        Bullet Point Summary:
        """
        llm = configure_llm()
        summary = llm.invoke(prompt)
        chunk_summaries.append(summary.content.strip())
    
    combined_summary = "\n".join(chunk_summaries)

    final_prompt = f"""
    You are a legal assistant. The following is a collection of summaries of parts of a legal document. Combine them into a single, high-quality bullet point summary for the entire document, removing repetition and improving clarity.
    {combined_summary}
    Final Summary:
    """
    final_summary = llm.invoke(prompt)
    
    return final_summary.content.strip()

def get_summary(file_path: str):
    
    extracted = extract_clauses(file_path)
    parsed = [parse_json_safely(text, idx) for idx, text in enumerate(extracted) if parse_json_safely(text, idx)]
    merged_clauses = merge_clause_chunks(parsed)

    clause_summary = summarize_contract(merged_clauses)
    doc_summary = get_doc_summary(file_path)
    
    return json.dumps(clause_summary, indent=2), doc_summary

if __name__ == "__main__":

    file_path = "./data/Example-One-Way-Non-Disclosure-Agreement.pdf"
    clause_prompt_path = "./prompts/clause_extraction.txt"
    summary_prompt_path = "./prompts/summarization.txt"

    clause_summary, doc_summary = get_summary(file_path)
    
    print("\n📝 Clause Summary Output:\n", json.dumps(clause_summary, indent=2))
    print("\n📝 Document Summary Output:\n", doc_summary)