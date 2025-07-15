"""
QA Chain Manager for RAG Chatbot

This module implements the Question-Answering chain using LangChain
with advanced prompt engineering and chat history management.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever, HumanMessage, AIMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QAChainManager:
    """
    Manages the Question-Answering chain for the RAG chatbot.
    
    Features:
    - Conversational retrieval with context awareness
    - Advanced prompt engineering for better responses
    - Chat history management with configurable window
    - Customizable response generation parameters
    """
    
    def __init__(
        self,
        retriever: BaseRetriever,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.1,
        max_tokens: int = 1000,
        memory_window: int = 10
    ):
        """
        Initialize the QA chain manager.
        
        Args:
            retriever (BaseRetriever): Vector store retriever for document search
            model_name (str): OpenAI chat model name
            temperature (float): Temperature for response generation
            max_tokens (int): Maximum tokens in response
            memory_window (int): Number of conversation turns to remember
        """
        self.retriever = retriever
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.memory_window = memory_window
        
        # Initialize chat model
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferWindowMemory(
            k=memory_window,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Initialize the QA chain
        self.qa_chain = self._create_qa_chain()
        
        # Store conversation history for UI display
        self.conversation_history: List[Dict[str, Any]] = []
    
    def _create_custom_prompt(self) -> PromptTemplate:
        """
        Create a custom prompt template for the QA chain.
        
        Returns:
            PromptTemplate: Custom prompt template with advanced engineering
        """
        template = """You are an intelligent assistant designed to answer questions based on the provided context documents. 
Your goal is to provide accurate, helpful, and comprehensive answers while being honest about the limitations of the available information.

INSTRUCTIONS:
1. Always base your answers primarily on the provided context
2. If the context doesn't contain enough information, clearly state this limitation
3. When possible, cite specific parts of the context that support your answer
4. Provide structured, well-organized responses
5. If asked about something not in the context, explain what you do know from the context
6. Be conversational but professional in tone

CONTEXT DOCUMENTS:
{context}

CONVERSATION HISTORY:
{chat_history}

CURRENT QUESTION: {question}

RESPONSE GUIDELINES:
- Start with a direct answer if possible
- Provide relevant details from the context
- If information is incomplete, suggest what additional information might be helpful
- Use bullet points or numbered lists for complex information
- End with a summary if the response is lengthy

ANSWER:"""

        return PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )
    
    def _create_qa_chain(self) -> ConversationalRetrievalChain:
        """
        Create the conversational retrieval QA chain.
        
        Returns:
            ConversationalRetrievalChain: Configured QA chain
        """
        try:
            # Create the conversational retrieval chain with simpler configuration
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.retriever,
                memory=self.memory,
                return_source_documents=True,
                verbose=True
            )
            
            return qa_chain
        except Exception as e:
            logger.error(f"Error creating QA chain: {str(e)}")
            # Fallback to basic configuration
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.retriever,
                return_source_documents=True
            )
            return qa_chain
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Process a question and return the answer with source documents.
        
        Args:
            question (str): User's question
            
        Returns:
            Dict[str, Any]: Response containing answer, sources, and metadata
        """
        if not question.strip():
            return {
                "answer": "Please provide a valid question.",
                "source_documents": [],
                "error": "Empty question"
            }
        
        try:
            logger.info(f"Processing question: {question[:100]}...")
            
            # Get response from the QA chain
            response = self.qa_chain({"question": question})
            
            # Extract answer and source documents
            answer = response.get("answer", "No answer generated")
            source_docs = response.get("source_documents", [])
            
            # Prepare source information
            sources = []
            for i, doc in enumerate(source_docs):
                source_info = {
                    "content": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                    "metadata": doc.metadata,
                    "source_number": i + 1
                }
                sources.append(source_info)
            
            # Store in conversation history
            conversation_entry = {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": answer,
                "source_count": len(sources)
            }
            self.conversation_history.append(conversation_entry)
            
            # Return structured response
            result = {
                "answer": answer,
                "source_documents": sources,
                "question": question,
                "timestamp": conversation_entry["timestamp"],
                "success": True
            }
            
            logger.info(f"Generated answer with {len(sources)} source documents")
            return result
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                "answer": f"I apologize, but I encountered an error while processing your question: {str(e)}",
                "source_documents": [],
                "error": str(e),
                "success": False
            }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the complete conversation history.
        
        Returns:
            List[Dict[str, Any]]: List of conversation entries
        """
        return self.conversation_history.copy()
    
    def clear_history(self):
        """
        Clear the conversation history and memory.
        """
        self.memory.clear()
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current memory state.
        
        Returns:
            Dict[str, Any]: Memory summary information
        """
        try:
            memory_variables = self.memory.load_memory_variables({})
            chat_history = memory_variables.get("chat_history", [])
            
            return {
                "total_conversations": len(self.conversation_history),
                "memory_window": self.memory_window,
                "current_memory_items": len(chat_history),
                "last_question": self.conversation_history[-1]["question"] if self.conversation_history else None
            }
        except Exception as e:
            logger.error(f"Error getting memory summary: {str(e)}")
            return {"error": str(e)}
    
    def update_chain_parameters(
        self,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Update the chain parameters dynamically.
        
        Args:
            temperature (float): New temperature value
            max_tokens (int): New max tokens value
        """
        try:
            if temperature is not None:
                self.temperature = temperature
                self.llm.temperature = temperature
            
            if max_tokens is not None:
                self.max_tokens = max_tokens
                self.llm.max_tokens = max_tokens
            
            logger.info(f"Updated chain parameters: temperature={self.temperature}, max_tokens={self.max_tokens}")
            
        except Exception as e:
            logger.error(f"Error updating chain parameters: {str(e)}")
            raise
