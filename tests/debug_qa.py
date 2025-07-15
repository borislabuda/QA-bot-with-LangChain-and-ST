"""
Quick test to identify the QA chain initialization issue
"""

import os
from dotenv import load_dotenv
load_dotenv()

print("Testing QA Chain Initialization...")
print(f"OpenAI API Key configured: {bool(os.getenv('OPENAI_API_KEY'))}")

try:
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
    from src.vector_store_manager import VectorStoreManager
    print("✓ VectorStoreManager import successful")
    
    # Test vector store initialization
    vector_manager = VectorStoreManager()
    print("✓ VectorStoreManager initialization successful")
    
    # Test retriever
    retriever = vector_manager.as_retriever()
    print(f"✓ Retriever created: {type(retriever)}")
    
except Exception as e:
    print(f"✗ VectorStoreManager error: {e}")

# Test QA Chain Manager
try:
    from src.qa_chain_manager import QAChainManager
    print("✓ QAChainManager import successful")
    
    # Test QA chain initialization
    if 'retriever' in locals():
        qa_manager = QAChainManager(retriever=retriever)
        print("✓ QAChainManager initialization successful")
        
        # Test a simple question
        response = qa_manager.ask_question("What is this document about?")
        print(f"✓ QA chain working: {response.get('success', False)}")
        if not response.get('success', False):
            print(f"   Error: {response.get('error', 'Unknown error')}")
    
except Exception as e:
    print(f"✗ QAChainManager error: {e}")
    import traceback
    print(f"   Full traceback: {traceback.format_exc()}")

print("\nTest completed. Check above for any ✗ errors.")
