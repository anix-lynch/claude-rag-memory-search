#!/bin/bash
# 🎨 Modern UI Setup Script
# Upgrade your Claude RAG Memory Search with shadcn/ui components!

echo "🎀 Setting up Modern Claude RAG Memory Search UI..."
echo "💅 Powered by streamlit-shadcn-ui components"

# Install new requirements
echo "📦 Installing modern UI dependencies..."
pip install streamlit-shadcn-ui

# Run the modern app
echo "🚀 Launching modern UI..."
echo "✨ French coastal color palette activated!"
echo "🌊 Navigate to: http://localhost:8501"

streamlit run src/app_modern.py --server.port 8501
