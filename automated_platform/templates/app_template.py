# ## app_template.py

# import streamlit as st
# from pathlib import Path
# import time
# from typing import List, Dict
# import os, sys
# import urllib.parse

# # Add parent directory to path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from utils.config import config

# # Set page config as the first Streamlit command
# st.set_page_config(
#     page_title=config.APP_TITLE,
#     layout="wide",
# )

# from core.embeddings import EmbeddingManager
# from core.vector_store import VectorStore
# from core.llm import LLMManager

# def check_environment():
#     """Check if all required environment variables are set."""
#     missing_vars = []
   
#     if config.LLM_MODEL.startswith('gpt') and not config.OPENAI_API_KEY:
#         missing_vars.append("OPENAI_API_KEY")
#     elif config.LLM_MODEL.startswith('claude') and not config.ANTHROPIC_API_KEY:
#         missing_vars.append("ANTHROPIC_API_KEY")
       
#     if config.PINECONE_API_KEY is None:
#         missing_vars.append("PINECONE_API_KEY")
#     if config.PINECONE_ENVIRONMENT is None:
#         missing_vars.append("PINECONE_ENVIRONMENT")
   
#     if missing_vars:
#         error_msg = f"Missing required environment variables: {', '.join(missing_vars)}\n"
#         error_msg += "Please ensure these variables are set in your .env file or environment."
#         raise ValueError(error_msg)

# def display_sources(sources: List[Dict]):
#     """Display sources with proper formatting and links."""
#     if not sources:
#         return
   
#     with st.expander("📚 Source References", expanded=False):
#         for i, source in enumerate(sources, 1):
#             metadata = source.get('metadata', {})
#             url = metadata.get('url', '')
           
#             st.markdown(f"### Reference {i}")
#             if url:
#                 st.markdown(f"[🔗 {metadata.get('source', 'Source')}]({url})")
#             else:
#                 st.markdown(f"**{metadata.get('source', 'Source')}**")
           
#             # Show preview text
#             preview_text = source['text'][:300] + "..." if len(source['text']) > 300 else source['text']
#             st.caption(preview_text)
#             st.divider()

# @st.cache_resource
# def initialize_components():
#     try:
#         # Check environment variables first
#         check_environment()
       
#         # Initialize components one by one with better error handling
#         try:
#             embedding_manager = EmbeddingManager(model_name=config.EMBEDDING_MODEL)
#         except Exception as e:
#             st.error(f"Embedding Manager Error: {str(e)}")
#             return None
           
#         try:
#             vector_store = VectorStore()
#         except Exception as e:
#             st.error(f"Vector Store Error: {str(e)}")
#             return None
           
#         try:
#             llm_manager = LLMManager()
#         except Exception as e:
#             st.error(f"LLM Manager Error: {str(e)}")
#             return None
       
#         components = {
#             'embedding_manager': embedding_manager,
#             'vector_store': vector_store,
#             'llm_manager': llm_manager
#         }
       
#         return components
#     except Exception as e:
#         st.error(f"Initialization Error: {str(e)}")
#         st.info("Please check your .env file and ensure all required API keys are set correctly.")
#         return None
   

# components = initialize_components()

# if components is None:
#     st.stop()

# embedding_manager = components['embedding_manager']
# vector_store = components['vector_store']
# llm_manager = components['llm_manager']

# # Initialize session state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "current_sources" not in st.session_state:
#     st.session_state.current_sources = []
# if "context_window" not in st.session_state:
#     st.session_state.context_window = config.TOP_K
# if "max_history" not in st.session_state:
#     st.session_state.max_history = 10
# if "show_sources" not in st.session_state:
#     st.session_state.show_sources = False

# st.title(config.APP_TITLE)

# st.markdown("""
# This is your custom RAG (Retrieval-Augmented Generation) application.
# Ask questions about the documents you've uploaded to get accurate, contextual answers.
# """)

# # Sidebar for app information
# with st.sidebar:
#     st.header("About this App")
#     st.write(f"**Instance ID:** {config.INSTANCE_ID}")
#     st.write(f"**Embedding Model:** {config.EMBEDDING_MODEL}")
#     st.write(f"**LLM Model:** {config.LLM_MODEL}")
   
#     # Toggle source visibility
#     st.session_state.show_sources = st.toggle(
#         "Show Source References",
#         value=st.session_state.show_sources
#     )
   
#     # Adjust retrieval parameters
#     st.subheader("Retrieval Settings")
#     st.session_state.context_window = st.slider(
#         "Number of sources to retrieve",
#         min_value=1,
#         max_value=10,
#         value=st.session_state.context_window
#     )
   
