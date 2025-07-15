# QA RAG Chatbot with LangChain and ChromaDB

A simple yet powerful Question-Answering RAG (Retrieval-Augmented Generation) chatbot built with LangChain, ChromaDB, and Streamlit.

## Features

- **Document Processing**: Load and process PDF, TXT, and DOCX files
- **Vector Store**: ChromaDB for efficient document storage and retrieval
- **Advanced QA**: Conversational retrieval chain with context awareness
- **Chat History**: Maintains conversation context across questions
- **Simple Interface**: Clean Streamlit interface focused on functionality
- **Source Citations**: Shows which documents were used to generate answers

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_DB_PATH=./chroma_db
EMBEDDINGS_MODEL=text-embedding-ada-002
CHAT_MODEL=gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.1
```

### 3. Run the Application

```bash
streamlit run app.py
```

## Usage

### 1. Upload Documents
- Use the "Documents" tab to upload PDF, TXT, or DOCX files
- Or specify a directory path to load multiple files at once
- Documents are processed and stored in the ChromaDB vector store

### 2. Ask Questions
- Switch to the "Chat" tab
- Enter questions about your uploaded documents
- The system will provide answers based on the document content
- View source documents used for each answer

### 3. Manage History
- Conversation history is maintained for context
- Clear history when starting a new topic
- View previous questions and answers in the chat history

## Architecture

### Core Components

1. **DocumentLoader** (`src/document_loader.py`)
   - Handles loading PDF, TXT, and DOCX files
   - Splits documents into manageable chunks
   - Preserves metadata for source tracking

2. **VectorStoreManager** (`src/vector_store_manager.py`)
   - Manages ChromaDB vector store operations
   - Handles document indexing with OpenAI embeddings
   - Provides similarity search capabilities

3. **QAChainManager** (`src/qa_chain_manager.py`)
   - Implements conversational retrieval chain
   - Advanced prompt engineering for better responses
   - Manages chat history and context

4. **Streamlit App** (`app.py`)
   - Simple, functional web interface
   - Document upload and processing
   - Interactive chat interface

### Key Features

- **Chunk-based Processing**: Documents are split into optimal chunks for better retrieval
- **Semantic Search**: Uses OpenAI embeddings for intelligent document retrieval
- **Context Awareness**: Maintains conversation history for follow-up questions
- **Source Attribution**: Shows which documents contributed to each answer
- **Error Handling**: Comprehensive error handling and logging

## Configuration

### Model Settings
- **Chat Model**: gpt-3.5-turbo (configurable)
- **Embeddings**: text-embedding-ada-002
- **Temperature**: 0.1 (conservative responses)
- **Max Tokens**: 1000
- **Memory Window**: 10 conversation turns

### Document Processing
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Supported Formats**: PDF, TXT, DOCX

## File Structure

```
QA bot with LangChain and ST/
├── src/                      # Source code package
│   ├── __init__.py          # Package initialization
│   ├── document_loader.py   # Document loading and processing
│   ├── vector_store_manager.py # ChromaDB vector store management
│   ├── qa_chain_manager.py  # QA chain and conversation handling
│   └── test_setup.py        # Component-level tests
├── app.py                   # Streamlit web interface
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration template
├── test_setup.py           # System test script
├── setup.bat              # Windows setup script
├── run.bat                # Windows run script
└── README.md              # This file
```

## Dependencies

- **streamlit**: Web interface framework
- **langchain**: LLM application framework
- **chromadb**: Vector database for document storage
- **openai**: OpenAI API integration
- **pypdf2**: PDF document processing
- **python-docx**: Word document processing
- **sentence-transformers**: Additional embedding options

## Extending the System

This basic implementation can be extended with:

- Multiple vector store backends (Pinecone, Weaviate, etc.)
- Different LLM providers (Anthropic, Cohere, local models)
- Advanced document processing (OCR, table extraction)
- User authentication and session management
- Batch processing capabilities
- Custom embedding models
- Question answering evaluation metrics

## Troubleshooting

### Common Issues

1. **OpenAI API Key**: Ensure your OpenAI API key is set in the `.env` file
2. **Memory Usage**: Large documents may require adjusting chunk sizes
3. **File Formats**: Ensure uploaded files are in supported formats (PDF, TXT, DOCX)
4. **Dependencies**: Install all required packages from `requirements.txt`

### Logging

The system includes comprehensive logging. Check console output for detailed error messages and processing information.

## License

This project is provided as-is for educational and development purposes.
