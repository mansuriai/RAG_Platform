# ## platform_ui.py

# import streamlit as st
# import os
# import sys
# import time
# import uuid
# from pathlib import Path
# import json
# import subprocess
# import threading

# # Add parent directory to path
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# # from app.instance_creator import InstanceCreator
# # from app.instance_manager import InstanceManager
# # from platform_core.config_manager import ConfigManager      ###
# # from platform_core.port_manager import PortManager          ##

# # Get the absolute path of the parent directory (automated_platform)
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# # Add it to sys.path if not already present
# if parent_dir not in sys.path:
#     sys.path.append(parent_dir)

# # Now use direct imports (no 'app.' prefix since we added parent_dir to path)
# from app.instance_creator import InstanceCreator
# from app.instance_manager import InstanceManager
# from platform_core.config_manager import ConfigManager
# from platform_core.port_manager import PortManager

# # Initialize components
# instance_creator = InstanceCreator()
# instance_manager = InstanceManager()
# config_manager = ConfigManager()
# port_manager = PortManager()

# # Set page config
# st.set_page_config(
#     page_title="RAG Application Generator",
#     layout="wide"
# )

# # Initialize session state
# if "instance_id" not in st.session_state:
#     st.session_state.instance_id = None
# if "deployment_status" not in st.session_state:
#     st.session_state.deployment_status = ""
# if "uploaded_pdfs" not in st.session_state:
#     st.session_state.uploaded_pdfs = []
# if "urls" not in st.session_state:
#     st.session_state.urls = []

# def deploy_instance_async(instance_id, port):
#     """Deploy the instance in a separate thread"""
#     try:
#         instance_manager.start_instance(instance_id, port)
#         st.session_state.deployment_status = f"Deployed! Access your RAG application at: http://localhost:{port}"
#     except Exception as e:
#         st.session_state.deployment_status = f"Deployment failed: {str(e)}"

# def main():
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
#         app_name = st.text_input("Application Name", "My RAG App")
        
#         # Model selection
#         embedding_model = st.selectbox(
#             "Embedding Model",
#             [
#                 "sentence-transformers/all-mpnet-base-v2",
#                 "sentence-transformers/all-MiniLM-L6-v2",
#                 "BAAI/bge-small-en-v1.5",
#                 "BAAI/bge-base-en-v1.5"
#             ]
#         )
        
#         llm_model = st.selectbox(
#             "LLM Model",
#             [
#                 "gpt-3.5-turbo",
#                 "gpt-4",
#                 "gpt-4-turbo",
#                 "claude-3-opus-20240229",
#                 "claude-3-sonnet-20240229"
#             ]
#         )
        
#         # Vector store selection
#         vector_store = st.selectbox(
#             "Vector Store Platform",
#             [
#                 "Pinecone",
#                 "Chroma (Local)",
#                 "FAISS (Local)"
#             ]
#         )
        
#         # Advanced settings
#         with st.expander("Advanced Settings", expanded=False):
#             chunk_size = st.slider("Chunk Size", 500, 2000, 1000)
#             chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200)
#             top_k = st.slider("Top K Results", 1, 10, 5)
            
#             st.subheader("API Keys")
#             if llm_model.startswith("gpt"):
#                 openai_api_key = st.text_input("OpenAI API Key", type="password")
#             elif llm_model.startswith("claude"):
#                 anthropic_api_key = st.text_input("Anthropic API Key", type="password")
            
#             if vector_store == "Pinecone":
#                 pinecone_api_key = st.text_input("Pinecone API Key", type="password")
#                 pinecone_environment = st.text_input("Pinecone Environment", "gcp-starter")
    
#     # Generation section
#     st.header("Generate Your Application")
    
#     if st.button("Generate and Deploy RAG Application"):
#         with st.spinner("Processing and deploying your RAG application..."):
#             # Validate inputs
#             if not st.session_state.uploaded_pdfs and not st.session_state.urls:
#                 st.error("Please upload at least one PDF document or add at least one URL.")
#                 return
            
#             # Create unique instance ID
#             instance_id = str(uuid.uuid4())
#             st.session_state.instance_id = instance_id
            
#             # Create instance configuration
#             config = {
#                 "instance_id": instance_id,
#                 "app_name": app_name,
#                 "embedding_model": embedding_model,
#                 "llm_model": llm_model,
#                 "vector_store": vector_store,
#                 "chunk_size": chunk_size,
#                 "chunk_overlap": chunk_overlap,
#                 "top_k": top_k,
#                 "created_at": time.time()
#             }
            
