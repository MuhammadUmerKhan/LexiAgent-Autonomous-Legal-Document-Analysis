import os
import logging
from typing import Optional
from utils.utils import configure_llm, load_prompt_template
from document_loader import load_document
from config import config as CONFIG
from pathlib import Path

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

def classify_document(text: str, prompt_path: str) -> Optional[str]:
    try:
        # Load prompt template
        prompt_template = load_prompt_template(prompt_path)
        prompt = prompt_template.replace("{text}", text.strip()[:CONFIG.MAX_TEXT_LIMIT])  # Limit size for efficiency

        logging.info("🔍 Sending document to LLM for classification...")

        # Initialize Groq LLM with Qwen
        llm = configure_llm()

        # Get LLM response
        response = llm.invoke(prompt)
        result = response.content.strip()

        logging.info(f"✅ Classification result: {result}")
        return result

    except Exception as e:
        logging.error(f"❌ Error during classification: {e}")
        return None

def get_classified_doc(file: str, prompt_path: str):
    text = load_document(file)
    return classify_document(text, prompt_path)

if __name__ == "__main__":
    # Sample test
    file_path = "./data/attention paper.pdf"
    prompt_path = "./prompts/document_classification.txt"
    result = get_classified_doc(file_path, prompt_path=prompt_path)
    if result:
        print(f"📄 Document Type: {result}")