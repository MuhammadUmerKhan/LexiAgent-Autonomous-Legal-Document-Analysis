import os
import logging
import re
from typing import Optional
from utils.utils import configure_llm, load_prompt_template
from document_loader import load_document
from config import config as CONFIG

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/document_classifier.log"),
        logging.StreamHandler()
    ]
)

# Category mapping for numeric to text conversion
CATEGORY_MAPPING = {
    "1": "Non Disclosure Agreement",
    "2": "Employment Contract",
    "3": "Lease Agreement",
    "4": "Service Agreement",
    "5": "Privacy Policy",
    "6": "Terms and Conditions",
    "7": "Legal Notice",
    "8": "Memorandum of Understanding",
    "9": "Research Paper",
    "10": "Technical Specification",
    "11": "Business Proposal",
    "12": "Financial Report",
    "13": "Government Form",
    "14": "Academic Thesis",
    "15": "Others"
}

def parse_llm_response(response: str) -> Optional[str]:
    """
    Parse Qwen-QwQ-32B response to extract only the document type, ignoring reasoning and tags.
    Converts numeric outputs to category names using CATEGORY_MAPPING.
    """
    try:
        # Remove <think> tags and their content
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        # Clean up any remaining tags or whitespace
        response = response.strip()

        # Check if response is numeric (e.g., "1")
        if response in CATEGORY_MAPPING:
            return CATEGORY_MAPPING[response]
        
        # Check if response is a valid category name
        if response in CATEGORY_MAPPING.values():
            return response
        
        # Log unexpected response
        logging.warning(f"⚠️ Unexpected response format: {response}")
        return None
    except Exception as e:
        logging.error(f"❌ Error parsing response: {e}")
        return None

def classify_document(text: str) -> Optional[str]:
    try:
        # Load prompt template
        prompt_template = load_prompt_template(CONFIG.DOC_CLASSIFICATION_PATH)
        # Ensure text is truncated to avoid exceeding token limits
        prompt = prompt_template.replace("{text}", text.strip()[:CONFIG.MAX_TEXT_LIMIT])
        # Reinforce concise output
        prompt += "\nStrictly output only the document type (e.g., 'Non Disclosure Agreement') as a single phrase, no numbers, no tags, no explanation."

        logging.info("🔍 Sending document to LLM for classification...")

        # Initialize Groq LLM with Qwen-QwQ-32B
        llm = configure_llm(MODEL_NAME="qwen-qwq-32b")

        # Get LLM response
        response = llm.invoke(prompt)
        result = parse_llm_response(response.content.strip())

        if result:
            logging.info(f"✅ Classification result: {result}")
            return result
        else:
            logging.warning("⚠️ No valid classification found in response")
            return None

    except Exception as e:
        logging.error(f"❌ Error during classification: {e}")
        return None

def get_classified_doc(file: str) -> Optional[str]:
    text = load_document(file)
    return classify_document(text)

if __name__ == "__main__":
    # Sample test
    result = get_classified_doc(CONFIG.FILE_PATH)
    
    if result:
        print(f"📄 Document Type: {result}")
    else:
        print("❌ Failed to classify document")