#             # Add API keys to config
#             if llm_model.startswith("gpt") and 'openai_api_key' in locals():
#                 config["openai_api_key"] = openai_api_key
#             elif llm_model.startswith("claude") and 'anthropic_api_key' in locals():
#                 config["anthropic_api_key"] = anthropic_api_key
            
#             if vector_store == "Pinecone" and 'pinecone_api_key' in locals():
#                 config["pinecone_api_key"] = pinecone_api_key
#                 config["pinecone_environment"] = pinecone_environment
            
#             # Save configuration
#             config_manager.save_config(instance_id, config)
            
#             # Process PDFs
#             pdf_paths = []
#             for pdf in st.session_state.uploaded_pdfs:
#                 pdf_path = os.path.join(config_manager.get_instance_dir(instance_id), "pdfs", pdf.name)
#                 os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
#                 with open(pdf_path, 'wb') as f:
#                     f.write(pdf.getvalue())
#                 pdf_paths.append(pdf_path)
            
#             # Save URLs
#             if st.session_state.urls:
#                 urls_file = os.path.join(config_manager.get_instance_dir(instance_id), "urls.txt")
#                 with open(urls_file, 'w') as f:
#                     for url in st.session_state.urls:
#                         f.write(f"{url}\n")
            
#             # Create the instance
#             instance_creator.create_instance(instance_id, config, pdf_paths, st.session_state.urls)
            
#             # Find available port
#             port = port_manager.get_available_port()
            
#             # Add port to config and update
#             config["port"] = port
#             config_manager.save_config(instance_id, config)
            
#             # Start deployment in a background thread
#             threading.Thread(
#                 target=deploy_instance_async,
#                 args=(instance_id, port)
#             ).start()
            
#             st.success(f"RAG application created with ID: {instance_id}")
#             st.info("Deploying your application... This may take a moment.")
    
#     # Display deployment status
#     if st.session_state.deployment_status:
#         if "Deployed!" in st.session_state.deployment_status:
#             st.success(st.session_state.deployment_status)
#         else:
#             st.error(st.session_state.deployment_status)
    
#     # Instance management section
#     st.header("Manage Your Instances")
    
#     instances = instance_manager.list_instances()
#     if instances:
#         st.write(f"You have {len(instances)} active instances:")
        
#         for instance in instances:
#             with st.expander(f"{instance['app_name']} ({instance['instance_id']})"):
#                 st.write(f"**Status:** {'Running' if instance['running'] else 'Stopped'}")
#                 st.write(f"**URL:** http://localhost:{instance['port']}")
#                 st.write(f"**Created:** {time.ctime(instance['created_at'])}")
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if instance['running']:
#                         if st.button(f"Stop {instance['app_name']}", key=f"stop_{instance['instance_id']}"):
#                             instance_manager.stop_instance(instance['instance_id'])
#                             st.rerun()
#                     else:
#                         if st.button(f"Start {instance['app_name']}", key=f"start_{instance['instance_id']}"):
#                             instance_manager.start_instance(instance['instance_id'], instance['port'])
#                             st.rerun()
                
#                 with col2:
#                     if st.button(f"Delete {instance['app_name']}", key=f"delete_{instance['instance_id']}"):
#                         instance_manager.delete_instance(instance['instance_id'])
#                         st.rerun()
#     else:
#         st.info("No instances found. Generate a new RAG application to get started!")

# if __name__ == "__main__":
#     main()











#########################################

# platform_ui.py

import streamlit as st
import os
import sys
import time
import uuid
from pathlib import Path
import json
import subprocess
import threading
import webbrowser
import socket

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.instance_creator import InstanceCreator
from app.instance_manager import InstanceManager
from platform_core.config_manager import ConfigManager
from platform_core.port_manager import PortManager

# Initialize components
instance_creator = InstanceCreator()
instance_manager = InstanceManager()
config_manager = ConfigManager()
port_manager = PortManager()

# Set page config
st.set_page_config(
    page_title="RAG Application Generator",
    layout="wide"
)

# Initialize session state
if "instance_id" not in st.session_state:
    st.session_state.instance_id = None
if "deployment_status" not in st.session_state:
    st.session_state.deployment_status = ""
