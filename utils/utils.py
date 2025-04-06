from langchain_groq import ChatGroq
from config import config as CONFIG
import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
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
    
def configure_llm(MODEL_NAME):
    """
    Configure LLM to run on Hugging Face Inference API (Cloud-Based).
    
    Returns:
        llm (LangChain LLM object): Configured model instance.
    """

    # Sidebar to select LLM
    try:
        # logging.info(f"🤖 Querying LLM: {MODEL_NAME}")
        llm = ChatGroq(
            temperature=0,
            groq_api_key=CONFIG.GROQ_API_KEY,
            model_name=MODEL_NAME
        )
        return llm
    except Exception as e:
        logging.error(f"❌ LLM Query Error: {str(e)}")
        return "❌ Error generating LLM response."

@st.cache_resource  # Cache the embedding model to avoid reloading it every time
def configure_embedding_model():
    """
    Configures and caches the embedding model.

    Returns:
        embedding_model (FastEmbedEmbeddings): The loaded embedding model.
    """
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # Load and return the embedding model

def enable_chat_history(func):
    """
    Decorator to handle chat history and UI interactions.
    Ensures chat messages persist across interactions.
    """
    current_page = func.__qualname__  # Get function name to track current chatbot session

    # Clear session state if model/chatbot is switched
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page  # Store the current chatbot session
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()  # Clear cached resources
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except Exception:
            pass  # Ignore errors if session state keys do not exist

    # Initialize chat history if not already present
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display chat history in the UI
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)  # Execute the decorated function

    return execute

def display_msg(msg, author):
    """
    Displays a chat message in the UI and appends it to session history.

    Args:
        msg (str): The message content to display.
        author (str): The author of the message ("user" or "assistant").
    """
    st.session_state.messages.append({"role": author, "content": msg})  # Store message in session
    st.chat_message(author).write(msg)  # Display message in Streamlit UI

def print_qa(cls, question, answer):
    """
    Logs the Q&A interaction for debugging and tracking.

    Args:
        cls (class): The calling class.
        question (str): User question.
        answer (str): Model response.
    """
    log_str = f"\nUsecase: {cls.__name__}\nQuestion: {question}\nAnswer: {answer}\n" + "-" * 50
    logging.info(log_str)  # Log the interaction using Streamlit's logger

def sync_st_session():
    """
    Ensures Streamlit session state values are properly synchronized.
    """
    for k, v in st.session_state.items():
        st.session_state[k] = v 