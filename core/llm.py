# core/llm.py

from typing import List, Dict, Optional, Tuple, Any
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.callbacks.base import BaseCallbackHandler
from utils.config import config
from utils.helpers import format_chat_history
import json
import re
from urllib.parse import urlparse

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
        
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

class LLMManager:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=0.7,
            api_key=config.OPENAI_API_KEY,
            streaming=True
        )

        self.system_prompt = """You are an AI travel assistant for IndiGo Airlines, designed to provide clear, detailed, and accurate answers to user queries about IndiGo's services, policies, and offerings.

            IMPORTANT GUIDELINES:
            1. Provide comprehensive, detailed responses that fully answer the user's question.
            2. If the context doesn't contain enough information to answer the query completely, ASK FOLLOW-UP QUESTIONS to clarify what the user needs.
            3. Do not mention or reference that you're using "context" or "sources" in your response.
            4. If you don't have enough information to answer accurately, clearly state what you know and what additional information would be helpful. Don't give any generalised response if you don't know the answer
            5. Use a friendly, professional tone that represents IndiGo Airlines.
            6. Structure your answers in a clear, organized manner using paragraphs, bullet points, or numbered lists when appropriate.
            7. Include relevant details such as policies, procedures, requirements, or exceptions when applicable.
            8. Make sure your source citation and response aligns with the content which we have stored in our Database. 
            9. Don't use the content directly from the internet if it is not in the database. Your major focus to provide response on the context and query. 
            10. Your source of document should be only the Database where we have stored the embedding, don't cite directly from the internet.
            11. End your response on a clear concluding note, avoiding phrases like "Is there anything else you'd like to know?"

            Current context information:
            {context}

            Previous conversation history:
            {chat_history}
            
            Remember: If you need more information to provide an accurate answer, ASK A CLARIFYING QUESTION first.
        """
        
        self.human_prompt = "{question}"
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", self.human_prompt)
        ])
        
        self.chain = (
            {"context": RunnablePassthrough(), 
             "chat_history": RunnablePassthrough(), 
             "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        # Add a separate prompt for analyzing if clarification is needed
        self.clarification_system_prompt = """You are an AI assistant helping to determine if a user query needs clarification before providing a full response.
        
        Given the user's question and the available context information, determine:
        1. If the question is clear and specific enough to answer accurately with the available context
        2. If not, what specific clarifying questions would help provide a better answer

        Context information:
        {context}

        User question:
        {question}

        Previous conversation:
        {chat_history}

        Respond in JSON format with two fields:
        - "needs_clarification": Boolean (true/false)
        - "clarifying_questions": Array of strings (1-3 specific questions to ask the user if needed)
        - "reasoning": Brief explanation of why clarification is or isn't needed
        """
        
        self.clarification_prompt = ChatPromptTemplate.from_messages([
            ("system", self.clarification_system_prompt)
        ])
        
        # Non-streaming LLM for clarification assessment
        self.analysis_llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=0.3,
            api_key=config.OPENAI_API_KEY,
            streaming=False
        )
        
        self.clarification_chain = (
            {"context": RunnablePassthrough(), 
             "chat_history": RunnablePassthrough(), 
             "question": RunnablePassthrough()}
            | self.clarification_prompt
            | self.analysis_llm
            | StrOutputParser()
        )
    
    def extract_source_links(self, context_docs: List[Dict]) -> List[str]:
        """Extract unique source URLs from context documents."""
        sources = []
        for doc in context_docs:
            if 'metadata' in doc and 'url' in doc['metadata']:
                url = doc['metadata']['url']
                if url and url not in sources:
                    sources.append(url)
        return sources
    
    def needs_clarification(
        self,
        question: str,
        context: List[Dict],
        chat_history: Optional[List[Dict]] = None
    ) -> Tuple[bool, List[str]]:
        """Determine if the query needs clarification and suggest clarifying questions."""
        formatted_context = "\n\n".join([doc['text'] for doc in context])
        formatted_history = format_chat_history(chat_history) if chat_history else ""
        
        try:
            response = self.clarification_chain.invoke({
                "context": formatted_context,
                "chat_history": formatted_history,
                "question": question
            })
            
            # Parse JSON response
            result = json.loads(response)
            needs_clarification = result.get("needs_clarification", False)
            questions = result.get("clarifying_questions", [])
            
            return needs_clarification, questions
        except Exception as e:
            # If any error occurs, default to not needing clarification
            print(f"Error in clarification assessment: {str(e)}")
            return False, []
    
    def _extract_anchor_text(self, text: str, url: str) -> str:
        """Extract relevant anchor text for a URL from the content."""
        # Simple implementation - can be enhanced with NLP
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for sentence in sentences:
            if urlparse(url).path.lower() in sentence.lower():
                return sentence
        return ""
    
    def format_source_references(self, context_docs: List[Dict]) -> str:
        """Format source references with anchor texts and direct links."""
        source_lines = []
        seen_urls = set()
        
        for doc in context_docs:
            if 'metadata' not in doc:
                continue
                
            url = doc['metadata'].get('url', '')
            if not url or url in seen_urls:
                continue
                
            seen_urls.add(url)
            anchor_text = self._extract_anchor_text(doc['text'], url)
            
            if anchor_text:
                source_lines.append(f"🔗 {anchor_text} [Read more]({url})")
            else:
                source_lines.append(f"🔗 [Source]({url})")
        
        if source_lines:
            return "\n\n**References:**\n" + "\n".join(source_lines)
        return ""
    
    def generate_response(
        self,
        question: str,
        context: List[Dict],
        chat_history: Optional[List[Dict]] = None,
        streaming_container = None
    ) -> str:
        """Generate a comprehensive response with proper source attribution."""
        # Check for clarification needs
        needs_clarification, clarifying_questions = self.needs_clarification(
            question, context, chat_history
        )
        
        # if needs_clarification and clarifying_questions:
        #     return self._format_clarification_question(clarifying_questions)
        
        # Generate the main response
        formatted_context = "\n\n".join([
            f"CONTEXT {i+1}:\n{doc['text']}\n" 
            for i, doc in enumerate(context)
        ])
        
        response = self.chain.invoke({
            "context": formatted_context,
            "chat_history": format_chat_history(chat_history) if chat_history else "",
            "question": question
        })
        
        # Add formatted source references
        if not response.strip().endswith(("?", "...")):
            source_references = self.format_source_references(context)
            if source_references:
                response += f"\n\n{source_references}"
        
        return response