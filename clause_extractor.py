import os
import logging
import json
import re
from typing import Dict, Optional, List
from collections import defaultdict
from utils.utils import configure_llm, load_prompt_template
from document_loader import load_and_chunk
from config import config as CONFIG

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/clause_extractor.log"),
        logging.StreamHandler()
    ]
)

def fix_json_string(json_string: str) -> str:
    """
    Fix malformed JSON by removing <think> tags and extracting valid JSON content.
    """
    try:
        # Remove <think> tags and their content
        json_string = re.sub(r'<think>.*?</think>', '', json_string, flags=re.DOTALL)
        # Remove any leading/trailing non-JSON text
        json_string = re.sub(r'^[^\{]*', '', json_string)
        json_string = re.sub(r'[^\}]*$', '', json_string)
        # Ensure proper JSON structure
        json_string = json_string.strip()
        if not json_string.startswith('{'):
            json_string = '{' + json_string
        if not json_string.endswith('}'):
            json_string = json_string + '}'
        return json_string
    except Exception as e:
        logging.error(f"❌ Error fixing JSON string: {e}")
        return json_string

def parse_json_safely(json_string: str, chunk_index: int) -> Optional[Dict]:
    """
    Parse JSON string, attempting to fix malformed JSON if necessary.
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        logging.warning(f"⚠️ Chunk {chunk_index+1} returned invalid JSON. Attempting to fix...")
        try:
            fixed_json = fix_json_string(json_string)
            return json.loads(fixed_json)
        except Exception as e:
            logging.error(f"❌ JSON fix failed for chunk {chunk_index+1}: {e}")
            return None

def extract_clauses_from_chunk(chunk: str, prompt_template: str, llm) -> Optional[str]:
    try:
        prompt = prompt_template.replace("{text}", chunk.strip())
        logging.info("🔹 Sending chunk to LLM for clause extraction...")
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else response
        logging.debug(f"Raw LLM response for chunk: {content}")
        return content
    except Exception as e:
        logging.error(f"❌ Error in extracting clauses from chunk: {e}")
        return None

def extract_clauses(file_path: str) -> List[str]:
    try:
        logging.info(f"📂 Loading and chunking document: {file_path}")
        _, chunks = load_and_chunk(file_path)
        
        prompt_template = load_prompt_template(CONFIG.CLAUSE_EXTRACTION_PROMPT_PATH)
        llm = configure_llm(MODEL_NAME="meta-llama/llama-4-maverick-17b-128e-instruct")
        
        all_extracted_clauses = []
        for i, chunk in enumerate(chunks):
            logging.info(f"📄 Processing chunk {i+1}/{len(chunks)}...")
            clauses = extract_clauses_from_chunk(chunk, prompt_template, llm)
            if clauses:
                all_extracted_clauses.append(clauses)
        
        logging.info("✅ All chunks processed for clause extraction.")
        return all_extracted_clauses
    
    except Exception as e:
        logging.exception(f"❌ Failed to extract clauses from document: {e}")
        return []

def merge_clause_chunks(chunk_outputs: List[Dict[str, str]]) -> Dict[str, str]:
    final_clauses = defaultdict(str)

    for chunk in chunk_outputs:
        if not chunk:  # Skip None or empty chunks
            continue
        for clause, value in chunk.items():
            if final_clauses[clause] == "" and value and value != "Not Found":
                final_clauses[clause] = value

    # Initialize all required clauses with "Not Found" if missing
    required_clauses = [
        "Termination Clause", "Confidentiality Clause", "Governing Law", "Payment Terms",
        "Liability Clause", "Force Majeure", "Dispute Resolution", "Indemnification Clause",
        "Intellectual Property", "Amendment Clause"
    ]
    for clause in required_clauses:
        if clause not in final_clauses or not final_clauses[clause]:
            final_clauses[clause] = "Not Found"

    return dict(final_clauses)

def get_clause_extracted(file_path: str) -> Dict[str, str]:
    extracted = extract_clauses(file_path)
    parsed_results = [parse_json_safely(text, idx) for idx, text in enumerate(extracted)]
    merged_clauses = merge_clause_chunks([res for res in parsed_results if res])
    
    return merged_clauses

# Sample Test
if __name__ == "__main__":
    merged_clauses = get_clause_extracted(CONFIG.FILE_PATH)
    
    print("\n📌 Final Merged Clauses:\n", json.dumps(merged_clauses, indent=2))