#     # New conversation button
#     if st.button("🔄 New Conversation"):
#         st.session_state.chat_history = []
#         st.session_state.current_sources = []
#         st.rerun()

# # Chat interface
# for message in st.session_state.chat_history:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # Display sources if enabled
# if st.session_state.show_sources and st.session_state.current_sources:
#     display_sources(st.session_state.current_sources)

# # User input
# user_input = st.chat_input("Ask a question about your documents...")

# # Update the query processing in the main chat interface
# if user_input:
#     # Add user message to chat history
#     st.session_state.chat_history.append({
#         "role": "user",
#         "content": user_input
#     })
   
#     # Display user message
#     with st.chat_message("user"):
#         st.write(user_input)
   
#     # Create a placeholder for the streaming response
#     with st.chat_message("assistant"):
#         response_placeholder = st.empty()
       
#         try:
#             # Generate embedding for query
#             query_embedding = embedding_manager.generate_embeddings([user_input])[0]
#             relevant_docs = vector_store.search(
#                 user_input,
#                 query_embedding,
#                 k=st.session_state.context_window
#             )
           
#             # Save the current sources for potential display
#             st.session_state.current_sources = relevant_docs

#             # Generate response with enhanced LLM manager
#             response = llm_manager.generate_response(
#                 user_input,
#                 relevant_docs,
#                 st.session_state.chat_history[-st.session_state.max_history:],
#                 streaming_container=response_placeholder
#             )
           
#             # Display the response
#             response_placeholder.markdown(response)
           
#             # Display sources separately
#             if st.session_state.show_sources:
#                 display_sources(relevant_docs)

#             # Update chat history
#             st.session_state.chat_history.append({
#                 "role": "assistant",
#                 "content": response
#             })
           
#         except Exception as e:
#             st.error(f"An error occurred during query processing: {str(e)}")
#             st.error("Full error details:")
#             st.exception(e)








#############################################



## app_template.py

# import streamlit as st
# from pathlib import Path
# import time
# from typing import List, Dict
# import os, sys
# import urllib.parse

# # Add parent directory to path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from utils.config import config

# # Set page config as the first Streamlit command
# st.set_page_config(
#     page_title=config.APP_TITLE,
#     layout="wide",
# )

# from core.embeddings import EmbeddingManager
# from core.vector_store import VectorStore
# from core.llm import LLMManager

# def check_environment():
#     """Check if all required environment variables are set."""
#     missing_vars = []
    
#     if config.LLM_MODEL.startswith('gpt') and not config.OPENAI_API_KEY:
#         missing_vars.append("OPENAI_API_KEY")
#     elif config.LLM_MODEL.startswith('claude') and not config.ANTHROPIC_API_KEY:
#         missing_vars.append("ANTHROPIC_API_KEY")
        
#     if config.PINECONE_API_KEY is None:
#         missing_vars.append("PINECONE_API_KEY")
#     if config.PINECONE_ENVIRONMENT is None:
#         missing_vars.append("PINECONE_ENVIRONMENT")
    
#     if missing_vars:
#         error_msg = f"Missing required environment variables: {', '.join(missing_vars)}\n"
#         error_msg += "Please ensure these variables are set in your .env file or environment."
#         st.error(error_msg)
#         return False
#     return True

# def display_sources(sources: List[Dict]):
#     """Display sources with proper formatting and links."""
#     if not sources:
#         return
    
#     with st.expander("📚 Source References", expanded=False):
#         for i, source in enumerate(sources, 1):
#             metadata = source.get('metadata', {})
#             url = metadata.get('url', '')
            
#             st.markdown(f"### Reference {i}")
#             if url:
#                 st.markdown(f"[🔗 {metadata.get('source', 'Source')}]({url})")
#             else:
#                 st.markdown(f"**{metadata.get('source', 'Source')}**")
            
#             # Show preview text
#             preview_text = source['text'][:300] + "..." if len(source['text']) > 300 else source['text']
#             st.caption(preview_text)
#             st.divider()

# @st.cache_resource
# def initialize_components():
#     try:
#         # Check environment variables first
#         if not check_environment():
#             return None
        
#         # Initialize components one by one with better error handling
#         try:
#             embedding_manager = EmbeddingManager()
#         except Exception as e:
#             st.error(f"Embedding Manager Error: {str(e)}")
#             return None
            
#         try:
#             vector_store = VectorStore()
#         except Exception as e:
#             st.error(f"Vector Store Error: {str(e)}")
#             return None
            
