#!/usr/bin/env python3
"""
Test script to verify vector store functionality after fixing persist() issue.
"""

import os
import getpass
from langchain.schema import Document

# Prompt for API key if not already set
if not os.getenv('OPENAI_API_KEY'):
    api_key = getpass.getpass("Enter your OpenAI API key: ")
    os.environ['OPENAI_API_KEY'] = api_key

from src.vector_store_manager import VectorStoreManager

def test_vector_store():
    """Test vector store operations."""
    print("Testing Vector Store Manager...")
    
    try:
        # Initialize vector store manager
        vector_store_manager = VectorStoreManager(
            persist_directory="./test_chroma_db",
            collection_name="test_documents"
        )
        print("✓ Vector store manager initialized")
        
        # Create test documents
        test_docs = [
            Document(
                page_content="This is a test document about artificial intelligence.",
                metadata={"source": "test1.txt", "type": "test"}
            ),
            Document(
                page_content="Machine learning is a subset of artificial intelligence.",
                metadata={"source": "test2.txt", "type": "test"}
            )
        ]
        
        # Add documents to vector store
        doc_ids = vector_store_manager.add_documents(test_docs)
        print(f"✓ Added {len(doc_ids)} documents to vector store")
        
        # Test similarity search
        results = vector_store_manager.similarity_search("artificial intelligence", k=2)
        print(f"✓ Similarity search returned {len(results)} results")
        
        # Print results
        for i, doc in enumerate(results, 1):
            print(f"  Result {i}: {doc.page_content[:50]}...")
        
        # Test retriever
        retriever = vector_store_manager.as_retriever()
        if retriever:
            print("✓ Retriever created successfully")
        else:
            print("✗ Failed to create retriever")
        
        print("\n✅ All vector store tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_vector_store()
