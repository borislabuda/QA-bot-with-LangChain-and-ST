"""
Streamlit Interface for QA RAG Chatbot

This module provides a simple, functional Streamlit interface for the
QA RAG chatbot without fancy styling - focused on functionality.
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path

import streamlit as st

# Import our custom modules from src package
from src.document_loader import DocumentLoader
from src.vector_store_manager import VectorStoreManager
from src.qa_chain_manager import QAChainManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'vector_store_manager' not in st.session_state:
        st.session_state.vector_store_manager = None
    
    if 'qa_chain_manager' not in st.session_state:
        st.session_state.qa_chain_manager = None
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    
    if 'api_key_configured' not in st.session_state:
        st.session_state.api_key_configured = False


def setup_vector_store():
    """Initialize the vector store manager."""
    try:
        if st.session_state.vector_store_manager is None:
            # Use default configuration
            persist_dir = './chroma_db'
            embedding_model = 'text-embedding-ada-002'
            
            st.session_state.vector_store_manager = VectorStoreManager(
                persist_directory=persist_dir,
                embedding_model=embedding_model
            )
            
        return True
    except Exception as e:
        st.error(f"Error initializing vector store: {str(e)}")
        return False


def setup_qa_chain():
    """Initialize the QA chain manager."""
    try:
        if st.session_state.qa_chain_manager is None and st.session_state.vector_store_manager is not None:
            # Use default configuration
            model_name = 'gpt-3.5-turbo'
            max_tokens = 1000
            temperature = 0.1
            
            # Debug information
            st.info(f"Initializing QA chain with model: {model_name}, temperature: {temperature}")
            
            # Get retriever from vector store
            retriever = st.session_state.vector_store_manager.as_retriever()
            
            if retriever is not None:
                st.session_state.qa_chain_manager = QAChainManager(
                    retriever=retriever,
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                st.success("QA chain initialized successfully!")
                return True
            else:
                st.error("Failed to create retriever from vector store")
                return False
        elif st.session_state.qa_chain_manager is not None:
            return True  # Already initialized
        else:
            st.error("Vector store not initialized. Please upload documents first.")
            return False
    except Exception as e:
        st.error(f"Error initializing QA chain: {str(e)}")
        st.error(f"Error type: {type(e).__name__}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return False


def document_upload_section():
    """Handle document upload and processing."""
    st.header("📄 Document Management")
    
    # Check if API key is configured
    if not st.session_state.get('api_key_configured', False):
        st.warning("⚠️ Please configure your OpenAI API key in the sidebar first.")
        return
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, TXT, DOCX)",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True,
        help="Upload documents to add to the knowledge base"
    )
    
    # Directory upload option
    st.subheader("Or load from directory")
    directory_path = st.text_input(
        "Directory path",
        placeholder="Enter path to directory containing documents",
        help="Path to folder containing PDF, TXT, or DOCX files"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Process Uploaded Files", disabled=not uploaded_files):
            process_uploaded_files(uploaded_files)
    
    with col2:
        if st.button("Load from Directory", disabled=not directory_path):
            process_directory(directory_path)
    
    with col3:
        if st.button("Clear Vector Store"):
            clear_vector_store()


def process_uploaded_files(uploaded_files):
    """Process uploaded files and add to vector store."""
    if not setup_vector_store():
        return
    
    try:
        # Create temporary directory for uploaded files
        temp_dir = Path("./temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        
        # Save uploaded files temporarily
        temp_file_paths = []
        for uploaded_file in uploaded_files:
            temp_file_path = temp_dir / uploaded_file.name
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_file_paths.append(str(temp_file_path))
        
        # Initialize document loader
        loader = DocumentLoader()
        
        # Load and process documents
        with st.spinner("Processing documents..."):
            documents = loader.load_multiple_files(temp_file_paths)
            
            if documents:
                # Add to vector store
                doc_ids = st.session_state.vector_store_manager.add_documents(documents)
                st.success(f"Successfully processed {len(documents)} document chunks from {len(uploaded_files)} files")
                st.session_state.documents_loaded = True
                
                # Clean up temporary files
                for temp_file_path in temp_file_paths:
                    Path(temp_file_path).unlink(missing_ok=True)
                temp_dir.rmdir()
                
            else:
                st.error("No documents could be processed")
    
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
        logger.error(f"Error processing uploaded files: {str(e)}")


def process_directory(directory_path):
    """Process documents from a directory."""
    if not setup_vector_store():
        return
    
    try:
        # Initialize document loader
        loader = DocumentLoader()
        
        # Load documents from directory
        with st.spinner("Loading documents from directory..."):
            documents = loader.load_directory(directory_path)
            
            if documents:
                # Add to vector store
                doc_ids = st.session_state.vector_store_manager.add_documents(documents)
                st.success(f"Successfully processed {len(documents)} document chunks from directory")
                st.session_state.documents_loaded = True
            else:
                st.error("No supported documents found in directory")
    
    except Exception as e:
        st.error(f"Error processing directory: {str(e)}")
        logger.error(f"Error processing directory: {str(e)}")


def clear_vector_store():
    """Clear the vector store."""
    if st.session_state.vector_store_manager is not None:
        try:
            st.session_state.vector_store_manager.delete_collection()
            st.session_state.documents_loaded = False
            st.session_state.qa_chain_manager = None
            st.success("Vector store cleared successfully")
        except Exception as e:
            st.error(f"Error clearing vector store: {str(e)}")


def qa_chat_section():
    """Handle the QA chat interface."""
    st.header("💬 Ask Questions")
    
    # Check if API key is configured
    if not st.session_state.get('api_key_configured', False):
        st.warning("⚠️ Please configure your OpenAI API key in the sidebar first.")
        return
    
    # Check if we have documents loaded
    if not st.session_state.documents_loaded:
        st.warning("Please upload and process documents first before asking questions.")
        return
    
    # Setup QA chain if not already done
    if not setup_qa_chain():
        st.error("Failed to initialize QA system. Please check your configuration.")
        return
    
    # Chat input
    question = st.text_input(
        "Ask a question about your documents:",
        placeholder="Enter your question here...",
        key="question_input"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        ask_button = st.button("Ask Question", disabled=not question.strip())
    
    with col2:
        if st.button("Clear Chat History"):
            st.session_state.qa_chain_manager.clear_history()
            st.session_state.conversation_history = []
            st.success("Chat history cleared")
    
    # Process question
    if ask_button and question.strip():
        process_question(question)
    
    # Display conversation history
    display_conversation_history()


def process_question(question: str):
    """Process a user question and display the response."""
    try:
        with st.spinner("Generating answer..."):
            # Get response from QA chain
            response = st.session_state.qa_chain_manager.ask_question(question)
            
            if response.get('success', False):
                # Add to session conversation history
                st.session_state.conversation_history.append(response)
                
                # Display the response
                display_qa_response(response)
            else:
                st.error(f"Error: {response.get('error', 'Unknown error')}")
    
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")
        logger.error(f"Error processing question: {str(e)}")


def display_qa_response(response: Dict[str, Any]):
    """Display a QA response with sources."""
    st.subheader("Answer:")
    st.write(response['answer'])
    
    # Display source documents
    if response.get('source_documents'):
        with st.expander(f"📚 Source Documents ({len(response['source_documents'])})"):
            for i, source in enumerate(response['source_documents'], 1):
                st.write(f"**Source {i}:**")
                st.write(source['content'])
                
                # Display metadata if available
                if source.get('metadata'):
                    metadata = source['metadata']
                    if 'file_name' in metadata:
                        st.write(f"*File: {metadata['file_name']}*")
                
                if i < len(response['source_documents']):
                    st.divider()


def display_conversation_history():
    """Display the conversation history."""
    if st.session_state.conversation_history:
        st.subheader("📝 Conversation History")
        
        # Reverse to show newest first
        for i, entry in enumerate(reversed(st.session_state.conversation_history)):
            with st.expander(f"Q: {entry['question'][:60]}..." if len(entry['question']) > 60 else f"Q: {entry['question']}"):
                st.write("**Question:**")
                st.write(entry['question'])
                st.write("**Answer:**")
                st.write(entry['answer'])
                st.write(f"*{entry.get('source_count', 0)} sources used*")


def sidebar_info():
    """Display information in the sidebar."""
    with st.sidebar:
        st.header("ℹ️ System Info")
        
        # Vector store info
        if st.session_state.vector_store_manager is not None:
            try:
                info = st.session_state.vector_store_manager.get_collection_info()
                st.write("**Vector Store:**")
                st.write(f"Documents: {info.get('document_count', 'Unknown')}")
                st.write(f"Collection: {info.get('collection_name', 'Unknown')}")
            except Exception as e:
                st.write(f"Vector store error: {str(e)}")
        
        # QA chain info
        if st.session_state.qa_chain_manager is not None:
            try:
                memory_info = st.session_state.qa_chain_manager.get_memory_summary()
                st.write("**Chat Memory:**")
                st.write(f"Conversations: {memory_info.get('total_conversations', 0)}")
                st.write(f"Memory window: {memory_info.get('memory_window', 0)}")
            except Exception as e:
                st.write(f"Memory error: {str(e)}")
        
        # Configuration
        st.write("**Configuration:**")
        st.write(f"Model: {os.getenv('CHAT_MODEL', 'gpt-3.5-turbo')}")
        st.write(f"Temperature: {os.getenv('TEMPERATURE', '0.1')}")
        st.write(f"Max tokens: {os.getenv('MAX_TOKENS', '1000')}")


def configure_api_key():
    """Handle OpenAI API key configuration."""
    st.sidebar.header("🔑 API Configuration")
    
    # Check if API key is already set in environment
    env_api_key = os.getenv('OPENAI_API_KEY')
    
    if env_api_key and not st.sidebar.checkbox("Use different API key"):
        st.sidebar.success("✅ API key found in environment")
        os.environ['OPENAI_API_KEY'] = env_api_key
        st.session_state.api_key_configured = True
        return True
    
    # Input field for API key
    api_key = st.sidebar.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys"
    )
    
    if api_key:
        # Validate API key format (basic check)
        if api_key.startswith('sk-') and len(api_key) > 20:
            os.environ['OPENAI_API_KEY'] = api_key
            st.session_state.api_key_configured = True
            st.sidebar.success("✅ API key configured!")
            return True
        else:
            st.sidebar.error("❌ Invalid API key format. Should start with 'sk-'")
            return False
    else:
        if not env_api_key:
            st.sidebar.warning("⚠️ Please enter your OpenAI API key to continue")
            st.sidebar.info("You can find your API key at: https://platform.openai.com/api-keys")
        return False


def main():
    """Main Streamlit application."""
    # Page configuration
    st.set_page_config(
        page_title="QA RAG Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Ensure no accidental session state display
    if hasattr(st.session_state, '_debug') and st.session_state._debug:
        st.session_state._debug = False
    
    # Hide Streamlit style and menu for cleaner look
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp > header {display: none;}
        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
        .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK {display: none;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Main title
    st.title("🤖 QA RAG Chatbot")
    st.write("Upload documents and ask questions about their content using AI-powered retrieval.")
    
    # Always show the sidebar with API key configuration
    api_key_configured = configure_api_key()
    
    # Show main content only if API key is configured
    if not api_key_configured:
        st.info("👆 Please configure your OpenAI API key in the sidebar to continue.")
    else:
        # Main content in tabs
        tab1, tab2 = st.tabs(["📄 Documents", "💬 Chat"])
        
        with tab1:
            document_upload_section()
        
        with tab2:
            qa_chat_section()
    
    # Sidebar
    sidebar_info()


if __name__ == "__main__":
    # Check if running in Streamlit context
    try:
        import streamlit as st
        # This will raise an exception if not in Streamlit context
        st.session_state
        main()
    except:
        print("ERROR: This script must be run with Streamlit!")
        print("Please use: streamlit run app.py")
        print("Or run: .\\run.bat")
        exit(1)
