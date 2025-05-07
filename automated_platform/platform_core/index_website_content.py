# index_website_content.py

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Set
import hashlib
import logging
from urllib.parse import urljoin, urlparse
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """Scrapes and processes web content for RAG applications."""
    
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.visited_urls = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.session = requests.Session()
    
    def scrape_website(self, start_url, max_pages=10, same_domain_only=True):
        """Scrape a website starting from a URL, following links up to max_pages.
        
        Args:
            start_url (str): Starting URL
            max_pages (int): Maximum number of pages to scrape
            same_domain_only (bool): Whether to stay on the same domain
        
        Returns:
            list: List of dictionaries with page content and metadata
        """
        if not self.base_url:
            self.base_url = start_url
        
        # Parse the domain of the start URL
        start_domain = urlparse(start_url).netloc
        
        # Initialize data structures
        to_visit = [start_url]
        self.visited_urls = set()
        scraped_pages = []
        
        while to_visit and len(self.visited_urls) < max_pages:
            # Get the next URL to visit
            url = to_visit.pop(0)
            
            # Skip if already visited
            if url in self.visited_urls:
                continue
            
            # Skip if not on the same domain and same_domain_only is True
            if same_domain_only and urlparse(url).netloc != start_domain:
                continue
            
            # Mark as visited
            self.visited_urls.add(url)
            
            # Fetch the page
            try:
                logger.info(f"Scraping: {url}")
                time.sleep(1)  # Be respectful with rate limiting
                response = self.session.get(url, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch {url}: Status code {response.status_code}")
                    continue
                
                # Parse the page
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract content
                page_content = self._extract_content(soup, url)
                if page_content:
                    scraped_pages.append(page_content)
                
                # Extract links for further crawling
                links = self._extract_links(soup, url)
                
                # Add new links to the to_visit list
                for link in links:
                    if link not in self.visited_urls and link not in to_visit:
                        to_visit.append(link)
            
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
        
        return scraped_pages
    
    def _extract_content(self, soup, url):
        """Extract meaningful content from a web page.
        
        Args:
            soup (BeautifulSoup): BeautifulSoup object
            url (str): URL of the page
        
        Returns:
            dict: Dictionary with content and metadata
        """
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'iframe']):
            element.decompose()
        
        # Extract title
        title = soup.title.string if soup.title else "No Title"
        
        # Find main content
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup.body
        
        if not main_content:
            return None
        
        # Extract text content
        content_text = main_content.get_text(separator='\n', strip=True)
        
        # Skip pages with too little content
        if len(content_text) < 100:
            return None
        
        # Generate content hash for change detection
        content_hash = hashlib.md5(content_text.encode()).hexdigest()
        
        # Extract headings for better context
        headings = []
        for heading in main_content.find_all(['h1', 'h2', 'h3', 'h4']):
            heading_text = heading.get_text(strip=True)
            if heading_text:
                headings.append(heading_text)
        
        # Create metadata
        metadata = {
            "source": title,
            "url": url,
            "crawl_time": time.time(),
            "content_hash": content_hash,
            "headings": headings
        }
        
        return {
            "text": content_text,
            "metadata": metadata
        }
    
    def _extract_links(self, soup, base_url):
        """Extract links from a web page.
        
        Args:
            soup (BeautifulSoup): BeautifulSoup object
            base_url (str): Base URL for resolving relative links
        
        Returns:
            set: Set of absolute URLs
        """
        links = set()
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            
            # Skip empty links, javascript links, or anchors
            if not href or href.startswith('javascript:') or href.startswith('#'):
                continue
            
            # Resolve relative URLs
            absolute_url = urljoin(base_url, href)
            
            # Remove fragments
            absolute_url = absolute_url.split('#')[0]
            
            # Normalize the URL
            if absolute_url.endswith('/'):
                absolute_url = absolute_url[:-1]
            
            links.add(absolute_url)
        
        return links


def process_web_content(content_items, embedding_manager, vector_store):
    """Process web content, chunk it, and store in vector database.
    
    Args:
        content_items (list): List of content items from web scraping
        embedding_manager: Instance of EmbeddingManager
        vector_store: Instance of VectorStore
    
    Returns:
        int: Number of chunks indexed
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    total_chunks = 0
    
    # Process each content item
    for item in content_items:
        try:
            # Split the text into chunks
            chunks = text_splitter.split_text(item["text"])
            
            # Create documents with metadata
            documents = []
            for i, chunk_text in enumerate(chunks):
                chunk_id = hashlib.md5(f"{item['metadata']['url']}-{i}".encode()).hexdigest()
                
                documents.append({
                    "text": chunk_text,
                    "metadata": {
                        **item["metadata"],
                        "chunk_id": chunk_id,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                })
            
            # Generate embeddings
            embeddings = embedding_manager.generate_embeddings([doc["text"] for doc in documents])
            
            # Store in vector database
            vector_store.add_documents(documents, embeddings)
            
            total_chunks += len(chunks)
            logger.info(f"Indexed {len(chunks)} chunks from {item['metadata']['url']}")
        
        except Exception as e:
            logger.error(f"Error processing content: {str(e)}")
    
    return total_chunks


def index_website(url, embedding_manager, vector_store, max_pages=10):
    """Index a website starting from a URL.
    
    Args:
        url (str): Starting URL
        embedding_manager: Instance of EmbeddingManager
        vector_store: Instance of VectorStore
        max_pages (int): Maximum number of pages to index
    
    Returns:
        int: Number of chunks indexed
    """
    logger.info(f"Starting indexing of {url}")
    
    # Create web scraper and scrape the website
    scraper = WebScraper(base_url=url)
    content_items = scraper.scrape_website(url, max_pages=max_pages)
    
    # Process the content
    total_chunks = process_web_content(content_items, embedding_manager, vector_store)
    
    logger.info(f"Completed indexing of {url}. Indexed {total_chunks} chunks from {len(content_items)} pages.")
    
    return total_chunks