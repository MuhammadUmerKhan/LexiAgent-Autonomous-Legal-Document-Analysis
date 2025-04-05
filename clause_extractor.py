import os
import logging
import json
from typing import Dict, Optional, List
from collections import defaultdict
from utils.utils import configure_llm, load_prompt_template
from document_loader import load_and_chunk
from config import config as CONFIG
from json_fix import fix_it as json_fix

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

def extract_clauses_from_chunk(chunk: str, prompt_template: str, llm) -> Optional[str]:
    try:
        prompt = prompt_template.replace("{text}", chunk.strip())
        logging.info("🔹 Sending chunk to LLM for clause extraction...")
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else response
    except Exception as e:
        logging.error(f"❌ Error in extracting clauses from chunk: {e}")
        return None

def extract_clauses(file_path: str) -> str:
    try:
        logging.info(f"📂 Loading and chunking document: {file_path}")
        _, chunks = load_and_chunk(file_path)
        
        prompt_template = load_prompt_template(CONFIG.CLAUSE_EXTRACTION_PROMPT_PATH)
        llm = configure_llm()
        
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
        for clause, value in chunk.items():
            if final_clauses[clause] == "":  # Only keep the first found instance
                if value and value != "Not Found":
                    final_clauses[clause] = value

    # Fill missing clauses with "Not Found"
    for clause in final_clauses:
        if not final_clauses[clause]:
            final_clauses[clause] = "Not Found"

    return dict(final_clauses)

def parse_json_safely(json_string: str, chunk_index: int) -> Optional[Dict]:
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        logging.warning(f"⚠️ Chunk {chunk_index+1} returned invalid JSON. Trying jsonfix...")
        try:
            fixed = json_fix(json_string)
            return json.loads(fixed)
        except Exception as e:
            logging.error(f"❌ jsonfix also failed for chunk {chunk_index+1}: {e}")
            return None

def get_clause_extracted(file_path: str):
    
    extracted = extract_clauses(file_path)
    parsed_results = [parse_json_safely(text, idx) for idx, text in enumerate(extracted) if parse_json_safely(text, idx)]
    merged_clauses = merge_clause_chunks(parsed_results)
    
    return json.dumps(merged_clauses, indent=2)

# Sample Test
if __name__ == "__main__":
    file_path = "./data/Example-One-Way-Non-Disclosure-Agreement.pdf"
    merged_clauses = get_clause_extracted(file_path)
    
    print("\n📌 Final Merged Clauses:\n", merged_clauses)
