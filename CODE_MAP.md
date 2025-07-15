# QA RAG Chatbot - Code Architecture Map

## Overview
This document provides a visual representation of the code architecture, showing how classes and functions are interconnected throughout the QA RAG Chatbot system.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    app.py                                           │
│                               (Main Application)                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              Streamlit Functions                                    │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                  │
│  │ main()          │    │ configure_api   │    │ initialize_     │                  │
│  │ (Entry Point)   │──▶│ _key()           │───▶│ session_state()│                  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                  │
│                                        │                                            │
│                                        ▼                                            │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                  │
│  │ document_upload │    │ setup_vector_   │    │ setup_qa_chain()│                  │
│  │ _section()      │───▶│ store()         │───▶│                │                  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                  │
│                                        │                                            │
│                                        ▼                                            │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                  │
│  │ qa_chat_        │    │ process_        │    │ display_qa_     │                  │
│  │ section()       │───▶│ question()      │───▶│ response()     │                  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                               Core Components                                       │
│                                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                  │
│  │ DocumentLoader  │    │ VectorStore     │    │ QAChainManager  │                  │
│  │ (Class)         │───▶│ Manager         │───▶│ (Class)        │                  │
│  │                 │    │ (Class)         │    │                 │                  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              External Dependencies                                  │
│                                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                  │
│  │ OpenAI API      │    │ ChromaDB        │    │ LangChain       │                  │
│  │ (External)      │    │ (External)      │    │ (External)      │                  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Detailed Class/Function Relationships

### 1. Main Application Flow (app.py)

```
main()
├── st.set_page_config()
├── initialize_session_state()
├── configure_api_key()
├── document_upload_section()
│   ├── process_uploaded_files()
│   │   └── DocumentLoader.load_multiple_files()
│   ├── process_directory()
│   │   └── DocumentLoader.load_directory()
│   └── clear_vector_store()
│       └── VectorStoreManager.delete_collection()
├── qa_chat_section()
│   ├── setup_qa_chain()
│   │   └── QAChainManager.__init__()
│   ├── process_question()
│   │   └── QAChainManager.ask_question()
│   └── display_qa_response()
└── sidebar_info()
    ├── VectorStoreManager.get_collection_info()
    └── QAChainManager.get_memory_summary()
```

### 2. DocumentLoader Class Hierarchy

```
DocumentLoader
├── __init__()
│   ├── RecursiveCharacterTextSplitter (LangChain)
│   └── supported_extensions (set)
├── load_single_document()
│   ├── PyPDFLoader (LangChain)
│   ├── TextLoader (LangChain)
│   └── Docx2txtLoader (LangChain)
├── load_directory()
│   └── load_single_document() (recursive call)
└── load_multiple_files()
    └── load_single_document() (iterative calls)
```

### 3. VectorStoreManager Class Hierarchy

```
VectorStoreManager
├── __init__()
│   ├── OpenAIEmbeddings (LangChain)
│   ├── Path (pathlib)
│   └── _initialize_vector_store()
├── _initialize_vector_store()
│   ├── _vector_store_exists()
│   └── Chroma (LangChain)
├── _vector_store_exists()
├── add_documents()
│   └── Chroma.add_documents()
├── similarity_search()
│   └── Chroma.similarity_search()
├── similarity_search_with_score()
│   └── Chroma.similarity_search_with_score()
├── get_collection_info()
│   └── Chroma._collection.count()
├── delete_collection()
│   ├── Chroma.delete_collection()
│   └── _initialize_vector_store()
└── as_retriever()
    └── Chroma.as_retriever()
```

### 4. QAChainManager Class Hierarchy

```
QAChainManager
├── __init__()
│   ├── ChatOpenAI (LangChain)
│   ├── ConversationSummaryBufferMemory (LangChain)
│   ├── _create_qa_chain()
│   └── conversation_history (list)
├── _create_qa_chain()
│   ├── _create_custom_prompt()
│   └── ConversationalRetrievalChain (LangChain)
├── _create_custom_prompt()
│   └── PromptTemplate (LangChain)
├── ask_question()
│   ├── qa_chain() (ConversationalRetrievalChain)
│   └── conversation_history.append()
├── clear_history()
│   ├── memory.clear()
│   └── conversation_history.clear()
└── get_memory_summary()
    └── memory.chat_memory.messages
```

## Data Flow Architecture

