import os, logging, json
from typing import Dict, Optional
from utils.utils import configure_llm, load_prompt_template
from clause_extractor import extract_clauses, merge_clause_chunks
from clause_extractor import parse_json_safely
from config import config as CONFIG

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/risk_detector.log"),
        logging.StreamHandler()
    ]
)

def analyze_clause_risks(clauses: Dict[str, str], prompt_path: str) -> Optional[Dict]:
    try:
        prompt_template = load_prompt_template(prompt_path)
        clause_json = json.dumps(clauses, indent=2)
        prompt = prompt_template.replace("{clauses}", clause_json)

        llm = configure_llm()
        logging.info("🛡️ Sending clauses to LLM for risk analysis...")
        response = llm.invoke(prompt)

        raw_output = str(response.content if hasattr(response, "content") else response)

        # Try to extract JSON manually from the string (strip code block markdowns if any)
        try:
            json_start = raw_output.find('{')
            json_end = raw_output.rfind('}') + 1
            json_text = raw_output[json_start:json_end]
            parsed = json.loads(json_text)
            logging.info("✅ Risk analysis JSON extracted successfully.")
            return parsed
        except Exception as json_err:
            logging.warning("⚠️ Failed to parse JSON manually. Returning raw response.")
            return {
                "ambiguous_clauses": {},
                "suggestions": {},
                "raw_response": raw_output
            }

    except Exception as e:
        logging.error(f"❌ Risk detection failed: {e}")
        return None


# Sample Test
if __name__ == "__main__":

    file_path = "./data/Example-One-Way-Non-Disclosure-Agreement.pdf"
    clause_extract_prompt_path = "./prompts/clause_extraction.txt"
    risk_prompt_path = "./prompts/risk_analysis.txt"

    extracted = extract_clauses(file_path, clause_extract_prompt_path)
    parsed_results = [parse_json_safely(text, idx) for idx, text in enumerate(extracted) if parse_json_safely(text, idx)]
    merged_clauses = merge_clause_chunks(parsed_results)
    
    print("\n🛡️ Risk Detection Output:\n", json.dumps(merged_clauses, indent=2))