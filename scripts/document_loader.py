import os
import docx
import pdfplumber
import logging
from typing import List, Tuple
from config import config as CONFIG
from langchain.text_splitter import RecursiveCharacterTextSplitter
import warnings

warnings.filterwarnings(action="ignore")

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

def load_pdf(file_path: str) -> str:
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        logging.info(f"✅ PDF loaded successfully: {file_path}")
        return text
    except Exception as e:
        logging.error(f"❌ Failed to load PDF file: {file_path}. Error: {e}")
        raise

def load_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        logging.info(f"✅ DOCX loaded successfully: {file_path}")
        return text
    except Exception as e:
        logging.error(f"❌ Failed to load DOCX file: {file_path}. Error: {e}")
        raise

def load_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        logging.info(f"✅ TXT loaded successfully: {file_path}")
        return content
    except Exception as e:
        logging.error(f"❌ Failed to load TXT file: {file_path}. Error: {e}")
        raise

def load_document(file_path: str) -> str:
    if not os.path.exists(file_path):
        logging.error(f"⛔ File not found: {file_path}")
        raise FileNotFoundError(f"⛔ File not found: {file_path}")

    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == ".pdf":
            return load_pdf(file_path)
        elif ext == ".docx":
            return load_docx(file_path)
        elif ext == ".txt":
            return load_txt(file_path)
        else:
            logging.error(f"⛔ Unsupported file format: {ext}")
            raise ValueError(f"⛔ Unsupported file format {ext}")
    except Exception as e:
        logging.exception(f"❌ Error loading document: {file_path}")
        raise

def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = splitter.split_text(text=text)
        logging.info(f"✅ Text chunked into {len(chunks)} chunks with size={chunk_size}, overlap={chunk_overlap}")
        return chunks
    except Exception as e:
        logging.error("❌ Error during text chunking.")
        raise

def load_and_chunk(
            file_path: str, chunk_size: int = CONFIG.CHUNK_SIZE, chunk_overlap: int = CONFIG.CHUNK_OVERLAP
                    ) -> Tuple[str, List[str]]:
    try:
        full_text = load_document(file_path)
        chunks = chunk_text(full_text, chunk_size, chunk_overlap)
        return full_text, chunks
    except Exception as e:
        logging.exception(f"❌ Failed to load and chunk file: {file_path}")
        raise

# Example Usage (for testing)
if __name__ == "__main__":
    try:
        file_path = "./data/attention paper.pdf"  # Replace with your test file
    except FileExistsError as f:
        print("❌ Error File Path:", str(f))
    full_text, chunks = load_and_chunk(file_path)
    print(f"Document Length: {len(full_text)} characters")
    print(f"Chunks: {len(chunks)}")
    print("First Chunk:\n", chunks[0])