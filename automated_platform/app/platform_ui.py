# #platform_ui.py

# import streamlit as st
# import os
# import sys
# import time
# import uuid
# from pathlib import Path
# import json
# import subprocess
# import threading
# from datetime import datetime
# import urllib.parse

# # Add parent directory to path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# ################### Import platform components ################
# ## Use this Import to run on remote
# # from app.instance_creator import InstanceCreator
# # from app.instance_manager import InstanceManager
# # from platform_core.config_manager import ConfigManager 
# # from platform_core.port_manager import PortManager


# ### use these import to run on local
# from automated_platform.app.instance_creator import InstanceCreator
# from automated_platform.app.instance_manager import InstanceManager
# from automated_platform.platform_core.config_manager import ConfigManager 
# from automated_platform.platform_core.port_manager import PortManager

# ############################################################

# # Initialize components
# instance_creator = InstanceCreator()
# instance_manager = InstanceManager()
# config_manager = ConfigManager()

# # Set page config
# st.set_page_config(
#     page_title="RAG Application Generator",
#     layout="wide"
# )

# # Get URL parameters for routing
# query_params = st.experimental_get_query_params()
# # query_params = st.experimental_get_query_params()
# instance_id = query_params.get("instance_id", [None])[0]
# is_home = instance_id is None

# # Initialize session state
# if "active_instance_id" not in st.session_state:
#     st.session_state.active_instance_id = instance_id
# if "deployment_status" not in st.session_state:
#     st.session_state.deployment_status = ""
# if "uploaded_pdfs" not in st.session_state:
#     st.session_state.uploaded_pdfs = []
# if "urls" not in st.session_state:
#     st.session_state.urls = []
# if "generated_id" not in st.session_state:
#     st.session_state.generated_id = None
# if "app_name" not in st.session_state:
#     st.session_state.app_name = "My RAG App"

# def get_base_url():
#     """Get the base URL of the application."""
#     # This is a heuristic - in production, you'd want to set this via an environment variable
#     return os.environ.get("BASE_URL", "http://localhost:8501")

# def get_instance_url(instance_id):
#     """Get the URL for an instance."""
#     base_url = get_base_url()
#     return f"{base_url}/?instance_id={instance_id}"

# def create_instance():
#     """Create a new RAG application instance."""
#     try:
#         # Get values from session state
#         app_name = st.session_state.app_name
#         embedding_model = st.session_state.embedding_model
#         llm_model = st.session_state.llm_model
#         vector_store = st.session_state.vector_store
#         chunk_size = st.session_state.chunk_size
#         chunk_overlap = st.session_state.chunk_overlap
#         top_k = st.session_state.top_k
        
#         # Create unique instance ID
#         instance_id = str(uuid.uuid4())
#         st.session_state.generated_id = instance_id
        
#         # Create instance configuration
#         config = {
#             "instance_id": instance_id,
#             "app_name": app_name,
#             "embedding_model": embedding_model,
#             "llm_model": llm_model,
#             "vector_store": vector_store,
#             "chunk_size": chunk_size,
#             "chunk_overlap": chunk_overlap,
#             "top_k": top_k,
#             "created_at": time.time()
#         }
        
#         # Add API keys to config
#         if llm_model.startswith("gpt") and hasattr(st.session_state, 'openai_api_key'):
#             config["openai_api_key"] = st.session_state.openai_api_key
#         elif llm_model.startswith("claude") and hasattr(st.session_state, 'anthropic_api_key'):
#             config["anthropic_api_key"] = st.session_state.anthropic_api_key
        
#         if vector_store == "Pinecone" and hasattr(st.session_state, 'pinecone_api_key'):
#             config["pinecone_api_key"] = st.session_state.pinecone_api_key
#             config["pinecone_environment"] = st.session_state.pinecone_environment
        
#         # Save configuration
#         config_manager.save_config(instance_id, config)
        
#         # Process PDFs
#         pdf_paths = []
#         for pdf in st.session_state.uploaded_pdfs:
#             instance_dir = config_manager.get_instance_dir(instance_id)
#             pdf_dir = os.path.join(instance_dir, "pdfs")
#             os.makedirs(pdf_dir, exist_ok=True)
            
#             pdf_path = os.path.join(pdf_dir, pdf.name)
#             with open(pdf_path, 'wb') as f:
#                 f.write(pdf.getvalue())
#             pdf_paths.append(pdf_path)
        
