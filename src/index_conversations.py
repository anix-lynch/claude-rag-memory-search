#!/usr/bin/env python3
"""
Claude RAG Memory Search - Conversation Indexer
Process and index Claude chat exports for semantic search
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm

class ClaudeChatLoader:
    """Load and parse Claude Desktop chat exports"""
    
    def __init__(self, vault_path: str = "vault"):
        self.vault_path = Path(vault_path)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_all_conversations(self) -> List[Document]:
        """Load all markdown files from vault directory"""
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault directory not found: {self.vault_path}")
        
        documents = []
        md_files = list(self.vault_path.glob("*.md"))
        
        if not md_files:
            print("⚠️ No .md files found in vault directory!")
            print(f"💡 Add your Claude chat exports to: {self.vault_path.absolute()}")
            return documents
        
        print(f"📁 Found {len(md_files)} conversation files")
        
        for md_file in tqdm(md_files, desc="Loading conversations"):
            try:
                file_docs = self._load_single_file(md_file)
                documents.extend(file_docs)
            except Exception as e:
                print(f"⚠️ Error loading {md_file.name}: {e}")
        
        print(f"✨ Loaded {len(documents)} conversation chunks")
        return documents
    
    def _load_single_file(self, file_path: Path) -> List[Document]:
        """Load and process a single conversation file"""
        content = file_path.read_text(encoding='utf-8')
        
        # Split into conversation turns
        turns = self._parse_conversation_turns(content)
        
        # Create documents for each turn
        documents = []
        for i, turn in enumerate(turns):
            # Split long turns into chunks
            chunks = self.splitter.split_text(turn['content'])
            
            for j, chunk in enumerate(chunks):
                metadata = {
                    'source': str(file_path),
                    'filename': file_path.name,
                    'speaker': turn['speaker'],
                    'conversation_turn': i,
                    'chunk_id': j,
                    'total_chunks': len(chunks)
                }
                
                documents.append(Document(
                    page_content=chunk,
                    metadata=metadata
                ))
        
        return documents
    
    def _parse_conversation_turns(self, content: str) -> List[Dict[str, Any]]:
        """Parse markdown content into conversation turns"""
        turns = []
        
        # Split by double newlines to get sections
        sections = content.split('\n\n')
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Detect speaker
            speaker = 'unknown'
            clean_content = section
            
            # Look for speaker patterns
            if section.lower().startswith(('human:', 'user:')):
                speaker = 'human'
                clean_content = re.sub(r'^(human|user):\s*', '', section, flags=re.IGNORECASE)
            elif section.lower().startswith(('claude:', 'assistant:')):
                speaker = 'claude'
                clean_content = re.sub(r'^(claude|assistant):\s*', '', section, flags=re.IGNORECASE)
            elif section.startswith('#'):
                # Skip headers
                continue
            
            if clean_content.strip():
                turns.append({
                    'content': clean_content.strip(),
                    'speaker': speaker
                })
        
        return turns

def create_vector_database(documents: List[Document]) -> Chroma:
    """Create and populate ChromaDB vector database"""
    
    if not documents:
        raise ValueError("No documents to index!")
    
    print("🧠 Initializing embedding model...")
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create database directory
    db_path = Path("data/chroma_db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"🔄 Creating vector database with {len(documents)} documents...")
    
    # Create ChromaDB from documents
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedder,
        persist_directory=str(db_path)
    )
    
    print(f"✅ Vector database created at: {db_path.absolute()}")
    return vectordb

def main():
    """Main indexing workflow"""
    print("🧠 Claude RAG Memory Search - Conversation Indexer")
    print("=" * 50)
    
    try:
        # Load conversations
        loader = ClaudeChatLoader()
        documents = loader.load_all_conversations()
        
        if not documents:
            print("❌ No conversations to index.")
            return
        
        # Create vector database
        vectordb = create_vector_database(documents)
        
        # Test search
        print("\n🧪 Testing search functionality...")
        test_results = vectordb.similarity_search("hello", k=1)
        
        if test_results:
            print("✅ Search test successful!")
        else:
            print("⚠️ Search test returned no results")
        
        print("\n🎉 Indexing complete!")
        print("\n💡 Next steps:")
        print("  • Search: python src/search.py 'your query'")
        print("  • Web UI: streamlit run src/app.py")
        
    except Exception as e:
        print(f"\n❌ Error during indexing: {e}")
        print("💡 Make sure you have .md files in the vault/ directory")

if __name__ == "__main__":
    main()