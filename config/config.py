import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging configuration
os.makedirs(os.path.join("..", "logs"), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join("..", "logs", "config.log")),
        logging.StreamHandler()
    ]
)

try:
    # API Keys (Keep them private using .env)
    GROQ_API_KEY = os.getenv("GROK_API_KEY")
except:
    logging.error("❌ API KEYS not found or not set.")

try:
    CLAUSE_EXTRACTION_PROMPT_PATH = os.path.join("prompts", "clause_extraction.txt")
    RISK_ANALYZER_PATH = os.path.join("prompts", "risk_analysis.txt")
    DOC_CLASSIFICATION_PATH = os.path.join("prompts", "document_classification.txt")
    DOC_SUMMARIZER_PATH = os.path.join("prompts", "summarization.txt")
except FileNotFoundError as f:
    logging.error(f"❌ {f.filename} not found.")
try:
    # Constants
    CHUNK_SIZE = int(1000)
    CHUNK_OVERLAP = int(200)
    MODEL_NAME = "qwen-2.5-32b"
    MAX_TEXT_LIMIT = int(3000)
except Exception as e:
    logging.error(f"❌ Error loading Constants: {str(e)}")

logging.info("✅ Configuration Loaded Successfully.")