#         # Save URLs
#         if st.session_state.urls:
#             instance_dir = config_manager.get_instance_dir(instance_id)
#             os.makedirs(instance_dir, exist_ok=True)
#             urls_file = os.path.join(instance_dir, "urls.txt")
#             with open(urls_file, 'w') as f:
#                 for url in st.session_state.urls:
#                     f.write(f"{url}\n")
        
#         # Create the instance
#         instance_creator.create_instance(instance_id, config, pdf_paths, st.session_state.urls)
        
#         return instance_id
#     except Exception as e:
#         st.error(f"Error creating instance: {str(e)}")
#         import traceback
#         st.code(traceback.format_exc())
#         return None

# def render_home_page():
#     """Render the home page with instance creation form."""
#     st.title("RAG Application Generator")
#     st.write("Upload documents, configure your RAG application, and get a dedicated deployment.")
    
#     with st.expander("About this Platform", expanded=False):
#         st.markdown("""
#         This platform allows you to generate your own RAG (Retrieval-Augmented Generation) chatbot without coding.
        
#         Just follow these steps:
#         1. Upload PDF documents or add URLs to web pages
#         2. Configure your application (embedding model, LLM, etc.)
#         3. Generate your application
#         4. Get a dedicated URL to access your custom RAG chatbot
        
#         All processing and storage are handled automatically, and you'll get a dedicated instance.
#         """)
    
#     col1, col2 = st.columns(2)
    
#     # Document upload section
#     with col1:
#         st.header("Upload Documents")
        
#         # PDF Upload
#         pdf_files = st.file_uploader(
#             "Upload PDF documents",
#             type=['pdf'],
#             accept_multiple_files=True
#         )
        
#         if pdf_files:
#             st.session_state.uploaded_pdfs = pdf_files
#             st.write(f"{len(pdf_files)} PDF documents ready for processing.")
        
#         # URL Input
#         st.subheader("Add URLs")
#         url_input = st.text_area("Enter URLs (one per line) to index web content")
        
#         if url_input:
#             urls = [url.strip() for url in url_input.split("\n") if url.strip()]
#             st.session_state.urls = urls
#             st.write(f"{len(urls)} URLs ready for processing.")
    
#     # Configuration section
#     with col2:
#         st.header("Configure Your Application")
        
#         # Application name input
#         st.session_state.app_name = st.text_input("Application Name", "My RAG App")
        
#         # Model selection
#         st.session_state.embedding_model = st.selectbox(
#             "Embedding Model",
#             [
#                 "sentence-transformers/all-mpnet-base-v2",
#                 "sentence-transformers/all-MiniLM-L6-v2",
#                 "BAAI/bge-small-en-v1.5",
#                 "BAAI/bge-base-en-v1.5"
#             ]
#         )
        
#         st.session_state.llm_model = st.selectbox(
#             "LLM Model",
#             [
#                 # "gpt-3.5-turbo",
#                 # "gpt-4",
#                 # "gpt-4-turbo",
#                 "gpt-4.1-nano",
#                 "gpt-4.1-mini",
#                 "gpt-4.1",
#                 "claude-3-opus-20240229",
#                 "claude-3-sonnet-20240229"
#             ]
#         )
        
#         # Vector store selection
#         st.session_state.vector_store = st.selectbox(
#             "Vector Store Platform",
#             [
#                 "Pinecone",
#                 "Chroma (Local)",
#                 "FAISS (Local)"
#             ]
#         )
        
#         # Advanced settings
#         with st.expander("Advanced Settings", expanded=False):
#             st.session_state.chunk_size = st.slider("Chunk Size", 500, 2000, 1000)
#             st.session_state.chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200)
#             st.session_state.top_k = st.slider("Top K Results", 1, 10, 5)
            
#             st.subheader("API Keys")
#             if st.session_state.llm_model.startswith("gpt"):
#                 st.session_state.openai_api_key = st.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
#             elif st.session_state.llm_model.startswith("claude"):
#                 st.session_state.anthropic_api_key = st.text_input("Anthropic API Key", type="password", value=os.environ.get("ANTHROPIC_API_KEY", ""))
            
#             if st.session_state.vector_store == "Pinecone":
#                 st.session_state.pinecone_api_key = st.text_input("Pinecone API Key", type="password", value=os.environ.get("PINECONE_API_KEY", ""))
#                 st.session_state.pinecone_environment = st.text_input("Pinecone Environment", value=os.environ.get("PINECONE_ENVIRONMENT", "gcp-starter"))
    
