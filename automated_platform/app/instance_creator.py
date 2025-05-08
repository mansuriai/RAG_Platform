################################################ router ##################

# instance_creator.py

import os
import sys
import shutil
import json
from pathlib import Path
import uuid

# Update this path to include both parent directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from platform_core.config_manager import ConfigManager
from core.document_processor import EnhancedDocumentProcessor
from core.embeddings import EmbeddingManager
from core.vector_store import VectorStore

class InstanceCreator:
    """Handles the creation of new RAG application instances."""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def create_instance(self, instance_id, config, pdf_paths=None, urls=None):
        """Create a new RAG application instance.
        
        Args:
            instance_id (str): Unique identifier for the instance
            config (dict): Configuration for the instance
            pdf_paths (list): List of paths to PDF files
            urls (list): List of URLs to scrape
        """
        try:
            # Create instance directory
            instance_dir = self.config_manager.get_instance_dir(instance_id)
            os.makedirs(instance_dir, exist_ok=True)
            
            # Create required subdirectories
            pdf_dir = os.path.join(instance_dir, "pdfs")
            data_dir = os.path.join(instance_dir, "data")
            os.makedirs(pdf_dir, exist_ok=True)
            os.makedirs(data_dir, exist_ok=True)
            
            # Process PDFs and URLs to generate embeddings
            if pdf_paths or urls:
                self._process_documents(instance_id, config, pdf_paths, urls)
            
            return True
        except Exception as e:
            print(f"Error creating instance {instance_id}: {str(e)}")
            return False
    
    def _process_documents(self, instance_id, config, pdf_paths=None, urls=None):
        """Process documents and generate embeddings.
        
        Args:
            instance_id (str): Instance ID
            config (dict): Instance configuration
            pdf_paths (list): List of paths to PDF files
            urls (list): List of URLs to scrape
        """
        # Set environment variables for the instance
        os.environ["OPENAI_API_KEY"] = config.get("openai_api_key", os.environ.get("OPENAI_API_KEY", ""))
        os.environ["ANTHROPIC_API_KEY"] = config.get("anthropic_api_key", os.environ.get("ANTHROPIC_API_KEY", ""))
        os.environ["PINECONE_API_KEY"] = config.get("pinecone_api_key", os.environ.get("PINECONE_API_KEY", ""))
        os.environ["PINECONE_ENVIRONMENT"] = config.get("pinecone_environment", os.environ.get("PINECONE_ENVIRONMENT", "gcp-starter"))
        os.environ["PINECONE_INDEX_NAME"] = f"rag-{instance_id[:8]}"
        
        # Initialize document processor
        doc_processor = EnhancedDocumentProcessor()
        
        # Initialize embedding manager
        embedding_manager = EmbeddingManager()
        
        # Initialize vector store
        vector_store = None
        if config.get('vector_store') == 'Pinecone':
            vector_store = VectorStore()
        else:
            # For other vector stores, we'll need to implement those classes
            pass
        
        # Process PDFs
        if pdf_paths:
            for pdf_path in pdf_paths:
                try:
                    # Process documents
                    chunks = doc_processor.process_file(Path(pdf_path))
                    
                    # Generate embeddings
                    texts = [chunk['text'] for chunk in chunks]
                    embeddings = embedding_manager.generate_embeddings(texts)
                    
                    # Store in vector database
                    vector_store.add_documents(chunks, embeddings)
                except Exception as e:
                    print(f"Error processing PDF {pdf_path}: {str(e)}")
        
        # Process URLs
        if urls:
            try:
                # Import here to avoid circular imports
                from core.web_scraper import IndigoWebScraper
                
                scraper = IndigoWebScraper()
                for url in urls:
                    try:
                        # Scrape the URL
                        chunks = scraper.scrape_section("offers")  # Using a default section for now
                        
                        # Generate embeddings
                        texts = [chunk['text'] for chunk in chunks]
                        embeddings = embedding_manager.generate_embeddings(texts)
                        
                        # Store in vector database
                        vector_store.add_documents(chunks, embeddings)
                    except Exception as e:
                        print(f"Error processing URL {url}: {str(e)}")
            except Exception as e:
                print(f"Error initializing scraper: {str(e)}")