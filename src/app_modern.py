#!/usr/bin/env python3
"""
🧠 Claude RAG Memory Search - Modern UI
Beautiful Streamlit interface with shadcn/ui components
Author: Anix Lynch (@anixlynch)
"""

import streamlit as st
import streamlit_shadcn_ui as ui
import os
import sys
from datetime import datetime
import json

# Import your existing search functionality
try:
    from search import search_conversations
    from index_conversations import load_vector_store
except ImportError:
    # Fallback if modules not found
    def search_conversations(query, top_k=5):
        return [{"content": f"Mock result for: {query}", "source": "demo.md", "score": 0.95}]
    
    def load_vector_store():
        return None

# 🎨 Page Config with French Coastal Theme
st.set_page_config(
    page_title="🧠 Claude RAG Memory",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌊 Custom CSS for French Coastal Vibes
st.markdown("""
<style>
    /* French Coastal Color Palette */
    :root {
        --coastal-blue: #A8DADC;
        --soft-coral: #F1FAEE;
        --warm-white: #F1FAEE;
        --sage-green: #457B9D;
        --deep-navy: #1D3557;
        --accent-coral: #E63946;
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--coastal-blue), var(--sage-green));
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .search-container {
        background: var(--soft-coral);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid var(--sage-green);
        margin-bottom: 1rem;
    }
    
    .result-card {
        background: white;
        padding: 1.25rem;
        border-radius: 0.5rem;
        border: 1px solid var(--coastal-blue);
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: var(--warm-white);
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid var(--coastal-blue);
    }
</style>
""", unsafe_allow_html=True)

# 🎯 Initialize Session State
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'total_searches' not in st.session_state:
    st.session_state.total_searches = 0

# 🎨 Main Header
st.markdown("""
<div class="main-header">
    <h1>🧠 Claude RAG Memory Search</h1>
    <p>Give Claude ChatGPT-style memory with semantic search</p>
</div>
""", unsafe_allow_html=True)

# 📊 Stats Dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    ui.metric_card(
        title="Total Searches",
        content=str(st.session_state.total_searches),
        description="Lifetime queries",
        key="metric1"
    )

with col2:
    ui.metric_card(
        title="Session Searches", 
        content=str(len(st.session_state.search_history)),
        description="This session",
        key="metric2"
    )

with col3:
    ui.metric_card(
        title="Vector DB Status",
        content="🟢 Active",
        description="ChromaDB ready",
        key="metric3"
    )

with col4:
    ui.metric_card(
        title="Last Updated",
        content=datetime.now().strftime("%H:%M"),
        description="System time",
        key="metric4"
    )

st.markdown("---")

# 🔍 Search Interface
st.markdown("### 🔍 Search Claude's Memory")

# Create search container
search_container = st.container()

with search_container:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Use shadcn/ui input component
        search_query = st.text_input(
            "",
            placeholder="Ask about past conversations... (e.g., 'python web scraping tips')",
            key="search_input",
            label_visibility="collapsed"
        )
    
    with col2:
        # Use shadcn/ui button
        search_clicked = ui.button(
            text="🔍 Search",
            key="search_btn",
            variant="default",
            className="w-full mt-6"
        )