#     # Generation section
#     st.header("Generate Your Application")
    
#     if st.button("Generate RAG Application"):
#         with st.spinner("Processing your RAG application..."):
#             # Validate inputs
#             if not st.session_state.uploaded_pdfs and not st.session_state.urls:
#                 st.error("Please upload at least one PDF document or add at least one URL.")
#                 return
            
#             # Create the instance
#             instance_id = create_instance()
            
#             if instance_id:
#                 # Generate the URL for the instance
#                 instance_url = get_instance_url(instance_id)
                
#                 st.success(f"RAG application created with ID: {instance_id}")
#                 st.info("Your application is ready to use!")
                
#                 # Display the URL
#                 st.markdown(f"## Access Your RAG Application")
#                 st.markdown(f"Click the link below to access your dedicated RAG application:")
#                 st.markdown(f"[Open {st.session_state.app_name}]({instance_url})")
                
#                 # Create a button to navigate
#                 if st.button("Open Application"):
#                     # This uses an HTML redirect
#                     st.markdown(f'<meta http-equiv="refresh" content="0;url={instance_url}">', unsafe_allow_html=True)
    
#     # Instance management section
#     st.header("Manage Your Instances")
    
#     try:
#         instances = config_manager.list_configs()
#         if instances:
#             st.write(f"You have {len(instances)} instances:")
            
#             for instance_id, config in instances.items():
#                 app_name = config.get("app_name", "RAG Application")
#                 created_at = config.get("created_at", 0)
#                 formatted_date = datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else "Unknown"
                
#                 with st.expander(f"{app_name} ({instance_id})"):
#                     st.write(f"**Created:** {formatted_date}")
#                     st.write(f"**Models:** {config.get('embedding_model', 'Unknown')} / {config.get('llm_model', 'Unknown')}")
                    
#                     # Generate the URL for the instance
#                     instance_url = get_instance_url(instance_id)
                    
#                     # Display URL with clickable link
#                     st.markdown(f"**URL:** [Open Application]({instance_url})")
                    
#                     # Delete button
#                     if st.button(f"Delete {app_name}", key=f"delete_{instance_id}"):
#                         try:
#                             # Delete the instance directory
#                             instance_dir = config_manager.get_instance_dir(instance_id)
#                             if os.path.exists(instance_dir):
#                                 import shutil
#                                 shutil.rmtree(instance_dir)
                            
#                             # Delete the configuration
#                             config_manager.delete_config(instance_id)
                            
#                             st.success(f"Instance {app_name} deleted successfully!")
#                             st.rerun()
#                         except Exception as e:
#                             st.error(f"Error deleting instance: {str(e)}")
#         else:
#             st.info("No instances found. Generate a new RAG application to get started!")
#     except Exception as e:
#         st.error(f"Error listing instances: {str(e)}")
#         import traceback
#         st.code(traceback.format_exc())

# def render_instance_page(instance_id):
#     """Render the instance page for a specific RAG application."""
#     try:
#         # Get instance configuration
#         config = config_manager.load_config(instance_id)
#         if config is None:
#             st.error(f"Instance with ID {instance_id} not found.")
#             st.button("Back to Home", on_click=lambda: st.experimental_set_query_params())
#             return
        
#         app_name = config.get("app_name", "RAG Application")
#         embedding_model = config.get("embedding_model", "")
#         llm_model = config.get("llm_model", "")
#         vector_store = config.get("vector_store", "")
#         chunk_size = config.get("chunk_size", 1000)
#         chunk_overlap = config.get("chunk_overlap", 200)
#         top_k = config.get("top_k", 5)
#         created_at = config.get("created_at", 0)
        
#         # Initialize the RAG application components
#         from core.embeddings import EmbeddingManager
#         from core.vector_store import VectorStore
#         from core.llm import LLMManager
        
#         # Set environment variables for API keys
#         os.environ["OPENAI_API_KEY"] = config.get("openai_api_key", os.environ.get("OPENAI_API_KEY", ""))
#         os.environ["ANTHROPIC_API_KEY"] = config.get("anthropic_api_key", os.environ.get("ANTHROPIC_API_KEY", ""))
#         os.environ["PINECONE_API_KEY"] = config.get("pinecone_api_key", os.environ.get("PINECONE_API_KEY", ""))
#         os.environ["PINECONE_ENVIRONMENT"] = config.get("pinecone_environment", os.environ.get("PINECONE_ENVIRONMENT", "gcp-starter"))
#         os.environ["PINECONE_INDEX_NAME"] = f"rag-{instance_id[:8]}"
        
