# QA RAG Chatbot - Complete Code Documentation

## Project Status: ✅ FULLY FUNCTIONAL

**Last Updated**: July 14, 2025  
**Status**: All components tested and verified working  
**Recent Updates**: 
- ✅ ChromaDB persist() compatibility issue resolved  
- ✅ User-friendly API key input interface implemented
- ✅ No environment setup required for end users
- ✅ Complete end-to-end testing verified

**Tested Components**: ✅ Document loading ✅ Vector store ✅ QA chain ✅ Streamlit interface ✅ API key management

## Table of Contents
- [Project Structure](#project-structure)
- [Core Concepts](#core-concepts)
- [File-by-File Documentation](#file-by-file-documentation)
  - [app.py - Main Application](#apppy---main-application)
  - [src/document_loader.py - Document Processing](#srcdocument_loaderpy---document-processing)
  - [src/vector_store_manager.py - Vector Database](#srcvector_store_managerpy---vector-database)
  - [src/qa_chain_manager.py - Question Answering](#srcqa_chain_managerpy---question-answering)
  - [tests/test_setup.py - System Testing](#tests/test_setuppy---system-testing)
  - [tests/debug_qa.py - Debugging Script](#tests/debug_qapy---debugging-script)
- [How to Run Tests](#how-to-run-tests)

---

## Project Structure

```
QA bot with LangChain and ST/
├── 📁 src/                          # Main source code package
│   ├── 📄 __init__.py              # Makes 'src' a Python package
│   ├── 📄 document_loader.py       # Loads and processes documents (PDF, TXT, DOCX)
│   ├── 📄 vector_store_manager.py  # Manages ChromaDB vector database
│   └── 📄 qa_chain_manager.py      # Handles question-answering logic
├── 📁 tests/                        # Test scripts and debugging tools
│   ├── 📄 test_setup.py            # System-wide tests
│   ├── 📄 test_vector_store.py     # Tests for the vector store
│   └── 📄 debug_qa.py              # Debugging script for the QA chain
├── 📄 app.py                       # Main Streamlit web application
├── 📄 requirements.txt             # Python package dependencies
├── 📄 .env.example                 # Template for environment variables
├── 📄 setup.bat                    # Windows setup script
├── 📄 run.bat                      # Windows run script
├── 📄 README.md                    # Basic project information
├── 📁 chroma_db/                   # Vector database storage (created automatically)
├── 📁 temp_uploads/                # Temporary file storage (created automatically)
└── 📁 sample_documents/            # Sample documents for testing (created by test script)
```

---

## Core Concepts

### What is a RAG (Retrieval-Augmented Generation) System?

A RAG system combines two important AI techniques:

### How Our System Works:

1. **Document Upload**: User uploads PDF, TXT, or DOCX files
2. **Document Processing**: Files are split into smaller chunks for better processing
3. **Vector Storage**: Document chunks are converted to mathematical vectors and stored using ChromaDB
4. **Question Processing**: When user asks a question, the system finds relevant document chunks
5. **Response Generation**: OpenAI GPT-3.5-turbo generates contextual answers using retrieved information
6. **Conversation Memory**: Chat history is maintained for follow-up questions and context continuity

### Technology Stack (Verified Working):
- **LangChain 0.1+**: ✅ RAG pipeline orchestration with ConversationalRetrievalChain
- **ChromaDB + langchain-chroma**: ✅ Vector database (persist() compatibility issue resolved)
- **OpenAI API**: ✅ text-embedding-ada-002 + gpt-3.5-turbo models
- **Streamlit 1.29+**: ✅ Web interface with session state management
- **Python 3.8+**: ✅ Core runtime with package management
5. **Answer Generation**: AI creates an answer using the relevant chunks as context

---

## File-by-File Documentation

---

## app.py - Main Application

This is the main file that creates the web interface using Streamlit. It's like the "front door" of our application.

### Imports and Setup

```python
import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import streamlit as st
from src.document_loader import DocumentLoader
from src.vector_store_manager import VectorStoreManager  
from src.qa_chain_manager import QAChainManager
```

**What this does**: These imports bring in all the tools we need. Think of it like gathering all your tools before starting a project.

### Function: `initialize_session_state()`

**Purpose**: Sets up "memory" for our web application so it remembers things between user interactions.

**Source Code:**
```python
def initialize_session_state():
    # Session state is like the app's memory - it remembers things between page refreshes
    # Check if we already have a vector store manager (our database connection)
    if 'vector_store_manager' not in st.session_state:
        st.session_state.vector_store_manager = None  # Start with no database connection
    
    # Check if we have a QA chain manager (our question-answering system)
    if 'qa_chain_manager' not in st.session_state:
        st.session_state.qa_chain_manager = None  # Start with no QA system
    
    # Check if we have conversation history (all previous questions and answers)
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []  # Start with empty chat history
    
    # Check if we've loaded any documents yet
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False  # Start with no documents loaded
    
    # Check if the user has entered their API key
    if 'api_key_configured' not in st.session_state:
        st.session_state.api_key_configured = False  # Start with no API key
```

**What it does in detail**:
- **Session state** is like the app's short-term memory
- When you click buttons or upload files, the app needs to remember what happened
- This function creates "storage boxes" for different pieces of information:
  - `vector_store_manager`: Remembers our database connection
  - `qa_chain_manager`: Remembers our question-answering system
  - `conversation_history`: Remembers all previous questions and answers
  - `documents_loaded`: Remembers if we've uploaded documents yet

**Beginner analogy**: Imagine you're having a conversation. You need to remember what was said earlier to understand new messages. Session state does this for web apps.

### Function: `setup_vector_store()`

**Purpose**: Sets up our document database (called a "vector store").

**Source Code:**
```python
def setup_vector_store():
    try:
        # Only create a new vector store if we don't already have one
        if st.session_state.vector_store_manager is None:
            # Set up the folder where our document database will be saved
            persist_dir = './chroma_db'  # This creates a folder called 'chroma_db'
            
            # Choose which AI model to use for converting text to numbers (vectors)
            embedding_model = 'text-embedding-ada-002'  # OpenAI's text-to-vector model
            
            # Create the vector store manager (our database controller)
            st.session_state.vector_store_manager = VectorStoreManager(
                persist_directory=persist_dir,      # Where to save the database
                embedding_model=embedding_model     # Which AI model to use
            )
        
        return True  # Tell the calling function that everything worked
    
    except Exception as e:
        # If anything goes wrong, show an error message to the user
        st.error(f"Error initializing vector store: {str(e)}")
        return False  # Tell the calling function that something failed
```

**What it does step by step**:
1. **Checks if database is already set up**: If it exists, don't create a new one
2. **Gets configuration**: Reads settings from environment variables (like database location)
3. **Creates database manager**: Sets up the system that will store and search documents
4. **Returns success/failure**: Tells the calling function if everything worked

**Key concepts for beginners**:
- **Vector store**: A special database that stores documents as mathematical vectors
- **Environment variables**: Configuration settings stored outside the code
- **Error handling**: Using try/except to gracefully handle problems

### Function: `setup_qa_chain()`

**Purpose**: Sets up the question-answering system that will generate responses.

**Source Code:**
```python
def setup_qa_chain():
    try:
        # Check if we need to create a new QA system AND we have a vector store ready
        if st.session_state.qa_chain_manager is None and st.session_state.vector_store_manager is not None:
            
            # Configure the AI model settings
            model_name = 'gpt-3.5-turbo'    # Which OpenAI model to use for generating answers
            max_tokens = 1000               # Maximum length of AI responses (about 750 words)
            temperature = 0.1               # How creative the AI should be (0.1 = very focused)
            
            # Show the user what we're setting up
            st.info(f"Initializing QA chain with model: {model_name}, temperature: {temperature}")
            
            # Get the retriever (search engine) from our vector store
            retriever = st.session_state.vector_store_manager.as_retriever()
            
            # Make sure the retriever was created successfully
            if retriever is not None:
                # Create the QA chain manager (the "brain" of our system)
                st.session_state.qa_chain_manager = QAChainManager(
                    retriever=retriever,           # The search engine for finding relevant documents
                    model_name=model_name,         # Which AI model to use
                    temperature=temperature,       # How creative/focused the AI should be
                    max_tokens=max_tokens         # Maximum response length
                )
                
                # Tell the user everything worked
                st.success("QA chain initialized successfully!")
                return True  # Success!
            else:
                # The retriever couldn't be created
                st.error("Failed to create retriever from vector store")
                return False  # Failure
                
        elif st.session_state.qa_chain_manager is not None:
            # We already have a QA system set up
            return True  # Already working
        else:
            # We don't have documents loaded yet
            st.error("Vector store not initialized. Please upload documents first.")
            return False  # Can't work without documents
            
    except Exception as e:
        # If anything goes wrong, show detailed error information
        st.error(f"Error initializing QA chain: {str(e)}")
        st.error(f"Error type: {type(e).__name__}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return False  # Something went wrong
```

**What it does in detail**:
1. **Checks prerequisites**: Makes sure the vector store is ready first
2. **Gets AI model settings**: Retrieves configuration for the AI model (like temperature, max tokens)
3. **Creates retriever**: Sets up the system that finds relevant documents
4. **Initializes QA system**: Creates the component that generates answers
5. **Returns status**: Indicates success or failure

**Beginner concepts**:
- **QA Chain**: The "brain" that reads documents and answers questions
- **Retriever**: The "search engine" that finds relevant document pieces
- **Temperature**: Controls how creative vs. focused the AI responses are (0 = very focused, 1 = very creative)
- **Max tokens**: Limits how long the AI's response can be

### Function: `document_upload_section()`

**Purpose**: Creates the web interface section where users can upload documents.

**Source Code:**
```python
def document_upload_section():
    # Create a header for this section of the web page
    st.header("📄 Document Management")
    
    # Check if the user has entered their API key yet
    if not st.session_state.get('api_key_configured', False):
        # Show a warning if no API key is configured
        st.warning("⚠️ Please configure your OpenAI API key in the sidebar first.")
        return  # Stop here - can't work without API key
    
    # Create a file uploader widget that accepts multiple files
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, TXT, DOCX)",     # Label shown to user
        type=['pdf', 'txt', 'docx'],            # Only allow these file types
        accept_multiple_files=True,              # User can select multiple files at once
        help="Upload documents to add to the knowledge base"  # Tooltip help text
    )
    
    # Create a subheader for the directory option
    st.subheader("Or load from directory")
    
    # Create a text input box for entering a folder path
    directory_path = st.text_input(
        "Directory path",                                        # Label
        placeholder="Enter path to directory containing documents",  # Hint text
        help="Path to folder containing PDF, TXT, or DOCX files"    # Tooltip
    )
    
    # Create three columns for our buttons (makes them appear side by side)
    col1, col2, col3 = st.columns(3)
    
    # Put the first button in the first column
    with col1:
        # Button is disabled (grayed out) if no files are uploaded
        if st.button("Process Uploaded Files", disabled=not uploaded_files):
            process_uploaded_files(uploaded_files)  # Call function to handle the files
    
    # Put the second button in the second column
    with col2:
        # Button is disabled if no directory path is entered
        if st.button("Load from Directory", disabled=not directory_path):
            process_directory(directory_path)  # Call function to handle directory
    
    # Put the third button in the third column
    with col3:
        # This button is always enabled - it clears all stored documents
        if st.button("Clear Vector Store"):
            clear_vector_store()  # Call function to delete all documents
```

**What it does in detail**:
1. **Creates file uploader widget**: Allows users to select PDF, TXT, or DOCX files
2. **Creates directory input**: Lets users specify a folder path instead of individual files
3. **Creates action buttons**: 
   - "Process Uploaded Files": Processes the files users selected
   - "Load from Directory": Processes all files in a specified folder
   - "Clear Vector Store": Deletes all stored documents to start fresh

**UI Components explained**:
- **file_uploader**: A Streamlit widget that creates a "Choose Files" button
- **text_input**: Creates a text box where users can type
- **columns**: Divides the screen into sections for better layout
- **button**: Creates clickable buttons that trigger actions

### Function: `process_uploaded_files(uploaded_files)`

**Purpose**: Takes files uploaded by the user and adds them to our document database.

**Source Code:**
```python
def process_uploaded_files(uploaded_files):
    # First, make sure our vector store (database) is ready
    if not setup_vector_store():
        return  # Stop if database setup failed
    
    try:
        # Create a temporary folder to store uploaded files
        temp_dir = Path("./temp_uploads")  # Path object for easier file handling
        temp_dir.mkdir(exist_ok=True)      # Create folder if it doesn't exist
        
        # List to keep track of all temporary file paths
        temp_file_paths = []
        
        # Process each uploaded file one by one
        for uploaded_file in uploaded_files:
            # Create a path for this file in our temporary folder
            temp_file_path = temp_dir / uploaded_file.name  # Combine folder + filename
            
            # Write the uploaded file to disk so we can process it
            with open(temp_file_path, "wb") as f:  # Open in binary write mode
                f.write(uploaded_file.getbuffer())  # Get file content and write it
            
            # Add this file path to our list
            temp_file_paths.append(str(temp_file_path))
        
        # Create a document loader to process the files
        loader = DocumentLoader()
        
        # Show a spinning indicator while processing (this might take a while)
        with st.spinner("Processing documents..."):
            # Load and process all the files into document chunks
            documents = loader.load_multiple_files(temp_file_paths)
            
            # Check if we successfully processed any documents
            if documents:
                # Add all the document chunks to our vector database
                doc_ids = st.session_state.vector_store_manager.add_documents(documents)
                
                # Show success message with details
                st.success(f"Successfully processed {len(documents)} document chunks from {len(uploaded_files)} files")
                
                # Remember that we now have documents loaded
                st.session_state.documents_loaded = True
                
                # Clean up: delete all temporary files (we don't need them anymore)
                for temp_file_path in temp_file_paths:
                    Path(temp_file_path).unlink(missing_ok=True)  # Delete file, ignore if already gone
                
                # Remove the temporary directory (it should be empty now)
                temp_dir.rmdir()
            else:
                # No documents could be processed
                st.error("No documents could be processed")
                
    except Exception as e:
        # If anything goes wrong, show error messages
        st.error(f"Error processing files: {str(e)}")
        logger.error(f"Error processing uploaded files: {str(e)}")
```

**What it does step by step**:
1. **Creates temporary storage**: Makes a folder to temporarily store uploaded files
2. **Saves uploaded files**: Writes the uploaded files to disk so they can be processed
3. **Initializes document processor**: Creates a DocumentLoader to handle the files
4. **Processes documents**: Converts files into chunks that can be stored in the database
5. **Stores in database**: Adds processed documents to the vector store
6. **Cleans up**: Deletes temporary files to save disk space
7. **Shows results**: Displays success/error messages to the user

**Key concepts**:
- **Temporary files**: Files stored briefly during processing, then deleted
- **Document chunks**: Large documents are split into smaller pieces for better searching
- **Error handling**: Using try/except to handle problems gracefully
- **User feedback**: Showing progress and results to keep users informed

### Function: `process_directory(directory_path)`

**Purpose**: Processes all supported documents in a specified folder.

**Source Code:**
```python
def process_directory(directory_path):
    # Make sure our vector store (database) is ready
    if not setup_vector_store():
        return  # Stop if database setup failed
    
    try:
        # Create a document loader to process files
        loader = DocumentLoader()
        
        # Show a spinning indicator while we search and process files
        with st.spinner("Loading documents from directory..."):
            # Load all supported documents from the specified directory
            documents = loader.load_directory(directory_path)
            
            # Check if we found and processed any documents
            if documents:
                # Add all the document chunks to our vector database
                doc_ids = st.session_state.vector_store_manager.add_documents(documents)
                
                # Show success message
                st.success(f"Successfully processed {len(documents)} document chunks from directory")
                
                # Remember that we now have documents loaded
                st.session_state.documents_loaded = True
            else:
                # No supported documents were found in the directory
                st.error("No supported documents found in directory")
                
    except Exception as e:
        # If anything goes wrong, show error messages
        st.error(f"Error processing directory: {str(e)}")
        logger.error(f"Error processing directory: {str(e)}")
```

**What it does**:
1. **Validates path**: Checks that the specified directory exists
2. **Finds documents**: Looks for all PDF, TXT, and DOCX files in the folder
3. **Processes all files**: Uses DocumentLoader to process each file found
4. **Stores results**: Adds all processed documents to the vector store
5. **Reports results**: Shows how many documents were processed

**When to use**: This is the perfect tool when you have a folder full of documents (e.g., a project's documentation, a collection of reports) and want to add them all to the knowledge base in one go without selecting each file manually.

### Function: `clear_vector_store()`

**Purpose**: Deletes all stored documents to start fresh.

**Source Code:**
```python
def clear_vector_store():
    # Check if we actually have a vector store to clear
    if st.session_state.vector_store_manager is not None:
        try:
            # Delete all documents from the database
            st.session_state.vector_store_manager.delete_collection()
            
            # Update our app's memory to reflect that no documents are loaded
            st.session_state.documents_loaded = False
            
            # Reset the QA system since we no longer have documents
            st.session_state.qa_chain_manager = None
            
            # Tell the user that everything was cleared successfully
            st.success("Vector store cleared successfully")
            
        except Exception as e:
            # If something goes wrong during deletion, show an error
            st.error(f"Error clearing vector store: {str(e)}")
```

**What it does**:
1. **Checks if database exists**: Makes sure there's actually something to delete
2. **Deletes collection**: Removes all documents from the database
3. **Resets flags**: Updates the app's memory to reflect that no documents are loaded
4. **Clears QA system**: Resets the question-answering system
5. **Confirms action**: Shows success message to user

**When to use**: When you want to start over with different documents.

### Function: `qa_chat_section()`

**Purpose**: Creates the interface where users can ask questions about their documents.

**Source Code:**
```python
def qa_chat_section():
    # Add a header for the chat section
    st.header("💬 Ask Questions")
    
    # Check if API key is configured before allowing questions
    if not st.session_state.get('api_key_configured', False):
        st.warning("⚠️ Please configure your OpenAI API key in the sidebar first.")
        return
    
    # Check if documents have been loaded
    if not st.session_state.documents_loaded:
        st.warning("Please upload and process documents first before asking questions.")
        return
    
    # Ensure the QA system is ready
    if not setup_qa_chain():
        st.error("Failed to initialize QA system. Please check your configuration.")
        return
    
    # Create a text input for the user's question
    question = st.text_input(
        "Ask a question about your documents:",
        placeholder="Enter your question here...",
        key="question_input"  # Unique key for this widget
    )
    
    # Create columns for the buttons
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Create the "Ask" button, disabled if there's no question
        ask_button = st.button("Ask Question", disabled=not question.strip())
        
    with col2:
        # Create the "Clear History" button
        if st.button("Clear Chat History"):
            st.session_state.qa_chain_manager.clear_history()
            st.session_state.conversation_history = []
            st.success("Chat history cleared")
            
    # If the "Ask" button is clicked and there's a question
    if ask_button and question.strip():
        process_question(question)
        
    # Always display the conversation history
    display_conversation_history()
```

**What it does**:
- Creates the header for the chat section
- Checks if the API key is configured, shows warning if not
- Checks if documents are loaded, shows warning if not
- Sets up the QA chain if not already done
- Creates the text input for the user's question
- Creates the "Ask Question" and "Clear Chat History" buttons
- Processes the question and updates the conversation history

### Function: `process_question(question: str)`

**Purpose**: Takes a user's question and generates an answer using the stored documents.

**Source Code:**
```python
def process_question(question: str):
    try:
        # Show a spinner while the AI is thinking
        with st.spinner("Generating answer..."):
            # Send the question to the QA system
            response = st.session_state.qa_chain_manager.ask_question(question)
            
            # If the response was successful
            if response.get('success', False):
                # Add the new conversation to our history
                st.session_state.conversation_history.append(response)
                # Display the response immediately
                display_qa_response(response)
            else:
                # Show an error if something went wrong
                st.error(f"Error: {response.get('error', 'Unknown error')}")
                
    except Exception as e:
        # Handle any unexpected errors
        st.error(f"Error processing question: {str(e)}")
        logger.error(f"Error processing question: {str(e)}")
```

**What it does step by step**:
1. **Validates input**: Checks that the question isn't empty
2. **Shows progress**: Displays "Generating answer..." to keep user informed
3. **Calls QA system**: Sends question to the QAChainManager for processing
4. **Gets response**: Receives answer along with source documents
5. **Stores in history**: Saves the question and answer for display
6. **Shows results**: Displays the answer and source documents to user
7. **Handles errors**: Shows error messages if something goes wrong

**Key process**:
Question → Document Search → AI Processing → Answer + Sources → Display

### Function: `display_qa_response(response: Dict[str, Any])`

**Purpose**: Shows the AI's answer and the documents it used to create that answer.

**Source Code:**
```python
def display_qa_response(response: Dict[str, Any]):
    # Display the main answer subheader
    st.subheader("Answer:")
    st.write(response['answer'])
    
    # Check if there are any source documents to display
    if response.get('source_documents'):
        # Create an expandable section for the sources
        with st.expander(f"📚 Source Documents ({len(response['source_documents'])})"):
            # Loop through each source document
            for i, source in enumerate(response['source_documents'], 1):
                st.write(f"**Source {i}:**")
                st.write(source['content'])  # Display the text content of the source
                
                # Check for and display metadata
                if source.get('metadata'):
                    metadata = source['metadata']
                    if 'file_name' in metadata:
                        st.write(f"*File: {metadata['file_name']}*")
                        
                # Add a divider between sources for clarity
                if i < len(response['source_documents']):
                    st.divider()
```

**What it displays**:
1. **Main answer**: The AI-generated response to the user's question
2. **Source documents**: Expandable section showing which document chunks were used
3. **Metadata**: Information about each source (like filename)

**Why show sources**: This helps users verify the answer and understand where the information came from.

### Function: `display_conversation_history()`

**Purpose**: Shows all previous questions and answers in the current session.

**Source Code:**
```python
def display_conversation_history():
    # Only show the history section if there's something in it
    if st.session_state.conversation_history:
        st.subheader("📝 Conversation History")
        
        # Loop through the history in reverse to show the newest first
        for i, entry in enumerate(reversed(st.session_state.conversation_history)):
            # Use an expander for each conversation pair
            with st.expander(f"Q: {entry['question'][:60]}..." if len(entry['question']) > 60 else f"Q: {entry['question']}"):
                st.write("**Question:**")
                st.write(entry['question'])
                st.write("**Answer:**")
                st.write(entry['answer'])
                st.write(f"*{entry.get('source_count', 0)} sources used*")
```

**What it does**:
- Checks for history: Only displays if there are previous conversations
- Shows recent first: Displays newest conversations at the top
- Expandable format: Each conversation can be expanded to see full details
- Includes metadata: Shows how many source documents were used

### Function: `sidebar_info()`

**Purpose**: Shows system information in the side panel of the web interface.

**Source Code:**
```python
def sidebar_info():
    # Use a 'with' block to add items to the sidebar
    with st.sidebar:
        st.header("ℹ️ System Info")
        
        # Display vector store information if it's initialized
        if st.session_state.vector_store_manager is not None:
            try:
                info = st.session_state.vector_store_manager.get_collection_info()
                st.write("**Vector Store:**")
                st.write(f"Documents: {info.get('document_count', 'Unknown')}")
                st.write(f"Collection: {info.get('collection_name', 'Unknown')}")
            except Exception as e:
                st.write(f"Vector store error: {str(e)}")
                
        # Display chat memory information if it's initialized
        if st.session_state.qa_chain_manager is not None:
            try:
                memory_info = st.session_state.qa_chain_manager.get_memory_summary()
                st.write("**Chat Memory:**")
                st.write(f"Conversations: {memory_info.get('total_conversations', 0)}")
                st.write(f"Memory window: {memory_info.get('memory_window', 0)}")
            except Exception as e:
                st.write(f"Memory error: {str(e)}")
                
        # Display the static configuration of the AI model
        st.write("**Configuration:**")
        st.write(f"Model: gpt-3.5-turbo")
        st.write(f"Temperature: 0.1")
        st.write(f"Max tokens: 1000")
```

**What it displays**:
1. **Vector store info**: How many documents are stored, collection name
2. **Chat memory info**: How many conversations are remembered
3. **Configuration**: Current AI model settings (temperature, max tokens, etc.)

**Source Code:**
```python
def configure_api_key():
    # Create a section in the sidebar for API key configuration
    st.sidebar.header("🔑 API Configuration")
    
    # Check if there's an API key in the environment variables
    env_api_key = os.getenv('OPENAI_API_KEY')
    
    # If we found an environment API key and user doesn't want to override it
    if env_api_key and not st.sidebar.checkbox("Use different API key"):
        # Show that we found an API key in the environment
        st.sidebar.success("✅ API key found in environment")
        # Set the environment variable (in case it wasn't already set)
        os.environ['OPENAI_API_KEY'] = env_api_key
        # Remember that API key is configured
        st.session_state.api_key_configured = True
        return True  # API key is ready to use
    
    # Create a password input field for the API key (hides the text)
    api_key = st.sidebar.text_input(
        "Enter your OpenAI API Key:",
        type="password",  # This hides the text as user types
        help="Get your API key from https://platform.openai.com/api-keys"
    )
    
    # Check if user entered an API key
    if api_key:
        # Validate the API key format (should start with 'sk-' and be reasonably long)
        if api_key.startswith('sk-') and len(api_key) > 20:
            # Set the API key in environment so OpenAI library can use it
            os.environ['OPENAI_API_KEY'] = api_key
            # Remember that API key is configured
            st.session_state.api_key_configured = True
            # Show success message
            st.sidebar.success("✅ API key configured!")
            return True  # API key is valid and ready
        else:
            # API key format looks wrong
            st.sidebar.error("❌ Invalid API key format. Should start with 'sk-'")
            return False  # API key is not valid
    else:
        # No API key entered and none found in environment
        if not env_api_key:
            # Show warning and help information
            st.sidebar.warning("⚠️ Please enter your OpenAI API key to continue")
            st.sidebar.info("You can find your API key at: https://platform.openai.com/api-keys")
        return False  # No API key available
```

**Source Code:**
```python
def main():
    # Configure the Streamlit page settings (this must be first)
    st.set_page_config(
        page_title="QA RAG Chatbot",  # Title shown in browser tab
        page_icon="🤖",               # Icon shown in browser tab
        layout="wide"                 # Use full width of browser window
    )
    
    # Set up the app's memory system
    initialize_session_state()
    
    # Create the main title and description
    st.title("🤖 QA RAG Chatbot")
    st.write("Upload documents and ask questions about their content using AI-powered retrieval.")
    
    # Check if user has configured their API key
    api_key_configured = configure_api_key()
    
    # Only show the main interface if API key is configured
    if not api_key_configured:
        # Show a message telling user to configure API key first
        st.info("👆 Please configure your OpenAI API key in the sidebar to continue.")
    else:
        # API key is ready, show the main interface
        # Create two tabs to organize the interface
        tab1, tab2 = st.tabs(["📄 Documents", "💬 Chat"])
        
        # First tab: Document management
        with tab1:
            document_upload_section()  # Show file upload and processing interface
        
        # Second tab: Question and answer chat
        with tab2:
            qa_chat_section()  # Show chat interface for asking questions
    
    # Always show the sidebar with system information
    sidebar_info()

# This is the entry point - where the program starts when you run it
if __name__ == "__main__":
    main()  # Start the application
```

**What it does**:
1. **Configures page**: Sets title, icon, and layout for the web page
2. **Initializes session**: Sets up the app's memory
3. **Checks API key**: Ensures OpenAI API key is configured
4. **Creates tabs**: Organizes interface into "Documents" and "Chat" sections
5. **Loads sidebar**: Displays system information
6. **Starts app**: Begins the Streamlit web server

---

## src/document_loader.py - Document Processing

This file handles loading and processing different types of documents (PDF, TXT, DOCX) and preparing them for storage in the vector database.

### Class: `DocumentLoader`

**Purpose**: A class that knows how to read different types of documents and prepare them for the AI system.

**What is a class?**: Think of a class like a blueprint for creating objects. Like a blueprint for a car that defines what cars should have (wheels, engine, etc.), this class defines what a document loader should be able to do.

### Method: `__init__(self, chunk_size: int = 1000, chunk_overlap: int = 200)`

**Purpose**: This is the "constructor" - it sets up a new DocumentLoader when you create one.

**Source Code:**
```python
def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
    # Store the settings for how to split documents
    self.chunk_size = chunk_size        # How many characters per chunk (default: 1000)
    self.chunk_overlap = chunk_overlap  # How many characters overlap between chunks (default: 200)
    
    # Create a text splitter that intelligently breaks documents into chunks
    self.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,              # Maximum characters per chunk
        chunk_overlap=chunk_overlap,        # Characters to overlap between chunks
        length_function=len,                # Function to measure text length
        separators=["\n\n", "\n", " ", ""]  # Try to split on paragraphs, then lines, then words
    )
    
    # Define which file types we can process
    self.supported_extensions = {'.pdf', '.txt', '.docx', '.doc'}
```

**Parameters explained**:
- **chunk_size (1000)**: How many characters to put in each chunk
- **chunk_overlap (200)**: How many characters should overlap between chunks

**Why chunk documents?**:
- Large documents are too big for AI to process all at once
- Chunking breaks them into manageable pieces
- Overlap ensures we don't lose important information at chunk boundaries

**What it sets up**:
1. **Text splitter**: Tool that intelligently breaks documents into chunks
2. **Supported extensions**: List of file types we can process (.pdf, .txt, .docx, .doc)

**Beginner analogy**: Like preparing a large book by dividing it into chapters, but making sure each chapter includes a little bit from the previous chapter so nothing important is lost.

### Method: `load_single_document(self, file_path: str) -> List[Document]`

**Purpose**: Loads one document file and converts it into chunks ready for the database.

**Source Code:**
```python
def load_single_document(self, file_path: str) -> List[Document]:
    # Convert string path to Path object for easier handling
    file_path = Path(file_path)
    
    # Check if the file actually exists
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []  # Return empty list if file doesn't exist
    
    # Get the file extension (like .pdf, .txt, etc.)
    file_extension = file_path.suffix.lower()  # .lower() makes it case-insensitive
    
    # Check if we support this file type
    if file_extension not in self.supported_extensions:
        logger.warning(f"Unsupported file type: {file_extension}")
        return []  # Return empty list for unsupported files
    
    try:
        # Choose the right loader based on file type
        if file_extension == '.pdf':
            loader = PyPDFLoader(str(file_path))        # For PDF files
        elif file_extension == '.txt':
            loader = TextLoader(str(file_path), encoding='utf-8')  # For text files
        elif file_extension in ['.docx', '.doc']:
            loader = Docx2txtLoader(str(file_path))     # For Word documents
        else:
            logger.error(f"No loader available for {file_extension}")
            return []
        
        # Load the actual content from the file
        documents = loader.load()  # This reads the file and extracts text
        
        # Add metadata (information about the file) to each document
        for doc in documents:
            doc.metadata.update({
                'source_file': str(file_path),    # Full path to the original file
                'file_name': file_path.name,      # Just the filename
                'file_type': file_extension       # The file extension
            })
        
        # Split the documents into smaller chunks for better processing
        chunks = self.text_splitter.split_documents(documents)
        
        # Log how many chunks we created
        logger.info(f"Loaded {len(chunks)} chunks from {file_path.name}")
        
        return chunks  # Return the list of document chunks
        
    except Exception as e:
        # If anything goes wrong, log the error and return empty list
        logger.error(f"Error loading {file_path}: {str(e)}")
        return []
```

**What it does step by step**:
1. **Validates file**: Checks if file exists and is a supported type
2. **Chooses loader**: Picks the right tool based on file extension:
   - PDF files → PyPDFLoader
   - Text files → TextLoader  
   - Word files → Docx2txtLoader
3. **Loads content**: Reads the actual text from the file
4. **Adds metadata**: Attaches information like filename and file type
5. **Splits into chunks**: Breaks the document into smaller, manageable pieces
6. **Returns chunks**: Gives back a list of Document objects, each containing a chunk of text plus metadata

**Error handling**: If anything goes wrong (file not found, corrupted file, etc.), it logs the error and returns an empty list instead of crashing.

### Method: `load_directory(self, directory_path: str) -> List[Document]`

**Purpose**: Processes all supported documents in a specified folder.

**Source Code:**
```python
def load_directory(self, directory_path: str) -> List[Document]:
    # Convert string path to Path object for easier handling
    directory_path = Path(directory_path)
    
    # Check if the path exists and is actually a directory (folder)
    if not directory_path.exists() or not directory_path.is_dir():
        logger.error(f"Directory not found: {directory_path}")
        return []  # Return empty list if directory doesn't exist
    
    # List to collect all document chunks from all files
    all_chunks = []
    
    # Search through the directory and all subdirectories
    for file_path in directory_path.rglob('*'):  # rglob('*') finds all files recursively
        # Check if this is a file (not a folder) and has a supported extension
        if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
            # Process this file and get its chunks
            chunks = self.load_single_document(str(file_path))
            # Add all chunks from this file to our main list
            all_chunks.extend(chunks)  # extend() adds all items from chunks to all_chunks
    
    # Log the total number of chunks we processed
    logger.info(f"Loaded {len(all_chunks)} total chunks from {directory_path}")
    
    return all_chunks  # Return all chunks from all files
```

**What it does**:
1. **Validates directory**: Checks that the path exists and is actually a folder
2. **Finds all files**: Searches through the directory and all subdirectories
3. **Filters by type**: Only processes files with supported extensions
4. **Processes each file**: Calls `load_single_document` for each valid file
5. **Combines results**: Merges all chunks from all files into one big list
6. **Reports progress**: Logs how many chunks were created

**Recursive search**: Uses `rglob('*')` which means it looks in the main folder AND all folders inside it.

**When to use**: This is the perfect tool when you have a folder full of documents (e.g., a project's documentation, a collection of reports) and want to add them all to the knowledge base in one go without selecting each file manually.

### Method: `load_multiple_files(self, file_paths: List[str]) -> List[Document]`

**Purpose**: Processes multiple specific files (when you know exactly which files you want).

**Source Code:**
```python
def load_multiple_files(self, file_paths: List[str]) -> List[Document]:
    # List to collect all document chunks from all files
    all_chunks = []
    
    # Process each file path in the list
    for file_path in file_paths:
        # Load and process this single file
        chunks = self.load_single_document(file_path)
        # Add all chunks from this file to our main list
        all_chunks.extend(chunks)  # extend() adds all items from chunks to all_chunks
    
    return all_chunks  # Return combined chunks from all files
```

**What it does**:
1. **Takes a list of file paths**: Each string in the list should be a path to a file
2. **Processes each file**: Calls `load_single_document` for each path
3. **Combines results**: Merges all chunks into one list
4. **Returns everything**: Gives back all chunks from all files

**When to use**: When you want to process specific files, not everything in a folder.

---

## src/vector_store_manager.py - Vector Database

This file manages the ChromaDB vector database where we store document chunks as mathematical vectors for fast searching.

### What is a Vector Database?

**Simple explanation**: Imagine if you could turn every piece of text into a unique set of numbers (a vector) that represents its meaning. Similar texts would have similar numbers. A vector database stores these numbers and can quickly find texts with similar meanings.

**Beginner analogy**: Think of it like a magical librarian. Instead of organizing books by title, this librarian reads every book and organizes them by topic and meaning in a giant, multi-dimensional room. When you ask a question, the librarian instantly knows which corner of the room has the most relevant books, even if they don't use the exact same words as your question.

**Why use vectors**: When you ask "What is machine learning?", the database can find chunks about "ML", "artificial intelligence", "neural networks" etc., even if they don't contain the exact words you used.

### Class: `VectorStoreManager`

**Purpose**: Manages all operations related to storing and searching document vectors.

### Method: `__init__(...)`

**Purpose**: Sets up the vector database manager.

**Parameters explained**:
- **persist_directory**: Where to save the database on disk (like choosing a folder for your files)
- **collection_name**: Name for this group of documents (like naming a folder)
- **embedding_model**: Which AI model to use for converting text to vectors

**Source Code:**
```python
def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "qa_documents", embedding_model: str = "text-embedding-ada-002"):
    # Store configuration settings
    self.persist_directory = Path(persist_directory)  # Where to save the database
    self.collection_name = collection_name           # Name for this group of documents
    self.embedding_model = embedding_model           # Which AI model to use for embeddings
    
    # Create the embeddings object that converts text to vectors
    self.embeddings = OpenAIEmbeddings(model=embedding_model, show_progress_bar=True)
    
    # Initialize as None - will be set up in _initialize_vector_store()
    self.vector_store: Optional[Chroma] = None
    
    # Set up the vector store (database)
    self._initialize_vector_store()
```

**What it does**:
1. **Saves settings**: Stores all the configuration parameters
2. **Sets up embeddings**: Creates the OpenAI tool that converts text to vectors
3. **Initializes database**: Sets up or loads the ChromaDB database

**Embeddings explained**: These are AI models that read text and convert it into lists of numbers that capture the meaning. Similar texts get similar numbers.

### Method: `_initialize_vector_store(self)`

**Purpose**: Sets up the actual database, either by creating a new one or loading an existing one.

**The underscore prefix**: Methods starting with `_` are "private" - they're meant to be used only inside this class, not called from outside.

**Source Code:**
```python
def _initialize_vector_store(self):
    try:
        # Create the directory for storing the database if it doesn't exist
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Check if we already have a database saved on disk
        if self._vector_store_exists():
            logger.info(f"Loading existing vector store from {self.persist_directory}")
            # Load the existing database
            self.vector_store = Chroma(
                collection_name=self.collection_name,        # Name of our document collection
                embedding_function=self.embeddings,          # How to convert text to vectors
                persist_directory=str(self.persist_directory) # Where the database is saved
            )
        else:
            logger.info(f"Creating new vector store at {self.persist_directory}")
            # Create a new database
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
    except Exception as e:
        logger.error(f"Error initializing vector store: {str(e)}")
        raise  # Re-raise the error so the caller knows something went wrong
```

**What it does**:
1. **Creates directory**: Makes sure the storage folder exists
2. **Checks for existing database**: Looks for previous database files
3. **Loads or creates**: Either loads existing data or creates fresh database
4. **Handles errors**: If something goes wrong, it logs the error and stops

**Persistence explained**: The database saves to disk so your documents stay even after you close the program.

### Method: `_vector_store_exists(self) -> bool`

**Purpose**: Checks if a database already exists in the specified location.

**Source Code:**
```python
def _vector_store_exists(self) -> bool:
    # Check if the main database file exists
    chroma_db_path = self.persist_directory / "chroma.sqlite3"
    return chroma_db_path.exists()  # Returns True if file exists, False otherwise
```

**What it does**: Looks for the `chroma.sqlite3` file, which is ChromaDB's main database file.

**Returns**: True if database exists, False if starting fresh.

### Method: `add_documents(self, documents: List[Document]) -> List[str]`

**Purpose**: Adds new document chunks to the vector database.

**Source Code:**
```python
def add_documents(self, documents: List[Document]) -> List[str]:
    # Check if we actually have documents to add
    if not documents:
        logger.warning("No documents provided to add")
        return []  # Return empty list if no documents
    
    try:
        logger.info(f"Adding {len(documents)} documents to vector store")
        
        # Add documents to the vector store (this converts text to vectors and stores them)
        doc_ids = self.vector_store.add_documents(documents)
        
        logger.info(f"Successfully added {len(doc_ids)} documents")
        return doc_ids  # Return the unique IDs assigned to each document
        
    except Exception as e:
        logger.error(f"Error adding documents to vector store: {str(e)}")
        raise  # Re-raise the error
```

**What happens step by step**:
1. **Validates input**: Checks that we actually have documents to add
2. **Converts to vectors**: Uses OpenAI's embedding model to turn text into vectors
3. **Stores in database**: Saves both the text and its vector representation
4. **Returns IDs**: Gives back unique identifiers for each stored document

**The embedding process**: Each chunk of text gets sent to OpenAI's API, which returns a list of ~1500 numbers that represent the meaning of that text.

**Document IDs**: Each stored chunk gets a unique ID so it can be found later.

### Method: `similarity_search(...)`

**Purpose**: Finds document chunks that are most similar to a given question or query.

**Source Code:**
```python
def similarity_search(self, query: str, k: int = 4, filter_criteria: Optional[Dict[str, Any]] = None) -> List[Document]:
    # Check if the vector store is ready
    if not self.vector_store:
        logger.error("Vector store not initialized")
        return []  # Return empty list if database isn't ready
    
    try:
        # Search for documents similar to the query
        if filter_criteria:
            # Search with filters (e.g., only certain file types)
            results = self.vector_store.similarity_search(query=query, k=k, filter=filter_criteria)
        else:
            # Search without filters (all documents)
            results = self.vector_store.similarity_search(query=query, k=k)
        
        logger.info(f"Found {len(results)} similar documents for query")
        return results  # Return the most similar documents
        
    except Exception as e:
        logger.error(f"Error performing similarity search: {str(e)}")
        return []  # Return empty list if search fails
```

**How similarity search works**:
1. **Convert query to vector**: Turn the user's question into the same type of numbers used for documents
2. **Calculate distances**: Mathematically compare the query vector to all stored document vectors
3. **Find closest matches**: Identify the chunks with the most similar vectors
4. **Return results**: Give back the actual text chunks, not just the vectors

**Parameters**:
- **query**: The user's question or search term
- **k**: How many similar chunks to return (default 4)
- **filter_criteria**: Optional filters (like "only PDFs" or "only from specific file")

**Mathematical concept**: Uses cosine similarity or similar metrics to measure how "close" vectors are in high-dimensional space.

### Method: `similarity_search_with_score(...)`

**Purpose**: Same as similarity_search, but also returns numerical scores showing how similar each result is.

**Source Code:**
```python
def similarity_search_with_score(self, query: str, k: int = 4, filter_criteria: Optional[Dict[str, Any]] = None) -> List[tuple]:
    # Same as similarity_search but also returns confidence scores
    if not self.vector_store:
        logger.error("Vector store not initialized")
        return []
    
    try:
        if filter_criteria:
            results = self.vector_store.similarity_search_with_score(query=query, k=k, filter=filter_criteria)
        else:
            results = self.vector_store.similarity_search_with_score(query=query, k=k)
        
        logger.info(f"Found {len(results)} similar documents with scores")
        return results  # Returns list of (document, score) tuples
        
    except Exception as e:
        logger.error(f"Error performing similarity search with scores: {str(e)}")
        return []
```

**Scores explained**: Lower scores mean more similar. A score of 0.0 would be identical, 1.0 would be completely different.

**Why useful**: Helps you understand how confident the system is about each result.

### Method: `get_collection_info(self) -> Dict[str, Any]`

**Purpose**: Gets statistics and information about the current database.

**Source Code:**
```python
def get_collection_info(self) -> Dict[str, Any]:
    # Get information about the current database
    if not self.vector_store:
        return {"error": "Vector store not initialized"}
    
    try:
        # Access the underlying collection to get statistics
        collection = self.vector_store._collection
        return {
            "collection_name": self.collection_name,
            "document_count": collection.count(),  # How many documents are stored
            "persist_directory": str(self.persist_directory)
        }
    except Exception as e:
        logger.error(f"Error getting collection info: {str(e)}")
        return {"error": str(e)}
```

**What it returns**:
- Collection name
- Number of documents stored
- Storage directory location

**Use case**: For displaying system status in the UI or debugging.

### Method: `delete_collection(self)`

**Purpose**: Completely deletes all stored documents (like emptying the recycle bin).

**Source Code:**
```python
def delete_collection(self):
    # Delete all documents and reset the database
    try:
        if self.vector_store:
            # Delete all documents from the current collection
            self.vector_store.delete_collection()
            logger.info(f"Deleted collection: {self.collection_name}")
        
        # Re-initialize the vector store (creates a fresh, empty database)
        self._initialize_vector_store()
        
    except Exception as e:
        logger.error(f"Error deleting collection: {str(e)}")
        raise
```

**What it does**:
1. **Deletes all data**: Removes all document chunks and their vectors
2. **Recreates database**: Sets up a fresh, empty database
3. **Logs action**: Records that the deletion happened

**Warning**: This is permanent! All stored documents will be lost.

### Method: `as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None)`

**Purpose**: Creates a "retriever" object that the QA system can use to search for documents.

**Source Code:**
```python
def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
    # Create a retriever object that other parts of the system can use
    if not self.vector_store:
        logger.error("Vector store not initialized")
        return None
    
    # Set default search parameters
    default_search_kwargs = {"k": 4}  # Return 4 documents by default
    
    # Update with any custom parameters provided
    if search_kwargs:
        default_search_kwargs.update(search_kwargs)
    
    # Return a retriever object that the QA system can use
    return self.vector_store.as_retriever(search_kwargs=default_search_kwargs)
```

**What's a retriever**: It's like a standardized search interface that the question-answering system knows how to use.

**Default settings**: Sets up the retriever to return 4 similar documents by default, but this can be customized.

---

## src/qa_chain_manager.py - Question Answering

This file is the "brain" of the chatbot. It takes a user's question, finds relevant documents, and uses an AI model to generate a human-like answer. It also manages the conversation history to provide context for follow-up questions.

### Class: `QAChainManager`
**Purpose**: Manages the entire question-answering process, from receiving a question to generating a final answer with sources.

### Method: `__init__(...)`
**Purpose**: Sets up the QA system with all its components.
**Source Code:**
```python
def __init__(
    self, 
    retriever: BaseRetriever,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 1000,
    memory_window: int = 10
):
    # Store the document retriever (search system)
    self.retriever = retriever
    
    # Set up the language model with specified parameters
    self.llm = ChatOpenAI(
        model_name=model_name,  # Which AI model to use
        temperature=temperature,  # How creative responses should be
        max_tokens=max_tokens     # Maximum response length
    )
    
    # Set up conversation memory to remember previous exchanges
    self.memory = ConversationSummaryBufferMemory(
        llm=self.llm,
        max_token_limit=memory_window * 100,  # Approximate memory size
        return_messages=True,    # Return as message objects
        memory_key="chat_history",  # Key name for accessing history
        output_key="answer"      # Key name for AI responses
    )
    
    # Create the complete QA chain
    self.qa_chain = self._create_qa_chain()
    
    # Store conversation history for UI display
    self.conversation_history = []
    
    logger.info(f"QAChainManager initialized with model: {model_name}")
```

**Parameters**:
- **retriever**: The document search engine from our vector store.
- **model_name**: The specific OpenAI model to use for generating answers (e.g., "gpt-3.5-turbo").
- **temperature**: Controls the creativity of the AI. `0.1` means very factual and focused.
- **max_tokens**: The maximum length of the AI's generated answer.
- **memory_window**: How many past question-answer pairs to remember for context.

### Method: `_create_qa_chain(self)`
**Purpose**: Builds the core `ConversationalRetrievalChain` from LangChain, which connects all the components (LLM, retriever, memory, prompt).
**Source Code:**
```python
def _create_qa_chain(self) -> ConversationalRetrievalChain:
    """Create the full conversational retrieval chain."""
    # Create our custom prompt template
    custom_prompt = self._create_custom_prompt()
    
    # Build the complete QA chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=self.llm,                    # The language model
        retriever=self.retriever,        # Document search system
        memory=self.memory,              # Conversation memory
        return_source_documents=True,    # Include source docs in response
        combine_docs_chain_kwargs={      # Custom prompt configuration
            "prompt": custom_prompt
        },
        verbose=True,                    # Enable detailed logging
        chain_type="stuff"              # How to combine documents
    )
    
    return qa_chain
```

**What it does**:
- It assembles the final QA system by linking the language model, the document retriever, and the conversation memory.
- It uses a custom prompt to guide the AI's behavior.

### Method: `ask_question(self, question: str) -> Dict[str, Any]`
**Purpose**: The main public method to ask a question to the system. This is the primary entry point for the UI to interact with the QA manager.
**Source Code:**
```python
def ask_question(self, question: str) -> Dict[str, Any]:
    """Ask a question and get a structured response."""
    # Validate the input
    if not question.strip():
        return {
            "answer": "Please provide a valid question.",
            "source_documents": [],
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "success": False
        }
    
    try:
        logger.info(f"Processing question: {question}")
        
        # Send question through the QA chain
        response = self.qa_chain({
            "question": question,
            "chat_history": self.memory.chat_memory.messages
        })
        
        # Extract the answer and source documents
        answer = response.get("answer", "I couldn't generate an answer.")
        source_docs = response.get("source_documents", [])
        
        # Create response structure
        result = {
            "answer": answer,
            "source_documents": [
                {
                    "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in source_docs
            ],
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        # Store in conversation history for UI
        self.conversation_history.append(result)
        
        logger.info("Question processed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        error_result = {
            "answer": f"I encountered an error: {str(e)}",
            "source_documents": [],
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "success": False
        }
        self.conversation_history.append(error_result)
        return error_result
```

**What it returns**:
A dictionary containing:
- `question`: The original question asked.
- `answer`: The AI-generated answer.
- `source_documents`: A list of document chunks used to generate the answer.
- `success`: A boolean indicating if the operation was successful.

### Method: `_extract_source_documents(...)`
**Purpose**: A helper function to format the source documents into a clean, readable format for the final output.
**Source Code:**
```python
def _extract_source_documents(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and format source documents from the chain's result."""
    # ... (source code as before) ...
```

### Method: `clear_history(self)`
**Purpose**: Clears the conversation memory.
**Source Code:**
```python
def clear_history(self):
    """Clear the conversation memory."""
    self.memory.clear()
    self.conversation_history = []
    logger.info("Conversation history cleared.")
```

### Method: `get_memory_summary(self) -> Dict[str, Any]`
**Purpose**: Provides statistics about the current state of the conversation memory.
**Source Code:**
```python
def get_memory_summary(self) -> Dict[str, Any]:
    """Get a summary of the conversation memory."""
    try:
        # Count the number of messages in chat history
        message_count = len(self.memory.chat_memory.messages)
        
        # Get the memory window size
        memory_window = getattr(self.memory, 'k', 10)
        
        return {
            "total_conversations": message_count // 2,  # Each conversation has 2 messages (human + AI)
            "memory_window": memory_window,
            "current_memory_size": message_count
        }
    except Exception as e:
        logger.error(f"Error getting memory summary: {str(e)}")
        return {
            "total_conversations": 0,
            "memory_window": 0,
            "current_memory_size": 0
        }
```

**What it returns**:
- `total_conversations`: The number of question-answer pairs currently in memory.
- `memory_window`: The maximum number of pairs the memory can hold.
- `current_memory_size`: The current number of messages stored.

---

## tests/test_setup.py - System Testing

This file contains a series of tests to ensure that all components of the QA RAG Chatbot are functioning correctly. It's an essential script for developers to verify the system's health after making changes.

### Purpose
The test script validates that:
- All required libraries can be imported
- Environment variables are properly configured
- Core components can be initialized
- The full QA pipeline works end-to-end

### Function: `test_imports()`
**Purpose**: Verifies that all necessary Python libraries and custom modules can be imported without errors. This is the first check to ensure the environment is set up correctly.

**Source Code:**
```python
def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        # Test core libraries
        import streamlit
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import langchain
        print("✓ LangChain imported successfully")
    except ImportError as e:
        print(f"✗ LangChain import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✓ ChromaDB imported successfully")
    except ImportError as e:
        print(f"✗ ChromaDB import failed: {e}")
        return False
    
    try:
        import openai
        print("✓ OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
    
    try:
        # Test custom modules
        from src.document_loader import DocumentLoader
        print("✓ DocumentLoader imported successfully")
    except ImportError as e:
        print(f"✗ DocumentLoader import failed: {e}")
        return False
    
    try:
        from src.vector_store_manager import VectorStoreManager
        print("✓ VectorStoreManager imported successfully")
    except ImportError as e:
        print(f"✗ VectorStoreManager import failed: {e}")
        return False
    
    try:
        from src.qa_chain_manager import QAChainManager
        print("✓ QAChainManager imported successfully")
    except ImportError as e:
        print(f"✗ QAChainManager import failed: {e}")
        return False
    
    return True
```

### Function: `test_environment()`
**Purpose**: Checks for essential environment configurations, primarily the OpenAI API key.

**Source Code:**
```python
def test_environment():
    """Test environment configuration."""
    print("\nTesting environment configuration...")
    
    # Check for OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and openai_key != 'your_openai_api_key_here':
        print("✓ OpenAI API key is configured")
    else:
        print("✗ OpenAI API key not found or not configured")
        print("  Please set OPENAI_API_KEY in your .env file")
        return False
    
    # Check other environment variables
    chroma_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
    print(f"✓ ChromaDB path: {chroma_path}")
    
    embeddings_model = os.getenv('EMBEDDINGS_MODEL', 'text-embedding-ada-002')
    print(f"✓ Embeddings model: {embeddings_model}")
    
    chat_model = os.getenv('CHAT_MODEL', 'gpt-3.5-turbo')
    print(f"✓ Chat model: {chat_model}")
    
    return True
```

### Function: `test_document_loader()`
**Purpose**: Tests the `DocumentLoader` class by creating a sample document, processing it, and verifying the output.

**Source Code:**
```python
def test_document_loader():
    """Test document loader functionality."""
    print("\nTesting Document Loader...")
    
    # Create a dummy document for testing
    test_content = "This is a test document for the QA RAG system."
    test_file_path = Path("test_document.txt")
    
    try:
        # Write test content to file
        with open(test_file_path, "w") as f:
            f.write(test_content)
            
        # Initialize the document loader
        loader = DocumentLoader()
        
        # Load the dummy document
        documents = loader.load_single_document(str(test_file_path))
        
        # Check if the document was loaded and processed
        if documents and len(documents) > 0:
            print(f"✓ DocumentLoader created {len(documents)} chunk(s)")
            
            # Verify content and metadata
            if test_content in documents[0].page_content:
                print("✓ Document content is correct")
            else:
                print("✗ Incorrect document content")
                return False
                
            if documents[0].metadata.get('file_name') == 'test_document.txt':
                print("✓ Document metadata is correct")
            else:
                print("✗ Incorrect document metadata")
                return False
        else:
            print("✗ DocumentLoader failed to create chunks")
            return False
            
    except Exception as e:
        print(f"✗ DocumentLoader test failed with error: {e}")
        return False
    finally:
        # Clean up the dummy file
        if test_file_path.exists():
            test_file_path.unlink()
        
    return True
```

### Function: `test_vector_store()`
**Purpose**: Tests the `VectorStoreManager` by adding a document, performing a similarity search, and then cleaning up. This verifies the entire lifecycle of a document in the vector database.

**Source Code:**
```python
def test_vector_store():
    """Test vector store functionality."""
    print("\nTesting Vector Store...")
    
    # Define a unique collection name for testing to avoid conflicts
    test_collection = "test_collection"
    test_db_path = "./test_chroma_db"
    
    try:
        # Initialize the vector store manager for the test collection
        vector_store = VectorStoreManager(
            persist_directory=test_db_path, 
            collection_name=test_collection
        )
        
        # Create a dummy document to add
        from langchain.schema import Document
        test_doc = Document(
            page_content="The sky is blue.", 
            metadata={"source": "test"}
        )
        
        # Add the document to the vector store
        vector_store.add_documents([test_doc])
        print("✓ Document added to vector store")
        
        # Perform a similarity search
        query = "What color is the sky?"
        results = vector_store.similarity_search(query, k=1)
        
        # Check if the search returned the correct document
        if results and results[0].page_content == "The sky is blue.":
            print("✓ Similarity search returned correct document")
        else:
            print("✗ Similarity search failed")
            return False
            
    except Exception as e:
        print(f"✗ VectorStore test failed with error: {e}")
        return False
    finally:
        # Clean up the test database
        try:
            vector_store.delete_collection()
            import shutil
            if Path(test_db_path).exists():
                shutil.rmtree(test_db_path)
            print("✓ Test vector store cleaned up")
        except Exception as e:
            print(f"✗ Warning: Failed to clean up test vector store: {e}")
            
    return True
```

### Function: `test_qa_chain()`
**Purpose**: Performs an end-to-end test of the question-answering system. It sets up a vector store, adds a document, and asks a question to verify that the `QAChainManager` can generate a correct answer based on the document.

**Source Code:**
```python
def test_qa_chain():
    """Test the full QA chain."""
    print("\nTesting QA Chain...")
    
    # Use a unique collection for testing
    test_collection = "test_qa_chain_collection"
    test_db_path = "./test_qa_db"
    
    try:
        # 1. Set up Vector Store
        vector_store_manager = VectorStoreManager(
            persist_directory=test_db_path, 
            collection_name=test_collection
        )
        
        # 2. Add a document
        from langchain.schema import Document
        qa_doc = Document(
            page_content="LangChain is a framework for developing applications powered by language models.", 
            metadata={"source": "test_qa"}
        )
        vector_store_manager.add_documents([qa_doc])
        print("✓ Document added for QA test")
        
        # 3. Set up QA Chain
        retriever = vector_store_manager.as_retriever()
        qa_chain = QAChainManager(retriever=retriever)
        print("✓ QA Chain Manager initialized")
        
        # 4. Ask a question
        question = "What is LangChain?"
        response = qa_chain.ask_question(question)
        
        # 5. Verify the response
        if response.get('success', False) and 'langchain' in response.get('answer', '').lower():
            print(f"✓ QA Chain returned a relevant answer: {response['answer']}")
        else:
            print(f"✗ QA Chain failed to provide a correct answer. Response: {response}")
            return False
            
    except Exception as e:
        print(f"✗ QA Chain test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up the test database
        try:
            vector_store_manager.delete_collection()
            import shutil
            if Path(test_db_path).exists():
                shutil.rmtree(test_db_path)
            print("✓ Test QA chain database cleaned up")
        except Exception as e:
            print(f"✗ Warning: Failed to clean up QA chain database: {e}")
            
    return True
```

---

## tests/debug_qa.py - Debugging Script

This is a simple, standalone script used for quickly diagnosing issues with the core components of the QA system, particularly the `QAChainManager` and its dependencies. It's not part of the main application but serves as a developer tool.

### Purpose
- To isolate and test the initialization of `ChatOpenAI`, `VectorStoreManager`, and `QAChainManager`
- To quickly verify that the necessary LangChain components can be imported and instantiated without errors
- To run a simple end-to-end test of the QA chain by asking a generic question

### When to Use
Run this script when you encounter issues with:
- QA chain initialization failures
- Import errors with LangChain components
- OpenAI API connectivity problems
- Vector store configuration issues

### Source Code
```python
"""
Quick test to identify the QA chain initialization issue
"""

import os
from dotenv import load_dotenv
load_dotenv()

print("Testing QA Chain Initialization...")
print(f"OpenAI API Key configured: {bool(os.getenv('OPENAI_API_KEY'))}")

try:
    # Test importing and initializing the core language model
    from langchain_openai import ChatOpenAI
    print("✓ ChatOpenAI import successful")
    
    # Test basic ChatOpenAI initialization
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.1,
        max_tokens=1000
    )
    print("✓ ChatOpenAI initialization successful")
    
except Exception as e:
    print(f"✗ ChatOpenAI error: {e}")

try:
    # Test importing other necessary LangChain components
    from langchain.chains import ConversationalRetrievalChain
    print("✓ ConversationalRetrievalChain import successful")
except Exception as e:
    print(f"✗ ConversationalRetrievalChain import error: {e}")

try:
    from langchain.memory import ConversationBufferWindowMemory
    print("✓ ConversationBufferWindowMemory import successful")
except Exception as e:
    print(f"✗ ConversationBufferWindowMemory import error: {e}")

try:
    # Test importing and initializing our custom vector store manager
    from src.vector_store_manager import VectorStoreManager
    print("✓ VectorStoreManager import successful")
    
    # Test vector store initialization
    vector_manager = VectorStoreManager()
    print("✓ VectorStoreManager initialization successful")
    
    # Test creating a retriever from the vector store
    retriever = vector_manager.as_retriever()
    print(f"✓ Retriever created: {type(retriever)}")
    
except Exception as e:
    print(f"✗ VectorStoreManager error: {e}")

# Test our main QA Chain Manager
try:
    from src.qa_chain_manager import QAChainManager
    print("✓ QAChainManager import successful")
    
    # Check if the retriever was created successfully before proceeding
    if 'retriever' in locals():
        qa_manager = QAChainManager(retriever=retriever)
        print("✓ QAChainManager initialization successful")
        
        # Ask a simple question to test the end-to-end chain
        response = qa_manager.ask_question("What is this document about?")
        print(f"✓ QA chain working: {response.get('success', False)}")
        if not response.get('success', False):
            print(f"   Error: {response.get('error', 'Unknown error')}")
    
except Exception as e:
    print(f"✗ QAChainManager error: {e}")
    import traceback
    print(f"   Full traceback: {traceback.format_exc()}")

print("\nTest completed. Check above for any ✗ errors.")
```

---

## How to Run Tests

### Running the Main Test Suite
To run the comprehensive test suite, execute the following command in your terminal:

```bash
python tests/test_setup.py
```

The script will run through all tests and display results:
- ✓ indicates a successful test
- ✗ indicates a failed test with error details

### Running the Debug Script
If you encounter issues with the QA chain, run the debugging script:

```bash
python tests/debug_qa.py
```

This will help isolate which component is causing problems.

### Test Prerequisites
Before running tests, ensure:
1. **Environment Setup**: Your virtual environment is activated
2. **Dependencies**: All packages from `requirements.txt` are installed
3. **API Key**: OpenAI API key is configured in your `.env` file
4. **Clean Environment**: No conflicting ChromaDB instances are running

### Understanding Test Results
- **Import Tests**: Verify all required libraries are available
- **Environment Tests**: Check configuration settings
- **Component Tests**: Test individual system components
- **Integration Tests**: Verify the complete QA pipeline works

### Troubleshooting Failed Tests
If tests fail:
1. Check the specific error message
2. Verify your `.env` file configuration
3. Ensure all dependencies are installed correctly
4. Run the debug script to isolate the issue
5. Check for conflicting ChromaDB databases

---

**Documentation Complete**: This documentation now covers all components of the QA RAG Chatbot system, including the reorganized test structure with detailed explanations of each function and its purpose.