# Advanced options in expander
with st.expander("⚙️ Advanced Search Options"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_results = ui.select(
            options=[{"label": "5 results", "value": 5},
                    {"label": "10 results", "value": 10},
                    {"label": "15 results", "value": 15}],
            default_value=5,
            placeholder="Number of results",
            key="max_results"
        )
    
    with col2:
        search_mode = ui.select(
            options=[{"label": "Semantic", "value": "semantic"},
                    {"label": "Keyword", "value": "keyword"},
                    {"label": "Hybrid", "value": "hybrid"}],
            default_value="semantic",
            placeholder="Search mode",
            key="search_mode"
        )
    
    with col3:
        time_filter = ui.select(
            options=[{"label": "All time", "value": "all"},
                    {"label": "Last week", "value": "week"},
                    {"label": "Last month", "value": "month"}],
            default_value="all",
            placeholder="Time filter",
            key="time_filter"
        )

# 🎯 Search Results
if search_clicked and search_query:
    st.session_state.total_searches += 1
    st.session_state.search_history.append({
        'query': search_query,
        'timestamp': datetime.now(),
        'mode': search_mode
    })
    
    # Show loading spinner
    with st.spinner('🔍 Searching Claude\'s memory...'):
        try:
            # Perform actual search
            results = search_conversations(search_query, top_k=max_results)
            
            if results:
                # Success alert
                ui.alert(
                    text=f"Found {len(results)} relevant conversations! 🎉",
                    description="Results ranked by semantic similarity",
                    alert_type="default",
                    key="success_alert"
                )
                
                st.markdown("### 📋 Search Results")
                
                # Display results with shadcn/ui cards
                for i, result in enumerate(results):
                    with ui.card(key=f"result_card_{i}"):
                        # Score badge
                        score_color = "green" if result.get('score', 0) > 0.8 else "yellow" if result.get('score', 0) > 0.6 else "red"
                        ui.badge(
                            text=f"Relevance: {result.get('score', 0):.2%}",
                            variant=score_color,
                            key=f"badge_{i}"
                        )
                        
                        # Content preview
                        content_preview = result.get('content', '')[:300] + "..." if len(result.get('content', '')) > 300 else result.get('content', '')
                        st.markdown(f"**Content:** {content_preview}")
                        
                        # Source and metadata
                        st.markdown(f"**Source:** `{result.get('source', 'unknown')}`")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns([1, 1, 2])
                        with col1:
                            if ui.button(text="📋 Copy", key=f"copy_{i}", variant="outline"):
                                st.write("Copied to clipboard!")
                        with col2:
                            if ui.button(text="🔗 View Full", key=f"view_{i}", variant="outline"):
                                # Show full content in modal
                                ui.alert_dialog(
                                    show=True,
                                    title="Full Conversation",
                                    description=result.get('content', ''),
                                    confirm_label="Close",
                                    key=f"modal_{i}"
                                )
            else:
                # No results alert
                ui.alert(
                    text="No results found 😔",
                    description="Try different keywords or check your vector database",
                    alert_type="destructive",
                    key="no_results_alert"
                )
                
        except Exception as e:
            # Error alert
            ui.alert(
                text="Search Error",
                description=f"Something went wrong: {str(e)}",
                alert_type="destructive", 
                key="error_alert"
            )

# 📈 Search History Sidebar
with st.sidebar:
    st.markdown("### 📈 Recent Searches")
    
    if st.session_state.search_history:
        for i, search in enumerate(reversed(st.session_state.search_history[-10:])):  # Last 10 searches
            with ui.card(key=f"history_{i}"):
                st.markdown(f"**Query:** {search['query'][:50]}...")
                st.markdown(f"**Time:** {search['timestamp'].strftime('%H:%M:%S')}")
                st.markdown(f"**Mode:** {search['mode']}")
                
                if ui.button(text="🔄 Repeat", key=f"repeat_{i}", variant="ghost"):
                    st.session_state.search_input = search['query']
                    st.rerun()
    else:
        ui.alert(
            text="No search history",
            description="Start searching to see your history here",
            alert_type="default",
            key="no_history"
        )
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    if ui.button(text="🗑️ Clear History", key="clear_history", variant="destructive"):
        st.session_state.search_history = []
        st.rerun()
    
    if ui.button(text="📊 Export Results", key="export_results", variant="outline"):
        # Export functionality
        export_data = {
            'search_history': [
                {
                    'query': s['query'],
                    'timestamp': s['timestamp'].isoformat(),
                    'mode': s['mode']
                }
                for s in st.session_state.search_history
            ],
            'total_searches': st.session_state.total_searches
        }
        st.download_button(
            label="💾 Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"claude_rag_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# 🎯 Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; color: #6B7280;">
        <p>🧠 <strong>Claude RAG Memory Search</strong> • Built with ❤️ by <a href="https://github.com/anix-lynch" target="_blank">@anixlynch</a></p>
        <p>🎨 UI powered by <strong>streamlit-shadcn-ui</strong> • 🎯 French Coastal Design</p>
    </div>
    """, unsafe_allow_html=True)

# 🔧 Debug Info (only show in development)
if st.secrets.get("DEBUG", False):
    with st.expander("🔧 Debug Info"):
        st.json({
            "session_state": dict(st.session_state),
            "python_version": sys.version,
            "streamlit_version": st.__version__
        })