#         # Initialize components
#         with st.spinner("Initializing RAG application..."):
#             embedding_manager = EmbeddingManager()
#             vector_store = VectorStore()
#             llm_manager = LLMManager()
        
#         # Initialize session state
#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []
#         if "current_sources" not in st.session_state:
#             st.session_state.current_sources = []
#         if "context_window" not in st.session_state:
#             st.session_state.context_window = top_k
#         if "max_history" not in st.session_state:
#             st.session_state.max_history = 10
#         if "show_sources" not in st.session_state:
#             st.session_state.show_sources = False
        
#         # App header
#         st.title(app_name)
#         st.write("Ask questions about your documents to get accurate, contextual answers.")
        
#         # Back to home button
#         if st.button("↩️ Back to Platform"):
#             st.experimental_set_query_params()
#             st.rerun()
        
#         # Sidebar for app information
#         with st.sidebar:
#             st.header("About this App")
#             st.write(f"**Instance ID:** {instance_id[:8]}...")
#             st.write(f"**Created:** {datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else 'Unknown'}")
#             st.write(f"**Embedding Model:** {embedding_model}")
#             st.write(f"**LLM Model:** {llm_model}")
            
#             # Toggle source visibility
#             st.session_state.show_sources = st.toggle(
#                 "Show Source References", 
#                 value=st.session_state.show_sources
#             )
            
#             # Adjust retrieval parameters
#             st.subheader("Retrieval Settings")
#             st.session_state.context_window = st.slider(
#                 "Number of sources to retrieve", 
#                 min_value=1, 
#                 max_value=10, 
#                 value=st.session_state.context_window
#             )
            
#             # New conversation button
#             if st.button("🔄 New Conversation"):
#                 st.session_state.chat_history = []
#                 st.session_state.current_sources = []
#                 st.rerun()
        
#         # Chat interface
#         for message in st.session_state.chat_history:
#             with st.chat_message(message["role"]):
#                 st.write(message["content"])
        
#         # Display sources if enabled
#         if st.session_state.show_sources and st.session_state.current_sources:
#             with st.expander("📚 Source References", expanded=False):
#                 for i, source in enumerate(st.session_state.current_sources, 1):
#                     metadata = source.get('metadata', {})
#                     url = metadata.get('url', '')
                    
#                     st.markdown(f"### Reference {i}")
#                     if url:
#                         st.markdown(f"[🔗 {metadata.get('source', 'Source')}]({url})")
#                     else:
#                         st.markdown(f"**{metadata.get('source', 'Source')}**")
                    
#                     # Show preview text
#                     preview_text = source['text'][:300] + "..." if len(source['text']) > 300 else source['text']
#                     st.caption(preview_text)
#                     st.divider()
        
#         # User input
#         user_input = st.chat_input("Ask a question about your documents...")
        
#         # Update the query processing in the main chat interface
#         if user_input:
#             # Add user message to chat history
#             st.session_state.chat_history.append({
#                 "role": "user",
#                 "content": user_input
#             })
            
#             # Display user message
#             with st.chat_message("user"):
#                 st.write(user_input)
            
#             # Create a placeholder for the streaming response
#             with st.chat_message("assistant"):
#                 response_placeholder = st.empty()
                
#                 try:
#                     # Generate embedding for query
#                     query_embedding = embedding_manager.generate_embeddings([user_input])[0]
#                     relevant_docs = vector_store.search(
#                         user_input,
#                         query_embedding,
#                         k=st.session_state.context_window
#                     )
                    
#                     # Save the current sources for potential display
#                     st.session_state.current_sources = relevant_docs

#                     # Generate response with enhanced LLM manager
#                     response = llm_manager.generate_response(
#                         user_input,
#                         relevant_docs,
#                         st.session_state.chat_history[-st.session_state.max_history:],
#                         streaming_container=response_placeholder
#                     )
                    
#                     # Display the response
#                     response_placeholder.markdown(response)

#                     # Update chat history
#                     st.session_state.chat_history.append({
#                         "role": "assistant",
#                         "content": response
#                     })
                    
#                 except Exception as e:
#                     st.error(f"An error occurred during query processing: {str(e)}")
#                     st.error("Full error details:")
#                     st.exception(e)
    
#     except Exception as e:
#         st.error(f"Error loading instance: {str(e)}")
#         import traceback
#         st.code(traceback.format_exc())
        
