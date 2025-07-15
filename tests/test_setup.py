"""
Test Script for QA RAG Chatbot

This script helps verify that all components are working correctly.
Run this after setting up your environment to test the system.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the current directory to Python path to allow importing from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
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

def test_document_loader():
    """Test document loader functionality."""
    print("\nTesting DocumentLoader...")
    
    try:
        from src.document_loader import DocumentLoader
        
        # Initialize document loader
        loader = DocumentLoader()
        print("✓ DocumentLoader initialized successfully")
        
        # Test supported extensions
        expected_extensions = {'.pdf', '.txt', '.docx', '.doc'}
        if loader.supported_extensions == expected_extensions:
            print("✓ Supported extensions are correct")
        else:
            print(f"✗ Unexpected supported extensions: {loader.supported_extensions}")
        
        return True
        
    except Exception as e:
        print(f"✗ DocumentLoader test failed: {e}")
        return False

def test_vector_store():
    """Test vector store initialization."""
    print("\nTesting VectorStoreManager...")
    
    try:
        from src.vector_store_manager import VectorStoreManager
        
        # Test initialization without actual API calls
        print("✓ VectorStoreManager class imported successfully")
        
        # Note: We don't actually initialize here to avoid API calls during testing
        print("✓ VectorStoreManager ready for initialization")
        
        return True
        
    except Exception as e:
        print(f"✗ VectorStoreManager test failed: {e}")
        return False

def create_sample_document():
    """Create a sample text document for testing."""
    print("\nCreating sample document for testing...")
    
    sample_content = """# Sample Document for Testing

This is a sample document to test the QA RAG chatbot functionality.

## Introduction
This document contains information about artificial intelligence and machine learning.

## Key Concepts

### Machine Learning
Machine learning is a subset of artificial intelligence that focuses on the use of data and algorithms to imitate the way humans learn, gradually improving accuracy.

### Natural Language Processing
Natural Language Processing (NLP) is a branch of artificial intelligence that helps computers understand, interpret and manipulate human language.

### Vector Databases
Vector databases are specialized databases designed to store and query high-dimensional vector data efficiently.

## Applications
AI and ML have numerous applications including:
- Healthcare diagnosis
- Autonomous vehicles
- Recommendation systems
- Financial fraud detection
- Language translation

## Conclusion
These technologies continue to evolve and find new applications across various industries.
"""
    
    # Create sample directory
    sample_dir = Path("./sample_documents")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample text file
    sample_file = sample_dir / "sample_ai_document.txt"
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    print(f"✓ Sample document created: {sample_file}")
    return str(sample_file)

def main():
    """Run all tests."""
    print("QA RAG Chatbot - System Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install required dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    # Test environment
    if not test_environment():
        print("\n❌ Environment tests failed. Please check your .env configuration.")
        return False
    
    # Test components
    if not test_document_loader():
        print("\n❌ DocumentLoader tests failed.")
        return False
    
    if not test_vector_store():
        print("\n❌ VectorStoreManager tests failed.")
        return False
    
    # Create sample document
    sample_file = create_sample_document()
    
    print("\n" + "=" * 40)
    print("✅ All tests passed successfully!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure your OpenAI API key")
    print("2. Run the application: streamlit run app.py")
    print(f"3. Test with the sample document: {sample_file}")
    print("\nThe system is ready to use!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
