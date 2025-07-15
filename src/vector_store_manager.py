"""
Vector Store Manager for QA RAG Chatbot

This module manages the ChromaDB vector store including creation,
persistence, and retrieval operations.
"""

import os
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreManager:
    """
    Manages ChromaDB vector store operations for the QA RAG system.
    
    Handles:
    - Vector store creation and initialization
    - Document indexing with embeddings
    - Similarity search and retrieval
    - Persistence and loading of vector stores
    """
    
    def __init__(
        self, 
        persist_directory: str = "./chroma_db",
        collection_name: str = "qa_documents",
        embedding_model: str = "text-embedding-ada-002"
    ):
        """
        Initialize the vector store manager.
        
        Args:
            persist_directory (str): Directory to persist the vector store
            collection_name (str): Name of the ChromaDB collection
            embedding_model (str): OpenAI embedding model to use
        """
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            show_progress_bar=True
        )
        
        # Initialize vector store
        self.vector_store: Optional[Chroma] = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """
        Initialize or load existing ChromaDB vector store.
        """
        try:
            # Create persist directory if it doesn't exist
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            
            # Check if vector store already exists
            if self._vector_store_exists():
                logger.info(f"Loading existing vector store from {self.persist_directory}")
                self.vector_store = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=str(self.persist_directory)
                )
            else:
                logger.info(f"Creating new vector store at {self.persist_directory}")
                self.vector_store = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=str(self.persist_directory)
                )
                
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise
    
    def _vector_store_exists(self) -> bool:
        """
        Check if a vector store already exists in the persist directory.
        
        Returns:
            bool: True if vector store exists, False otherwise
        """
        chroma_db_path = self.persist_directory / "chroma.sqlite3"
        return chroma_db_path.exists()
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents (List[Document]): List of documents to add
            
        Returns:
            List[str]: List of document IDs that were added
        """
        if not documents:
            logger.warning("No documents provided to add")
            return []
        
        try:
            logger.info(f"Adding {len(documents)} documents to vector store")
            
            # Add documents to the vector store
            doc_ids = self.vector_store.add_documents(documents)
            
            # Note: ChromaDB with persist_directory automatically persists data
            # No need to call persist() explicitly in newer versions
            
            logger.info(f"Successfully added {len(doc_ids)} documents")
            return doc_ids
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform similarity search in the vector store.
        
        Args:
            query (str): Query string to search for
            k (int): Number of similar documents to retrieve
            filter_criteria (Dict): Optional metadata filters
            
        Returns:
            List[Document]: List of similar documents
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        
        try:
            # Perform similarity search
            if filter_criteria:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter=filter_criteria
                )
            else:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k
                )
            
            logger.info(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []
    
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = 4,
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> List[tuple]:
        """
        Perform similarity search with relevance scores.
        
        Args:
            query (str): Query string to search for
            k (int): Number of similar documents to retrieve
            filter_criteria (Dict): Optional metadata filters
            
        Returns:
            List[tuple]: List of (document, score) tuples
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        
        try:
            # Perform similarity search with scores
            if filter_criteria:
                results = self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k,
                    filter=filter_criteria
                )
            else:
                results = self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k
                )
            
            logger.info(f"Found {len(results)} similar documents with scores")
            return results
            
        except Exception as e:
            logger.error(f"Error performing similarity search with scores: {str(e)}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the current vector store collection.
        
        Returns:
            Dict[str, Any]: Collection information including document count
        """
        if not self.vector_store:
            return {"error": "Vector store not initialized"}
        
        try:
            # Get collection from the vector store
            collection = self.vector_store._collection
            
            return {
                "collection_name": self.collection_name,
                "document_count": collection.count(),
                "persist_directory": str(self.persist_directory)
            }
            
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"error": str(e)}
    
    def delete_collection(self):
        """
        Delete the entire vector store collection.
        Warning: This will permanently delete all stored documents.
        """
        try:
            if self.vector_store:
                self.vector_store.delete_collection()
                logger.info(f"Deleted collection: {self.collection_name}")
            
            # Reinitialize the vector store
            self._initialize_vector_store()
            
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise
    
    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Return the vector store as a LangChain retriever.
        
        Args:
            search_kwargs (Dict): Additional search parameters
            
        Returns:
            VectorStoreRetriever: LangChain retriever interface
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return None
        
        default_search_kwargs = {"k": 4}
        if search_kwargs:
            default_search_kwargs.update(search_kwargs)
        
        return self.vector_store.as_retriever(
            search_kwargs=default_search_kwargs
        )