#         try:
#             llm_manager = LLMManager()
#         except Exception as e:
#             st.error(f"LLM Manager Error: {str(e)}")
#             return None
        
#         components = {
#             'embedding_manager': embedding_manager,
#             'vector_store': vector_store,
#             'llm_manager': llm_manager
#         }
        
#         return components
#     except Exception as e:
#         st.error(f"Initialization Error: {str(e)}")
#         st.info("Please check your .env file and ensure all required API keys are set correctly.")
#         return None
    

# def main():
#     # Initialize components
#     components = initialize_components()

#     if components is None:
#         st.write("Failed to initialize components. Check the errors above.")
#         return

#     embedding_manager = components['embedding_manager']
#     vector_store = components['vector_store']
#     llm_manager = components['llm_manager']

#     # Initialize session state
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#     if "current_sources" not in st.session_state:
#         st.session_state.current_sources = []
#     if "context_window" not in st.session_state:
#         st.session_state.context_window = config.TOP_K
#     if "max_history" not in st.session_state:
#         st.session_state.max_history = 10
#     if "show_sources" not in st.session_state:
#         st.session_state.show_sources = False

#     st.title(config.APP_TITLE)

#     st.markdown("""
#     This is your custom RAG (Retrieval-Augmented Generation) application.
#     Ask questions about the documents you've uploaded to get accurate, contextual answers.
#     """)

#     # Sidebar for app information
#     with st.sidebar:
#         st.header("About this App")
#         st.write(f"**Instance ID:** {config.INSTANCE_ID}")
#         st.write(f"**Embedding Model:** {config.EMBEDDING_MODEL}")
#         st.write(f"**LLM Model:** {config.LLM_MODEL}")
        
#         # Toggle source visibility
#         st.session_state.show_sources = st.toggle(
#             "Show Source References", 
#             value=st.session_state.show_sources
#         )
        
#         # Adjust retrieval parameters
#         st.subheader("Retrieval Settings")
#         st.session_state.context_window = st.slider(
#             "Number of sources to retrieve", 
#             min_value=1, 
#             max_value=10, 
#             value=st.session_state.context_window
#         )
        
#         # New conversation button
#         if st.button("🔄 New Conversation"):
#             st.session_state.chat_history = []
#             st.session_state.current_sources = []
#             st.rerun()

#     # Chat interface
#     for message in st.session_state.chat_history:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # Display sources if enabled
#     if st.session_state.show_sources and st.session_state.current_sources:
#         display_sources(st.session_state.current_sources)

#     # User input
#     user_input = st.chat_input("Ask a question about your documents...")

#     # Update the query processing in the main chat interface
#     if user_input:
#         # Add user message to chat history
#         st.session_state.chat_history.append({
#             "role": "user",
#             "content": user_input
#         })
        
#         # Display user message
#         with st.chat_message("user"):
#             st.write(user_input)
        
#         # Create a placeholder for the streaming response
#         with st.chat_message("assistant"):
#             response_placeholder = st.empty()
            
#             try:
#                 # Generate embedding for query
#                 query_embedding = embedding_manager.generate_embeddings([user_input])[0]
#                 relevant_docs = vector_store.search(
#                     user_input,
#                     query_embedding,
#                     k=st.session_state.context_window
#                 )
                
#                 # Save the current sources for potential display
#                 st.session_state.current_sources = relevant_docs

#                 # Generate response with enhanced LLM manager
#                 response = llm_manager.generate_response(
#                     user_input,
#                     relevant_docs,
#                     st.session_state.chat_history[-st.session_state.max_history:],
#                     streaming_container=response_placeholder
#                 )
                
#                 # Display the response
#                 response_placeholder.markdown(response)
                
#                 # Display sources separately
#                 if st.session_state.show_sources:
#                     display_sources(relevant_docs)

#                 # Update chat history
#                 st.session_state.chat_history.append({
#                     "role": "assistant",
#                     "content": response
#                 })
                
#             except Exception as e:
#                 st.error(f"An error occurred during query processing: {str(e)}")
#                 st.error("Full error details:")
#                 st.exception(e)

# if __name__ == "__main__":
#     main()


################################


## app_template.py

import streamlit as st
from pathlib import Path
import time
import os
import sys
from typing import List, Dict
import urllib.parse

# Debug info
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load config
try:
    from utils.config import config
    print(f"Config loaded successfully: {config.APP_TITLE}")
