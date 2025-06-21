#!/bin/bash
# 🧠 Claude RAG Memory Search - Setup Script

echo "🚀 Setting up Claude RAG Memory Search..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p vault
mkdir -p data/chroma_db
mkdir -p assets

# Test installation
echo "🧪 Testing installation..."
python -c "import chromadb, langchain, streamlit, sentence_transformers; print('✅ All packages installed successfully!')"

echo "🎉 Setup complete!"
echo ""
echo "💡 Next steps:"
echo "  1. Add your Claude chat exports to the vault/ directory"
echo "  2. Run: python src/index_conversations.py"
echo "  3. Search: python src/search.py 'your query'"
echo "  4. Web UI: streamlit run src/app.py"
echo ""
echo "🌍 Web UI will be available at: http://localhost:8501"