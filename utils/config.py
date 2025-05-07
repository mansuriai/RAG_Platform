# # utils/config.py
import os

from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
load_dotenv()

class Config:
    # Project structure
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DB_DIR = BASE_DIR / "storage" / "vectordb"
    # MODEL_DIR = BASE_DIR / "models" / "all-mpnet-base-v2"   ####
    
    # Create directories if they don't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    EMBEDDING_MODEL = "Snowflake/snowflake-arctic-embed-l-v2.0" 
    # EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5" 
    # model_name = "Snowflake/snowflake-arctic-embed-l-v2.0"
    EMBEDDING_DIMENSION = 1024  # Adjust based on your specific embedding model
    # EMBEDDING_MODEL = str(MODEL_DIR)
    LLM_MODEL = "gpt-4o-mini"
    
    # Document processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Pinecone settings
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "gcp-starter")
    PINECONE_INDEX_NAME = "rag-platform" #os.getenv("PINECONE_INDEX_NAME", "indigo-assistant")
    
    # App settings
    APP_TITLE = "GoAssist"
    MAX_HISTORY_LENGTH = 8
    
    # Vector DB settings
    COLLECTION_NAME = "indigo-documents"
    DISTANCE_METRIC = "cosine"
    
    # Pinecone index settings
    PINECONE_INDEX_SPEC = {
        "cloud": "aws",
        "region": "us-east-1",
        "metric": "cosine"
    }
    
    # Web scraping settings
    WEB_SCRAPING_DELAY = 1  # Delay between requests in seconds
    
config = Config()


# from pydantic import BaseSettings
# from pathlib import Path
# from typing import Optional

# class Config(BaseSettings):
#     # Application settings
#     APP_TITLE: str = "RAG Application"
#     DATA_DIR: Path = Path("data")
#     PDF_STORAGE_DIR: Path = Path("pdf_storage")
    
#     # Embedding settings
#     EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
#     EMBEDDING_DIMENSION: int = 384
    
#     # LLM settings
#     LLM_MODEL: str = "gpt-3.5-turbo"
    
#     # Vector database settings
#     PINECONE_API_KEY: Optional[str] = None
#     PINECONE_ENVIRONMENT: Optional[str] = None
#     PINECONE_INDEX_NAME: Optional[str] = None
    
#     # Web settings
#     MAX_WEBPAGE_DEPTH: int = 2
    
#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"

# def load_environment():
#     """Load environment variables and return config"""
#     return Config()

# config = load_environment()