except Exception as e:
    print(f"Error loading config: {str(e)}")
    st.error(f"Error loading configuration: {str(e)}")
    st.stop()

# Set page config as the first Streamlit command
st.set_page_config(
    page_title=config.APP_TITLE,
    layout="wide",
)

# Import components
try:
    from core.embeddings import EmbeddingManager
    from core.vector_store import VectorStore
    from core.llm import LLMManager
    print("Components imported successfully")
except Exception as e:
    print(f"Error importing components: {str(e)}")
    st.error(f"Error importing components: {str(e)}")
    st.stop()

def check_environment():
    """Check if all required environment variables are set."""
    missing_vars = []
    
    if config.LLM_MODEL.startswith('gpt') and not config.OPENAI_API_KEY:
        missing_vars.append("OPENAI_API_KEY")
    elif config.LLM_MODEL.startswith('claude') and not config.ANTHROPIC_API_KEY:
        missing_vars.append("ANTHROPIC_API_KEY")
        
    if config.PINECONE_API_KEY is None:
        missing_vars.append("PINECONE_API_KEY")
    if config.PINECONE_ENVIRONMENT is None:
        missing_vars.append("PINECONE_ENVIRONMENT")
    
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}\n"
        error_msg += "Please ensure these variables are set in your .env file or environment."
        st.error(error_msg)
        return False
    return True

def display_sources(sources: List[Dict]):
    """Display sources with proper formatting and links."""
    if not sources:
        return
    
    with st.expander("📚 Source References", expanded=False):
        for i, source in enumerate(sources, 1):
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

@st.cache_resource(show_spinner=False)
def initialize_components():
    try:
        # Check environment variables first
        if not check_environment():
            return None
        
        # Initialize components one by one with better error handling
        with st.spinner("Initializing embedding model..."):
            try:
                embedding_manager = EmbeddingManager()
                print("Embedding Manager initialized successfully")
            except Exception as e:
                print(f"Embedding Manager Error: {str(e)}")
                st.error(f"Embedding Manager Error: {str(e)}")
                return None
        
        with st.spinner("Connecting to vector store..."):    
            try:
                vector_store = VectorStore()
                print("Vector Store initialized successfully")
            except Exception as e:
                print(f"Vector Store Error: {str(e)}")
                st.error(f"Vector Store Error: {str(e)}")
                return None
        
        with st.spinner("Initializing LLM..."):
            try:
                llm_manager = LLMManager()
                print("LLM Manager initialized successfully")
            except Exception as e:
                print(f"LLM Manager Error: {str(e)}")
                st.error(f"LLM Manager Error: {str(e)}")
                return None
        
        components = {
            'embedding_manager': embedding_manager,
            'vector_store': vector_store,
            'llm_manager': llm_manager
        }
        
        return components
    except Exception as e:
        print(f"Initialization Error: {str(e)}")
        st.error(f"Initialization Error: {str(e)}")
        st.info("Please check your .env file and ensure all required API keys are set correctly.")
        return None

def main():
    st.title(config.APP_TITLE)

    st.markdown("""
    This is your custom RAG (Retrieval-Augmented Generation) application.
    Ask questions about the documents you've uploaded to get accurate, contextual answers.
    """)

    # Show loading spinner while initializing
    with st.spinner("Loading application components..."):
        # Initialize components
        components = initialize_components()

    if components is None:
        st.error("Failed to initialize components. Check the errors above.")
        return

    embedding_manager = components['embedding_manager']
    vector_store = components['vector_store']
    llm_manager = components['llm_manager']
    
    # Show success message
    st.success("Application initialized successfully!")

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_sources" not in st.session_state:
        st.session_state.current_sources = []
    if "context_window" not in st.session_state:
        st.session_state.context_window = config.TOP_K
    if "max_history" not in st.session_state:
        st.session_state.max_history = 10
    if "show_sources" not in st.session_state:
        st.session_state.show_sources = False

    # Sidebar for app information
    with st.sidebar:
        st.header("About this App")
        st.write(f"**Instance ID:** {config.INSTANCE_ID}")
        st.write(f"**Embedding Model:** {config.EMBEDDING_MODEL}")
        st.write(f"**LLM Model:** {config.LLM_MODEL}")
        
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
        display_sources(st.session_state.current_sources)

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
                
                # Display sources separately
                if st.session_state.show_sources:
                    display_sources(relevant_docs)

                # Update chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
            except Exception as e:
                st.error(f"An error occurred during query processing: {str(e)}")
                st.error("Full error details:")
                st.exception(e)

if __name__ == "__main__":
    main()