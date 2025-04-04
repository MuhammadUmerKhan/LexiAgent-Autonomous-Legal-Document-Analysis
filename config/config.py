import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/document_classifier.log"),
        logging.StreamHandler()
    ]
)

try:
    # API Keys (Keep them private using .env)
    GROQ_API_KEY = os.getenv("GROK_API_KEY")
except:
    logging.error("❌ API KEYS not found or not set.")

try:
    # Constants
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    MODEL_NAME = "qwen-2.5-32b"
except Exception as e:
    logging.error(f"❌ Error loading Constants: {str(e)}")

logging.info("✅ Configuration Loaded Successfully.")