#         # Back to home button
#         if st.button("Back to Home", key="back_error"):
#             st.experimental_set_query_params()
#             st.rerun()

# def main():
#     # Route based on instance_id parameter
#     if instance_id:
#         render_instance_page(instance_id)
#     else:
#         render_home_page()

# if __name__ == "__main__":
#     main()




######################################################

## platform_ui.py

import streamlit as st
import os
import sys
import time
import uuid
from pathlib import Path
import json
import subprocess
import threading
from datetime import datetime
import urllib.parse
import socket

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ################### Import platform components ################
# ## Use this Import to run on remote
# # from app.instance_creator import InstanceCreator
# # from app.instance_manager import InstanceManager
# # from platform_core.config_manager import ConfigManager 
# # from platform_core.port_manager import PortManager


# ### use these import to run on local
# from automated_platform.app.instance_creator import InstanceCreator
# from automated_platform.app.instance_manager import InstanceManager
# from automated_platform.platform_core.config_manager import ConfigManager 
# from automated_platform.platform_core.port_manager import PortManager

# Import platform components
from app.instance_creator import InstanceCreator
from app.instance_manager import InstanceManager
from platform_core.config_manager import ConfigManager 

# Initialize components
instance_creator = InstanceCreator()
config_manager = ConfigManager()

# Set page config
st.set_page_config(
    page_title="RAG Application Generator",
    layout="wide"
)

# Get URL parameters for routing
query_params = st.experimental_get_query_params()
instance_id = query_params.get("instance_id", [None])[0]
is_home = instance_id is None

# Initialize session state
if "active_instance_id" not in st.session_state:
    st.session_state.active_instance_id = instance_id
if "deployment_status" not in st.session_state:
    st.session_state.deployment_status = ""
if "uploaded_pdfs" not in st.session_state:
    st.session_state.uploaded_pdfs = []
if "urls" not in st.session_state:
    st.session_state.urls = []
if "generated_id" not in st.session_state:
    st.session_state.generated_id = None
if "app_name" not in st.session_state:
    st.session_state.app_name = "My RAG App"
if "server_hostname" not in st.session_state:
    # Try to detect the server's address
    st.session_state.server_hostname = None

def get_server_hostname():
    """Detect the server's hostname or IP address.
    
    Returns:
        str: Server hostname or IP, or None if can't be determined
    """
    # Use environment variables if available (for Railway and other platforms)
    if "RAILWAY_STATIC_URL" in os.environ:
        return os.environ["RAILWAY_STATIC_URL"]
    if "RAILWAY_PUBLIC_DOMAIN" in os.environ:
        return f"https://{os.environ['RAILWAY_PUBLIC_DOMAIN']}"
    
    # Check for streamlit's server address
    server_address = os.environ.get("STREAMLIT_SERVER_ADDRESS", "")
    server_port = os.environ.get("STREAMLIT_SERVER_PORT", "8501")
    
    # If explicitly set to 0.0.0.0, this means it's accepting all IPs
    if server_address == "0.0.0.0":
        # Try to get the machine's IP that's accessible from the network
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            if ip_address and ip_address != "127.0.0.1":
                return f"http://{ip_address}:{server_port}"
        except:
            pass
    
    # Try to get external hostname via what Streamlit reports
    try:
        server_url = st.server.server.get_url()
        if server_url and "localhost" not in server_url:
            return server_url
    except:
        pass
    
    # Fallback - use localhost if nothing else works
    return f"http://localhost:{server_port}"

def get_base_url():
    """Get the base URL of the application."""
    # Use cached hostname if available
    if st.session_state.server_hostname:
        return st.session_state.server_hostname
    
    # Otherwise detect it
    hostname = get_server_hostname()
    st.session_state.server_hostname = hostname
    return hostname

def get_instance_url(instance_id):
    """Get the URL for an instance."""
    base_url = get_base_url()
    # Handle case where base_url already has query parameters
    if "?" in base_url:
        return f"{base_url}&instance_id={instance_id}"
    else:
        return f"{base_url}/?instance_id={instance_id}"

