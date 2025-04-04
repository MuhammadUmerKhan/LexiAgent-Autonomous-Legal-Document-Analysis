import os
import logging
from typing import Optional
from utils.utils import configure_llm
from langchain.schema import HumanMessage
from document_loader import load_document
from utils.utils import load_prompt_template
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
        prompt = prompt_template.replace("{text}", text.strip()[:3000])  # Limit size for efficiency

        logging.info("🔍 Sending document to LLM for classification...")

        # Initialize Groq LLM with Qwen
        llm = configure_llm()

        # Get LLM response
        response = llm([HumanMessage(content=prompt)])
        result = response.content.strip()

        logging.info(f"✅ Classification result: {result}")
        return result

    except Exception as e:
        logging.error(f"❌ Error during classification: {e}")
        return None


if __name__ == "__main__":
    # Sample test
    sample_file = "./data/attention paper.pdf"
    try:
        text = load_document(sample_file)
        result = classify_document(text, "./prompts/document_classification.txt")
        if result:
            print(f"📄 Document Type: {result}")
    except Exception as e:
        logging.exception(f"Failed to classify document: {e}")
