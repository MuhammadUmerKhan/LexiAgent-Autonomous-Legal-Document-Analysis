import os, logging
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

def classify_document(text: str) -> Optional[str]:
    try:
        # Load prompt template
        prompt_template = load_prompt_template(CONFIG.DOC_CLASSIFICATION_PATH)
        prompt = prompt_template.replace("{text}", text.strip()[:CONFIG.MAX_TEXT_LIMIT])  # Limit size for efficiency

        logging.info("🔍 Sending document to LLM for classification...")

        # Initialize Groq LLM with Qwen
        llm = configure_llm(MODEL_NAME="qwen-2.5-32b")

        # Get LLM response
        response = llm.invoke(prompt)
        result = response.content.strip()

        logging.info(f"✅ Classification result: {result}")
        return result

    except Exception as e:
        logging.error(f"❌ Error during classification: {e}")
        return None

def get_classified_doc(file: str):
    text = load_document(file)
    return classify_document(text)

if __name__ == "__main__":
    # Sample test
    result = get_classified_doc(CONFIG.FILE_PATH)
    
    if result:
        print(f"📄 Document Type: {result}")