### Document Processing Flow
```
User Upload → process_uploaded_files() → DocumentLoader.load_multiple_files() 
    → DocumentLoader.load_single_document() → RecursiveCharacterTextSplitter.split_documents()
    → VectorStoreManager.add_documents() → OpenAIEmbeddings.embed_documents()
    → ChromaDB.add_documents() → Persistent Storage
```

### Question Answering Flow
```
User Question → process_question() → QAChainManager.ask_question()
    → ConversationalRetrievalChain() → VectorStoreManager.similarity_search()
    → ChromaDB.similarity_search() → OpenAIEmbeddings.embed_query()
    → ChatOpenAI.generate() → display_qa_response()
```

## Component Dependencies

### External Library Dependencies
```
OpenAI API
├── OpenAIEmbeddings (VectorStoreManager)
├── ChatOpenAI (QAChainManager)
└── Environment Variable (OPENAI_API_KEY)

ChromaDB
├── Chroma (VectorStoreManager)
├── Collection Management
└── Persistent Storage

LangChain
├── Document Processing
│   ├── PyPDFLoader
│   ├── TextLoader
│   ├── Docx2txtLoader
│   └── RecursiveCharacterTextSplitter
├── Vector Operations
│   ├── OpenAIEmbeddings
│   └── Chroma
├── Memory Management
│   └── ConversationSummaryBufferMemory
├── Chain Operations
│   ├── ConversationalRetrievalChain
│   └── PromptTemplate
└── Schema
    ├── Document
    ├── BaseRetriever
    ├── HumanMessage
    └── AIMessage

Streamlit
├── UI Components
│   ├── st.file_uploader
│   ├── st.text_input
│   ├── st.button
│   ├── st.expander
│   └── st.spinner
├── State Management
│   └── st.session_state
└── Layout
    ├── st.columns
    ├── st.tabs
    └── st.sidebar
```

## Session State Management

### Streamlit Session State Variables
```
st.session_state
├── vector_store_manager (VectorStoreManager instance)
├── qa_chain_manager (QAChainManager instance)
├── conversation_history (list of dict)
├── documents_loaded (boolean)
└── api_key_configured (boolean)
```

## Function Call Patterns

### Initialization Pattern
```
main() → initialize_session_state() → configure_api_key() → setup_vector_store() → setup_qa_chain()
```

### Document Upload Pattern
```
document_upload_section() → process_uploaded_files() → DocumentLoader() → VectorStoreManager.add_documents()
```

### Question Processing Pattern
```
qa_chat_section() → process_question() → QAChainManager.ask_question() → display_qa_response()
```

### Error Handling Pattern
```
try:
    Core Function
except Exception as e:
    logger.error()
    st.error()
    return error_response
```

## Testing Architecture

### Test File Structure
```
tests/
├── test_setup.py
│   ├── test_imports()
│   ├── test_environment()
│   ├── test_document_loader()
│   ├── test_vector_store()
│   └── test_qa_chain()
├── test_vector_store.py
└── debug_qa.py
```

### Test Dependencies
```
test_setup.py
├── test_imports() → All core modules
├── test_environment() → Environment variables
├── test_document_loader() → DocumentLoader class
├── test_vector_store() → VectorStoreManager class
└── test_qa_chain() → QAChainManager class
```

## Key Design Patterns

### 1. **Singleton Pattern** (Session State)
- `st.session_state` maintains single instances of managers
- Prevents multiple database connections

### 2. **Factory Pattern** (Document Loaders)
- `DocumentLoader.load_single_document()` creates appropriate loader based on file type
- Supports PDF, TXT, DOCX formats

### 3. **Builder Pattern** (QA Chain)
- `QAChainManager._create_qa_chain()` assembles complex chain from components
- Configurable prompts and memory

### 4. **Observer Pattern** (UI Updates)
- Streamlit automatically re-renders on state changes
- Real-time feedback to user actions

### 5. **Strategy Pattern** (Search Methods)
- `similarity_search()` vs `similarity_search_with_score()`
- Different retrieval strategies based on requirements

## Critical Connection Points

### 1. **App → Components**
```
app.py functions → Core classes (DocumentLoader, VectorStoreManager, QAChainManager)
```

### 2. **Components → External APIs**
```
VectorStoreManager → OpenAI Embeddings API
QAChainManager → OpenAI Chat API
```

### 3. **Components → Storage**
```
VectorStoreManager → ChromaDB → File System
```

### 4. **Memory → Context**
```
QAChainManager.memory → ConversationSummaryBufferMemory → Chat History
```

This code map provides a comprehensive view of how all components interact within the QA RAG Chatbot system, making it easier to understand the architecture and debug issues.
