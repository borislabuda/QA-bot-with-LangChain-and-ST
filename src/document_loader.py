"""
Document Loader Module for QA RAG Chatbot

This module handles loading and processing of various document formats
including PDF, TXT, and DOCX files for the vector store.
"""

import os
import logging
from typing import List, Optional
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Handles loading and processing of various document formats.
    
    Supports:
    - PDF files (.pdf)
    - Text files (.txt)
    - Word documents (.docx, .doc)
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document loader with text splitting parameters.
        
        Args:
            chunk_size (int): Maximum size of each text chunk
            chunk_overlap (int): Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Supported file extensions
        self.supported_extensions = {'.pdf', '.txt', '.docx', '.doc'}
    
    def load_single_document(self, file_path: str) -> List[Document]:
        """
        Load a single document and return its chunks.
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            List[Document]: List of document chunks
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return []
        
        file_extension = file_path.suffix.lower()
        
        if file_extension not in self.supported_extensions:
            logger.warning(f"Unsupported file type: {file_extension}")
            return []
        
        try:
            # Choose appropriate loader based on file extension
            if file_extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif file_extension == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif file_extension in ['.docx', '.doc']:
                loader = Docx2txtLoader(str(file_path))
            else:
                logger.error(f"No loader available for {file_extension}")
                return []
            
            # Load the document
            documents = loader.load()
            
            # Add metadata to documents
            for doc in documents:
                doc.metadata.update({
                    'source_file': str(file_path),
                    'file_name': file_path.name,
                    'file_type': file_extension
                })
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            logger.info(f"Loaded {len(chunks)} chunks from {file_path.name}")
            return chunks
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            return []
    
    def load_directory(self, directory_path: str) -> List[Document]:
        """
        Load all supported documents from a directory.
        
        Args:
            directory_path (str): Path to the directory containing documents
            
        Returns:
            List[Document]: List of all document chunks from the directory
        """
        directory_path = Path(directory_path)
        
        if not directory_path.exists() or not directory_path.is_dir():
            logger.error(f"Directory not found: {directory_path}")
            return []
        
        all_chunks = []
        
        # Find all supported files in the directory
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                chunks = self.load_single_document(str(file_path))
                all_chunks.extend(chunks)
        
        logger.info(f"Loaded {len(all_chunks)} total chunks from {directory_path}")
        return all_chunks
    
    def load_multiple_files(self, file_paths: List[str]) -> List[Document]:
        """
        Load multiple documents from a list of file paths.
        
        Args:
            file_paths (List[str]): List of file paths to load
            
        Returns:
            List[Document]: List of all document chunks
        """
        all_chunks = []
        
        for file_path in file_paths:
            chunks = self.load_single_document(file_path)
            all_chunks.extend(chunks)
        
        return all_chunks
