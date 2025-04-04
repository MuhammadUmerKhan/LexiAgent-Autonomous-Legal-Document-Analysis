from langchain_groq import ChatGroq
from config import config as CONFIG
import os, logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/document_classifier.log"),
        logging.StreamHandler()
    ]
)

def load_prompt_template(file_path: str) -> str:
    if not os.path.exists(file_path):
        logging.error(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    with open(file_path, "r") as f:
        return f.read()
    
def configure_llm():
    """
    Configure LLM to run on Hugging Face Inference API (Cloud-Based).
    
    Returns:
        llm (LangChain LLM object): Configured model instance.
    """

    # Sidebar to select LLM
    try:
        logging.info(f"🤖 Querying LLM: {CONFIG.MODEL_NAME}")
        llm = ChatGroq(
            temperature=0,
            groq_api_key=CONFIG.GROQ_API_KEY,
            model_name=CONFIG.MODEL_NAME
        )
        return llm
    except Exception as e:
        logging.error(f"❌ LLM Query Error: {str(e)}")
        return "❌ Error generating LLM response."