def create_instance():
    """Create a new RAG application instance."""
    try:
        # Get values from session state
        app_name = st.session_state.app_name
        embedding_model = st.session_state.embedding_model
        llm_model = st.session_state.llm_model
        vector_store = st.session_state.vector_store
        chunk_size = st.session_state.chunk_size
        chunk_overlap = st.session_state.chunk_overlap
        top_k = st.session_state.top_k
        
        # Create unique instance ID
        instance_id = str(uuid.uuid4())
        st.session_state.generated_id = instance_id
        
        # Create instance configuration
        config = {
            "instance_id": instance_id,
            "app_name": app_name,
            "embedding_model": embedding_model,
            "llm_model": llm_model,
            "vector_store": vector_store,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "top_k": top_k,
            "created_at": time.time()
        }
        
        # Add API keys to config
        if llm_model.startswith("gpt") and hasattr(st.session_state, 'openai_api_key'):
            config["openai_api_key"] = st.session_state.openai_api_key
        elif llm_model.startswith("claude") and hasattr(st.session_state, 'anthropic_api_key'):
            config["anthropic_api_key"] = st.session_state.anthropic_api_key
        
        if vector_store == "Pinecone" and hasattr(st.session_state, 'pinecone_api_key'):
            config["pinecone_api_key"] = st.session_state.pinecone_api_key
            config["pinecone_environment"] = st.session_state.pinecone_environment
        
        # Save configuration
        config_manager.save_config(instance_id, config)
        
        # Process PDFs
        pdf_paths = []
        for pdf in st.session_state.uploaded_pdfs:
            instance_dir = config_manager.get_instance_dir(instance_id)
            pdf_dir = os.path.join(instance_dir, "pdfs")
            os.makedirs(pdf_dir, exist_ok=True)
            
            pdf_path = os.path.join(pdf_dir, pdf.name)
            with open(pdf_path, 'wb') as f:
                f.write(pdf.getvalue())
            pdf_paths.append(pdf_path)
        
        # Save URLs
        if st.session_state.urls:
            instance_dir = config_manager.get_instance_dir(instance_id)
            os.makedirs(instance_dir, exist_ok=True)
            urls_file = os.path.join(instance_dir, "urls.txt")
            with open(urls_file, 'w') as f:
                for url in st.session_state.urls:
                    f.write(f"{url}\n")
        
        # Create the instance
        instance_creator.create_instance(instance_id, config, pdf_paths, st.session_state.urls)
        
        return instance_id
    except Exception as e:
        st.error(f"Error creating instance: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return None

def render_home_page():
    """Render the home page with instance creation form."""
    st.title("RAG Application Generator")
    st.write("Upload documents, configure your RAG application, and get a dedicated deployment.")
    
    # Display the detected server address (for debugging)
    base_url = get_base_url()
    st.write(f"Server address: {base_url}")
    
    with st.expander("About this Platform", expanded=False):
        st.markdown("""
        This platform allows you to generate your own RAG (Retrieval-Augmented Generation) chatbot without coding.
        
        Just follow these steps:
        1. Upload PDF documents or add URLs to web pages
        2. Configure your application (embedding model, LLM, etc.)
        3. Generate your application
        4. Get a dedicated URL to access your custom RAG chatbot
        
        All processing and storage are handled automatically, and you'll get a dedicated instance.
        """)
    
    col1, col2 = st.columns(2)
    
    # Document upload section
    with col1:
        st.header("Upload Documents")
        
        # PDF Upload
        pdf_files = st.file_uploader(
            "Upload PDF documents",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if pdf_files:
            st.session_state.uploaded_pdfs = pdf_files
            st.write(f"{len(pdf_files)} PDF documents ready for processing.")
        
        # URL Input
        st.subheader("Add URLs")
        url_input = st.text_area("Enter URLs (one per line) to index web content")
        
        if url_input:
            urls = [url.strip() for url in url_input.split("\n") if url.strip()]
            st.session_state.urls = urls
            st.write(f"{len(urls)} URLs ready for processing.")
    
    # Configuration section
    with col2:
        st.header("Configure Your Application")
        
        # Application name input
        st.session_state.app_name = st.text_input("Application Name", "My RAG App")
        
        # Model selection
        st.session_state.embedding_model = st.selectbox(
            "Embedding Model",
            [
                "sentence-transformers/all-mpnet-base-v2",
                "sentence-transformers/all-MiniLM-L6-v2",
                "BAAI/bge-small-en-v1.5",
                "BAAI/bge-base-en-v1.5"
            ]
        )
        
        st.session_state.llm_model = st.selectbox(
            "LLM Model",
            [
                "gpt-4.1-nano",
                "gpt-4.1-mini",
                "gpt-4.1",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229"
            ]
        )
        
        # Vector store selection
        st.session_state.vector_store = st.selectbox(
            "Vector Store Platform",
            [
                "Pinecone",
                "Chroma (Local)",
                "FAISS (Local)"
            ]
        )
        
        # Advanced settings
        with st.expander("Advanced Settings", expanded=False):
            st.session_state.chunk_size = st.slider("Chunk Size", 500, 2000, 1000)
            st.session_state.chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200)
            st.session_state.top_k = st.slider("Top K Results", 1, 10, 5)
            
            st.subheader("API Keys")
            if st.session_state.llm_model.startswith("gpt"):
                st.session_state.openai_api_key = st.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
            elif st.session_state.llm_model.startswith("claude"):
                st.session_state.anthropic_api_key = st.text_input("Anthropic API Key", type="password", value=os.environ.get("ANTHROPIC_API_KEY", ""))
            
            if st.session_state.vector_store == "Pinecone":
                st.session_state.pinecone_api_key = st.text_input("Pinecone API Key", type="password", value=os.environ.get("PINECONE_API_KEY", ""))
                st.session_state.pinecone_environment = st.text_input("Pinecone Environment", value=os.environ.get("PINECONE_ENVIRONMENT", "gcp-starter"))
    
    # Generation section
    st.header("Generate Your Application")
    
    if st.button("Generate RAG Application"):
        with st.spinner("Processing your RAG application..."):
            # Validate inputs
            if not st.session_state.uploaded_pdfs and not st.session_state.urls:
                st.error("Please upload at least one PDF document or add at least one URL.")
                return
            
            # Create the instance
            instance_id = create_instance()
            
            if instance_id:
                # Generate the URL for the instance
                instance_url = get_instance_url(instance_id)
                
                st.success(f"RAG application created with ID: {instance_id}")
                st.info("Your application is ready to use!")
                
                # Display the URL
                st.markdown(f"## Access Your RAG Application")
                st.markdown(f"Click the link below to access your dedicated RAG application:")
                st.markdown(f"[Open {st.session_state.app_name}]({instance_url})")
                
                # Create a button to navigate
                if st.button("Open Application"):
                    # This uses an HTML redirect
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={instance_url}">', unsafe_allow_html=True)
    
    # Instance management section
    st.header("Manage Your Instances")
    
    try:
        instances = config_manager.list_configs()
        if instances:
            st.write(f"You have {len(instances)} instances:")
            
            for instance_id, config in instances.items():
                app_name = config.get("app_name", "RAG Application")
                created_at = config.get("created_at", 0)
                formatted_date = datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else "Unknown"
                
                with st.expander(f"{app_name} ({instance_id})"):
                    st.write(f"**Created:** {formatted_date}")
                    st.write(f"**Models:** {config.get('embedding_model', 'Unknown')} / {config.get('llm_model', 'Unknown')}")
                    
                    # Generate the URL for the instance
                    instance_url = get_instance_url(instance_id)
                    
                    # Display URL with clickable link
                    st.markdown(f"**URL:** [Open Application]({instance_url})")
                    
                    # Delete button
                    if st.button(f"Delete {app_name}", key=f"delete_{instance_id}"):
                        try:
                            # Delete the instance directory
                            instance_dir = config_manager.get_instance_dir(instance_id)
                            if os.path.exists(instance_dir):
                                import shutil
                                shutil.rmtree(instance_dir)
                            
                            # Delete the configuration
                            config_manager.delete_config(instance_id)
                            
                            st.success(f"Instance {app_name} deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting instance: {str(e)}")
        else:
            st.info("No instances found. Generate a new RAG application to get started!")
    except Exception as e:
        st.error(f"Error listing instances: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

def render_instance_page(instance_id):
    """Render the instance page for a specific RAG application."""
    try:
        # Get instance configuration
        config = config_manager.load_config(instance_id)
        if config is None:
            st.error(f"Instance with ID {instance_id} not found.")
            st.button("Back to Home", on_click=lambda: st.experimental_set_query_params())
            return
        
        app_name = config.get("app_name", "RAG Application")
        embedding_model = config.get("embedding_model", "")
        llm_model = config.get("llm_model", "")
        vector_store = config.get("vector_store", "")
        chunk_size = config.get("chunk_size", 1000)
        chunk_overlap = config.get("chunk_overlap", 200)
        top_k = config.get("top_k", 5)
        created_at = config.get("created_at", 0)
        
        # Initialize the RAG application components
        from core.embeddings import EmbeddingManager
        from core.vector_store import VectorStore
        from core.llm import LLMManager
        
        # Set environment variables for API keys
        os.environ["OPENAI_API_KEY"] = config.get("openai_api_key", os.environ.get("OPENAI_API_KEY", ""))
        os.environ["ANTHROPIC_API_KEY"] = config.get("anthropic_api_key", os.environ.get("ANTHROPIC_API_KEY", ""))
        os.environ["PINECONE_API_KEY"] = config.get("pinecone_api_key", os.environ.get("PINECONE_API_KEY", ""))
        os.environ["PINECONE_ENVIRONMENT"] = config.get("pinecone_environment", os.environ.get("PINECONE_ENVIRONMENT", "gcp-starter"))
        os.environ["PINECONE_INDEX_NAME"] = f"rag-{instance_id[:8]}"
        
        # Initialize components
        with st.spinner("Initializing RAG application..."):
            embedding_manager = EmbeddingManager()
            vector_store = VectorStore()
            llm_manager = LLMManager()
        
        # Initialize session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "current_sources" not in st.session_state:
            st.session_state.current_sources = []
        if "context_window" not in st.session_state:
            st.session_state.context_window = top_k
        if "max_history" not in st.session_state:
            st.session_state.max_history = 10
        if "show_sources" not in st.session_state:
            st.session_state.show_sources = False
        
        # App header
        st.title(app_name)
        st.write("Ask questions about your documents to get accurate, contextual answers.")
        
        # Back to home button
        if st.button("↩️ Back to Platform"):
            st.experimental_set_query_params()
            st.rerun()
        
        # Sidebar for app information
        with st.sidebar:
            st.header("About this App")
            st.write(f"**Instance ID:** {instance_id[:8]}...")
            st.write(f"**Created:** {datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else 'Unknown'}")
            st.write(f"**Embedding Model:** {embedding_model}")
            st.write(f"**LLM Model:** {llm_model}")
            
            # Toggle source visibility
            st.session_state.show_sources = st.toggle(
                "Show Source References", 
                value=st.session_state.show_sources
            )
            
            # Adjust retrieval parameters
            st.subheader("Retrieval Settings")
            st.session_state.context_window = st.slider(
                "Number of sources to retrieve", 
                min_value=1, 
                max_value=10, 
                value=st.session_state.context_window
            )
            
            # New conversation button
            if st.button("🔄 New Conversation"):
                st.session_state.chat_history = []
                st.session_state.current_sources = []
                st.rerun()
        
        # Chat interface
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Display sources if enabled
        if st.session_state.show_sources and st.session_state.current_sources:
            with st.expander("📚 Source References", expanded=False):
                for i, source in enumerate(st.session_state.current_sources, 1):
                    metadata = source.get('metadata', {})
                    url = metadata.get('url', '')
                    
                    st.markdown(f"### Reference {i}")
                    if url:
                        st.markdown(f"[🔗 {metadata.get('source', 'Source')}]({url})")
                    else:
                        st.markdown(f"**{metadata.get('source', 'Source')}**")
                    
                    # Show preview text
                    preview_text = source['text'][:300] + "..." if len(source['text']) > 300 else source['text']
                    st.caption(preview_text)
                    st.divider()
        
        # User input
        user_input = st.chat_input("Ask a question about your documents...")
        
        # Update the query processing in the main chat interface
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_input)
            
            # Create a placeholder for the streaming response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                
                try:
                    # Generate embedding for query
                    query_embedding = embedding_manager.generate_embeddings([user_input])[0]
                    relevant_docs = vector_store.search(
                        user_input,
                        query_embedding,
                        k=st.session_state.context_window
                    )
                    
                    # Save the current sources for potential display
                    st.session_state.current_sources = relevant_docs

                    # Generate response with enhanced LLM manager
                    response = llm_manager.generate_response(
                        user_input,
                        relevant_docs,
                        st.session_state.chat_history[-st.session_state.max_history:],
                        streaming_container=response_placeholder
                    )
                    
                    # Display the response
                    response_placeholder.markdown(response)

                    # Update chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    st.error(f"An error occurred during query processing: {str(e)}")
                    st.error("Full error details:")
                    st.exception(e)
    
    except Exception as e:
        st.error(f"Error loading instance: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        
        # Back to home button
        if st.button("Back to Home", key="back_error"):
            st.experimental_set_query_params()
            st.rerun()

def main():
    # Route based on instance_id parameter
    if instance_id:
        render_instance_page(instance_id)
    else:
        render_home_page()

if __name__ == "__main__":
    main()