if "uploaded_pdfs" not in st.session_state:
    st.session_state.uploaded_pdfs = []
if "urls" not in st.session_state:
    st.session_state.urls = []
if "open_browser" not in st.session_state:
    st.session_state.open_browser = False
if "app_url" not in st.session_state:
    st.session_state.app_url = ""

def check_port_available(port):
    """Check if a port is available on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def deploy_instance_async(instance_id, port):
    """Deploy the instance in a separate thread"""
    try:
        # First check if port is available
        if not check_port_available(port):
            st.session_state.deployment_status = f"Error: Port {port} is already in use by another application"
            return

        # Start the instance
        success = instance_manager.start_instance(instance_id, port)
        
        if success:
            # Create app URL
            app_url = f"http://localhost:{port}"
            st.session_state.app_url = app_url
            
            # Create direct start script for backup
            instance_dir = config_manager.get_instance_dir(instance_id)
            with open(os.path.join(instance_dir, "direct_start.bat"), 'w') as f:
                f.write("@echo off\n")
                f.write("echo Starting RAG Application directly...\n")
                f.write(f"set PORT={port}\n")
                f.write("set PYTHONPATH=%CD%\n\n")
                f.write("echo Current directory: %CD%\n")
                f.write("echo Python path: %PYTHONPATH%\n\n")
                f.write(f"streamlit run app\\main.py --server.port {port} --server.address localhost --browser.gatherUsageStats false\n\n")
                f.write("pause\n")
            
            # Set the deployment status
            st.session_state.deployment_status = "success"
            
            # Wait a bit for the server to start
            time.sleep(5)
            
            # Check if the server is running
            if check_port_available(port):
                st.session_state.deployment_status = f"Error: App failed to start on port {port}. Try running direct_start.bat in the instance directory."
            else:
                st.session_state.deployment_status = f"Deployed! Access your RAG application at: <a href='{app_url}' target='_blank'>{app_url}</a>"
                # Set flag to open browser
                st.session_state.open_browser = True
        else:
            st.session_state.deployment_status = "Failed to start the instance. Check logs for details."
    except Exception as e:
        st.session_state.deployment_status = f"Deployment failed: {str(e)}"

def main():
    st.title("RAG Application Generator")
    st.write("Upload documents, configure your RAG application, and get a dedicated deployment.")
    
    # Open browser if needed
    if st.session_state.open_browser and st.session_state.app_url:
        try:
            webbrowser.open(st.session_state.app_url)
            st.session_state.open_browser = False
        except:
            pass
    
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
        app_name = st.text_input("Application Name", "My RAG App")
        
        # Model selection
        embedding_model = st.selectbox(
            "Embedding Model",
            [
                "sentence-transformers/all-mpnet-base-v2",
                "sentence-transformers/all-MiniLM-L6-v2",
                "BAAI/bge-small-en-v1.5",
                "BAAI/bge-base-en-v1.5",
                "Snowflake/snowflake-arctic-embed-l-v2.0"
            ]
        )
        
        llm_model = st.selectbox(
            "LLM Model",
            [
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229"
            ]
        )
        
        # Vector store selection
        vector_store = st.selectbox(
            "Vector Store Platform",
            [
                "Pinecone",
                "Chroma (Local)",
                "FAISS (Local)"
            ]
        )
        
        # Advanced settings
        with st.expander("Advanced Settings", expanded=False):
            chunk_size = st.slider("Chunk Size", 500, 2000, 1000)
            chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200)
            top_k = st.slider("Top K Results", 1, 10, 5)
            
            st.subheader("API Keys")
            if llm_model.startswith("gpt"):
                openai_api_key = st.text_input("OpenAI API Key", type="password")
            elif llm_model.startswith("claude"):
                anthropic_api_key = st.text_input("Anthropic API Key", type="password")
            
            if vector_store == "Pinecone":
                pinecone_api_key = st.text_input("Pinecone API Key", type="password")
                pinecone_environment = st.text_input("Pinecone Environment", "gcp-starter")
    
    # Generation section
    st.header("Generate Your Application")
    
    if st.button("Generate and Deploy RAG Application"):
        with st.spinner("Processing and deploying your RAG application..."):
            # Validate inputs
            if not st.session_state.uploaded_pdfs and not st.session_state.urls:
                st.error("Please upload at least one PDF document or add at least one URL.")
                return
            
            # Create unique instance ID
            instance_id = str(uuid.uuid4())
            st.session_state.instance_id = instance_id
            
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
            if llm_model.startswith("gpt") and 'openai_api_key' in locals():
                config["openai_api_key"] = openai_api_key
            elif llm_model.startswith("claude") and 'anthropic_api_key' in locals():
                config["anthropic_api_key"] = anthropic_api_key
            
            if vector_store == "Pinecone" and 'pinecone_api_key' in locals():
                config["pinecone_api_key"] = pinecone_api_key
                config["pinecone_environment"] = pinecone_environment
            
            # Save configuration
            config_manager.save_config(instance_id, config)
            
            # Process PDFs
            pdf_paths = []
            for pdf in st.session_state.uploaded_pdfs:
                pdf_path = os.path.join(config_manager.get_instance_dir(instance_id), "pdfs", pdf.name)
                os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                with open(pdf_path, 'wb') as f:
                    f.write(pdf.getvalue())
                pdf_paths.append(pdf_path)
            
            # Save URLs
            if st.session_state.urls:
                urls_file = os.path.join(config_manager.get_instance_dir(instance_id), "urls.txt")
                os.makedirs(os.path.dirname(urls_file), exist_ok=True)
                with open(urls_file, 'w') as f:
                    for url in st.session_state.urls:
                        f.write(f"{url}\n")
            
            # Create the instance
            instance_creator.create_instance(instance_id, config, pdf_paths, st.session_state.urls)
            
            # Find available port
            port = port_manager.get_available_port()
            
            # Add port to config and update
            config["port"] = port
            config_manager.save_config(instance_id, config)
            
            # Start deployment in a background thread
            threading.Thread(
                target=deploy_instance_async,
                args=(instance_id, port)
            ).start()
            
            st.success(f"RAG application created with ID: {instance_id}")
            st.info("Deploying your application... This may take a moment.")
    
    # Display deployment status
    if st.session_state.deployment_status:
        if st.session_state.deployment_status.startswith("Deployed!"):
            st.success(st.session_state.deployment_status)
            st.markdown(st.session_state.deployment_status, unsafe_allow_html=True)
        elif st.session_state.deployment_status.startswith("Error:"):
            st.error(st.session_state.deployment_status)
        else:
            st.info(st.session_state.deployment_status)
    
    # Instance management section
    st.header("Manage Your Instances")
    
    instances = instance_manager.list_instances()
    if instances:
        st.write(f"You have {len(instances)} active instances:")
        
        for instance in instances:
            with st.expander(f"{instance['app_name']} ({instance['instance_id']})"):
                st.write(f"**Status:** {'Running' if instance['running'] else 'Stopped'}")
                
                # Display URL with clickable link
                app_url = f"http://localhost:{instance['port']}"
                st.markdown(f"**URL:** <a href='{app_url}' target='_blank'>{app_url}</a>", unsafe_allow_html=True)
                
                st.write(f"**Created:** {time.ctime(instance['created_at'])}")
                
                # Show direct start instructions
                instance_dir = config_manager.get_instance_dir(instance['instance_id'])
                direct_start_path = os.path.join(instance_dir, "direct_start.bat")
                
                if os.path.exists(direct_start_path):
                    st.info(f"If the URL doesn't work, you can run the 'direct_start.bat' script in: {instance_dir}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if instance['running']:
                        if st.button(f"Stop {instance['app_name']}", key=f"stop_{instance['instance_id']}"):
                            instance_manager.stop_instance(instance['instance_id'])
                            st.rerun()
                    else:
                        if st.button(f"Start {instance['app_name']}", key=f"start_{instance['instance_id']}"):
                            instance_manager.start_instance(instance['instance_id'], instance['port'])
                            # Open URL
                            webbrowser.open(app_url)
                            st.rerun()
                
                with col2:
                    if st.button(f"Delete {instance['app_name']}", key=f"delete_{instance['instance_id']}"):
                        instance_manager.delete_instance(instance['instance_id'])
                        st.rerun()
                
                # Open URL button
                if st.button(f"Open {instance['app_name']} in Browser", key=f"open_{instance['instance_id']}"):
                    try:
                        webbrowser.open(app_url)
                    except:
                        st.error("Failed to open browser automatically. Please click the URL link above.")
    else:
        st.info("No instances found. Generate a new RAG application to get started!")

if __name__ == "__main__":
    main()