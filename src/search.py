#!/usr/bin/env python3
"""
Claude RAG Memory Search - CLI Interface
Search your Claude conversations from the command line
"""

import sys
import argparse
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def search_conversations(query: str, top_k: int = 5, similarity_threshold: float = 0.0):
    """Search Claude conversations using semantic similarity"""
    
    # Initialize embeddings
    print("🧠 Loading embedding model...")
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load vector database
    db_path = Path("data/chroma_db")
    if not db_path.exists():
        print("❌ No conversation database found!")
        print("💡 Run 'python src/index_conversations.py' first to index your chats.")
        return
    
    print("🔍 Loading conversation database...")
    vectordb = Chroma(
        persist_directory=str(db_path),
        embedding_function=embedder
    )
    
    # Perform search
    print(f"🔎 Searching for: '{query}'")
    results = vectordb.similarity_search_with_relevance_scores(
        query, 
        k=top_k
    )
    
    # Filter by similarity threshold
    filtered_results = [
        (doc, score) for doc, score in results 
        if score >= similarity_threshold
    ]
    
    if not filtered_results:
        print("😕 No relevant conversations found.")
        print("💡 Try a different query or lower the similarity threshold.")
        return
    
    # Display results
    print(f"\n✨ Found {len(filtered_results)} relevant conversations:")
    print("=" * 60)
    
    for i, (doc, score) in enumerate(filtered_results, 1):
        metadata = doc.metadata
        
        print(f"\n📄 Result {i} (Relevance: {score:.2f})")
        print(f"📁 Source: {metadata.get('filename', 'Unknown')}")
        print(f"🗣️ Speaker: {metadata.get('speaker', 'Unknown')}")
        print(f"🔢 Turn: {metadata.get('conversation_turn', 'N/A')}")
        print("\n💬 Content:")
        print("-" * 40)
        
        # Show content preview
        content = doc.page_content
        if len(content) > 300:
            content = content[:300] + "..."
        print(content)
        
        if i < len(filtered_results):
            print("\n" + "=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Search your Claude conversation history",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/search.py "python web scraping"
  python src/search.py "career advice" --top-k 10
  python src/search.py "debugging tips" --threshold 0.7
        """
    )
    
    parser.add_argument(
        "query",
        help="Search query"
    )
    
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of results to return (default: 5)"
    )
    
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.0,
        help="Minimum similarity threshold (default: 0.0)"
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    try:
        search_conversations(
            query=args.query,
            top_k=args.top_k,
            similarity_threshold=args.threshold
        )
    except KeyboardInterrupt:
        print("\n👋 Search cancelled.")
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("💡 Make sure you've run the setup script and indexed your conversations.")

if __name__ == "__main__":
    main()