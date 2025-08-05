# QA RAG Chatbot with LangChain and ChromaDB

A robust Question-Answering RAG (Retrieval-Augmented Generation) chatbot built with LangChain, ChromaDB, and Streamlit. Features advanced file handling, error recovery, and a clean user interface.

## ✨ Features

- **📄 Document Processing**: Load and process PDF, TXT, and DOCX files with robust error handling
- **🗃️ Vector Store**: ChromaDB for efficient document storage and retrieval
- **🤖 Advanced QA**: Conversational retrieval chain with context awareness
- **💬 Chat History**: Maintains conversation context across questions
- **🎨 Clean Interface**: Streamlined Streamlit interface with hidden developer tools
- **📚 Source Citations**: Shows which documents were used to generate answers
- **🔒 Secure File Handling**: Enhanced temporary file management with proper cleanup
- **⚡ Auto-Configuration**: Automatic environment detection and setup

## 🚀 Quick Start

### Option 1: Automated Setup (Windows)

```bash
# Run the setup script (installs dependencies and sets up environment)
.\setup.bat

# Start the application
.\run.bat
```

### Option 2: Manual Setup

#### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install requirements
pip install -r requirements.txt
```

#### 2. Environment Configuration

The application supports multiple ways to configure your OpenAI API key:

**Option A: Environment Variable**
```bash
set OPENAI_API_KEY=your_openai_api_key_here
```

**Option B: .env File**
Copy `.env.example` to `.env` and edit:
```bash
cp .env.example .env
```

**Option C: Streamlit Interface**
Enter your API key directly in the sidebar when running the app.

#### 3. Run the Application

```bash
streamlit run app.py
```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB recommended for large documents)
- **Storage**: 1GB free space for vector database
- **Internet**: Required for OpenAI API calls

## 💻 Usage

### 1. 📄 Upload Documents
- Navigate to the "Documents" tab
- **File Upload**: Drag and drop or select PDF, TXT, or DOCX files (supports multiple files)
- **Directory Upload**: Specify a directory path to load multiple files at once
- **Processing**: Documents are automatically chunked and stored in ChromaDB vector store
- **Cleanup**: Temporary files are automatically cleaned up with robust error handling

### 2. 💬 Ask Questions
- Switch to the "Chat" tab
- Enter questions about your uploaded documents
- The system provides contextual answers based on document content
- **Source Attribution**: View which documents were used for each answer
- **Follow-up**: Ask follow-up questions with maintained conversation context

### 3. 🔧 Manage System
- **Chat History**: View previous conversations and clear when needed
- **Vector Store**: Clear the document database to start fresh
- **System Info**: Monitor document count, memory usage, and configuration in the sidebar
- **API Configuration**: Manage OpenAI API key settings

## 🏗️ Architecture

### Core Components

1. **📄 DocumentLoader** (`src/document_loader.py`)
   - Handles loading PDF, TXT, and DOCX files with error recovery
   - Intelligent text splitting with optimal chunk sizes
   - Preserves metadata for source tracking and citations

2. **🗃️ VectorStoreManager** (`src/vector_store_manager.py`)
   - Manages ChromaDB vector store operations
   - Handles document indexing with OpenAI embeddings
   - Provides similarity search and retrieval capabilities
   - Persistent storage with automatic collection management

3. **🤖 QAChainManager** (`src/qa_chain_manager.py`)
   - Implements conversational retrieval chain with memory
   - Advanced prompt engineering for better responses
   - Manages chat history with configurable memory window
   - Context-aware follow-up question handling

4. **🎨 Streamlit App** (`app.py`)
   - Clean, functional web interface with hidden developer tools
   - Robust file upload with automatic cleanup
   - Real-time system monitoring and configuration
   - Enhanced error handling and user feedback

### 🔧 Technical Features

- **🔒 Secure File Handling**: System temp directory usage with fallback options
- **🧹 Automatic Cleanup**: Robust temporary file management with garbage collection
- **📊 Real-time Monitoring**: System info sidebar with live statistics
- **⚡ Performance Optimization**: Efficient memory usage and file handle management
- **🛡️ Error Recovery**: Comprehensive error handling with graceful degradation
- **🎯 Context Management**: Smart conversation history with memory windowing

## ⚙️ Configuration

### Model Settings
- **Chat Model**: `gpt-3.5-turbo` (configurable via environment)
- **Embeddings**: `text-embedding-ada-002` (OpenAI)
- **Temperature**: `0.1` (conservative, factual responses)
- **Max Tokens**: `1000` (response length limit)
- **Memory Window**: `10` conversation turns (configurable)

### Document Processing
- **Chunk Size**: `1000` characters (optimal for retrieval)
- **Chunk Overlap**: `200` characters (maintains context)
- **Supported Formats**: PDF, TXT, DOCX
- **Max File Size**: Limited by available memory
- **Batch Processing**: Multiple files supported

### File Handling
- **Temporary Storage**: System temp directory (with local fallback)
- **Cleanup Strategy**: Automatic with error recovery
- **Permissions**: Automatic permission testing
- **Security**: Isolated temporary directories with unique names

### UI Configuration
- **Theme**: Clean, minimal interface
- **Hidden Elements**: Streamlit developer tools and branding
- **Responsive**: Adapts to different screen sizes
- **Real-time Updates**: Live system monitoring

## 📁 File Structure

```
QA bot with LangChain and ST/
├── 📁 src/                    # Source code package
│   ├── __init__.py           # Package initialization
│   ├── document_loader.py    # Document loading and processing
│   ├── vector_store_manager.py # ChromaDB vector store management
│   ├── qa_chain_manager.py   # QA chain and conversation handling
│   └── test_setup.py         # Component-level tests
├── 📁 .streamlit/            # Streamlit configuration
│   └── config.toml           # UI and performance settings
├── 📁 chroma_db/             # Vector database storage (auto-created)
├── 📁 temp_uploads/          # Temporary file storage (auto-managed)
├── app.py                    # Main Streamlit web interface
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── setup.bat                # Windows automated setup script
├── run.bat                  # Windows application launcher
├── test_document.txt        # Sample document for testing
├── CODE_MAP.md              # Detailed code documentation
├── DOCUMENTATION.md         # Technical documentation
└── README.md                # This file
```

## 📊 Dependencies

### Core Framework
```
streamlit>=1.47.0          # Web interface
langchain>=0.1.0           # LLM application framework
langchain-community        # Community integrations
langchain-chroma          # ChromaDB integration
langchain-openai         # OpenAI integration
```

### Document Processing
```
pypdf2>=3.0.0             # PDF processing
python-docx>=0.8.11       # Word document processing
unstructured              # Advanced document parsing
```

### Vector Database
```
chromadb>=0.4.0           # Vector database
sentence-transformers     # Alternative embeddings
```

### Utilities
```
python-dotenv             # Environment management
pathlib                  # File path handling
typing                   # Type hints
```

## 🔧 Extending the System

This implementation provides a solid foundation for advanced features:

### 🗃️ Storage & Retrieval
- **Multiple Vector Stores**: Pinecone, Weaviate, Qdrant integration
- **Hybrid Search**: Combine semantic and keyword search
- **Custom Embeddings**: Fine-tuned models for specific domains
- **Metadata Filtering**: Advanced document filtering capabilities

### 🤖 AI & Models
- **Multiple LLM Providers**: Anthropic Claude, Cohere, local models
- **Model Switching**: Dynamic model selection based on query type
- **Custom Prompts**: Domain-specific prompt templates
- **Evaluation Metrics**: Answer quality assessment

### 📄 Document Processing
- **OCR Integration**: Scanned document processing
- **Table Extraction**: Structured data from documents
- **Image Analysis**: Vision models for document images
- **Language Support**: Multi-language document processing

### 🔐 Enterprise Features
- **User Authentication**: Multi-user support with session management
- **Access Control**: Document-level permissions
- **Audit Logging**: Comprehensive usage tracking
- **API Endpoints**: RESTful API for integration

### 🚀 Performance & Scale
- **Batch Processing**: Large document collections
- **Caching**: Query result caching for performance
- **Load Balancing**: Multi-instance deployment
- **Monitoring**: Performance metrics and alerting

## 🚨 Troubleshooting

### Common Issues

1. **🔑 OpenAI API Key Issues**
   - **Problem**: API key errors or authentication failures
   - **Solution**: Verify API key format (starts with `sk-`), check account balance
   - **Options**: Set via environment variable, .env file, or Streamlit interface

2. **📁 File Upload Errors**
   - **Problem**: "Access is denied" or permission errors
   - **Solution**: Application now uses system temp directory with automatic fallback
   - **Enhanced**: Robust cleanup and error recovery mechanisms

3. **💾 Memory Issues**
   - **Problem**: Large documents causing memory errors
   - **Solution**: Adjust chunk sizes, process smaller batches
   - **Monitoring**: Check system info sidebar for memory usage

4. **🔄 Session State Display**
   - **Problem**: Debug information showing on page
   - **Solution**: Clear browser cache, restart application
   - **Prevention**: Enhanced session state management implemented

5. **🖥️ Streamlit Context Warnings**
   - **Problem**: "Missing ScriptRunContext" warnings
   - **Solution**: Always use `streamlit run app.py` or `.\run.bat`
   - **Check**: Automatic context validation added

### Performance Tips

- **📊 Document Size**: Optimal chunk size is 500-1500 characters
- **🔍 Query Length**: Shorter, specific questions work better
- **💬 Context**: Clear chat history for unrelated topics
- **🗃️ Storage**: Regularly clear vector store for better performance

### Advanced Troubleshooting

1. **Enable Detailed Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check System Resources**
   - Monitor the system info sidebar
   - Verify available disk space
   - Check memory usage

3. **Validate Environment**
   ```bash
   # Run system tests
   python src/test_setup.py
   ```

4. **Reset Application State**
   ```bash
   # Clear vector database
   rm -rf chroma_db/
   
   # Clear temporary files
   rm -rf temp_uploads/
   ```

## 📄 License

This project is provided under MIT License for educational and development purposes.

---

## 🤝 Contributing

Feel free to submit issues, feature requests, and pull requests to improve this QA RAG chatbot!

## 📞 Support

For questions and support:
1. Check the troubleshooting section above
2. Review the detailed documentation in `DOCUMENTATION.md`
3. Examine the code structure in `CODE_MAP.md`
4. Run the system tests with `python src/test_setup.py`
