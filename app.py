import streamlit as st
from config.settings import APP_TITLE, APP_ICON, APP_DESCRIPTION
from src.ui.theme import get_base_css

st.set_page_config(
    page_title=f"{APP_TITLE} - {APP_DESCRIPTION}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

# Inject shared theme
st.markdown(get_base_css(), unsafe_allow_html=True)

# Page-specific CSS has been moved to theme.py to avoid inline CSS bloat.


# ============================================================================
# STATE 1: SPLASH SCREEN
# ============================================================================
if not st.session_state.entered_app:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        header { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="splash-container">
        <div class="splash-title">StrataAI.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Enter Workspace", use_container_width=True, type="primary"):
            st.session_state.entered_app = True
            st.rerun()


# ============================================================================
# STATE 2: MAIN DASHBOARD
# ============================================================================
else:
    st.markdown("""
    <div class="stagger-1" style="text-align: center; padding: 3rem 0;">
        <div class="hero-title">Intelligence for your documents.</div>
        <div class="hero-subtitle">Upload, analyze, and comprehend at the speed of thought.</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card stagger-2">
            <div class="feature-icon">❖</div>
            <div class="feature-title">Ingestion Engine</div>
            <div class="feature-text">High-fidelity extraction from PDFs, Word docs, and images using AI-powered OCR and intelligent chunking.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card stagger-2">
            <div class="feature-icon">⚲</div>
            <div class="feature-title">Semantic Search</div>
            <div class="feature-text">Vectorized knowledge retrieval powered by Sentence Transformers and ChromaDB architecture.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card stagger-2">
            <div class="feature-icon">⟡</div>
            <div class="feature-title">Generative Synthesis</div>
            <div class="feature-text">Context-aware explanations, dynamic quiz generation, and intelligent study plans synthesized by Gemini.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="feature-card stagger-3">
            <div class="feature-icon">◱</div>
            <div class="feature-title">Agentic Workflows</div>
            <div class="feature-text">LangGraph-orchestrated agents that evaluate answers and adapt learning paths dynamically.</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card stagger-3">
            <div class="feature-icon">◴</div>
            <div class="feature-title">Progress Tracking</div>
            <div class="feature-text">Persistent SQLite state management to track comprehension and milestone achievements.</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card stagger-3">
            <div class="feature-icon">⌘</div>
            <div class="feature-title">System Architecture</div>
            <div class="feature-text">Built on a robust, decoupled foundation prioritizing separation of concerns and maintainability.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-section stagger-4">
        <div class="about-title">Built for deep comprehension.</div>
        <div class="about-text">
            StrataAI is an enterprise-grade study assistant engineered from the ground up using state-of-the-art Retrieval-Augmented Generation (RAG) and Agentic frameworks. By breaking down complex academic and technical documents, it creates an adaptive learning environment tailored to rigorous intellectual pursuit.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### System Status")
        st.markdown("<span style='color: #86868b; font-size: 0.9rem;'>Phase 1: Foundation (Active)</span>", unsafe_allow_html=True)
        st.progress(0.08)
        st.write("")

        st.markdown("### Architecture Stack")
        st.markdown("""
        <div class="stack-tree">
        ├─ <span class="accent">UI</span>: Streamlit<br>
        ├─ <span class="accent">Logic</span>: Python 3.13<br>
        ├─ <span class="accent">Memory</span>: ChromaDB<br>
        ├─ <span class="accent">State</span>: SQLite<br>
        ├─ <span class="accent">Brain</span>: Gemini 2.5 Flash<br>
        └─ <span class="accent">Agents</span>: LangGraph
        </div>
        """, unsafe_allow_html=True)