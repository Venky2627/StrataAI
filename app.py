import streamlit as st
import time
from config.settings import APP_TITLE, APP_ICON, APP_DESCRIPTION

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title=f"{APP_TITLE} - {APP_DESCRIPTION}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Routing
if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

# ============================================================================
# PREMIUM CSS INJECTION (OPTION A: Pure CSS Animations)
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Splash Screen Animations */
    .splash-container {
        height: 70vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeInSlow 2s ease-out forwards;
    }
    
    .splash-title {
        font-size: 8rem;
        font-weight: 700;
        letter-spacing: -0.05em;
        line-height: 1;
        margin-bottom: 2rem;
        background: linear-gradient(270deg, #1D1D1F, #86868B, #1D1D1F);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 8s ease infinite;
    }

    @media (prefers-color-scheme: dark) {
        .splash-title {
            background: linear-gradient(270deg, #FFFFFF, #A1A1A6, #FFFFFF);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    }

    /* Dashboard Animations (Staggered Fade-in) */
    .stagger-1 { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both; }
    .stagger-2 { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both; }
    .stagger-3 { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both; }
    .stagger-4 { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both; }

    /* Custom Keyframes */
    @keyframes fadeInSlow {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Minimalist Feature Cards */
    .feature-card {
        background: rgba(120, 120, 128, 0.03);
        border: 1px solid rgba(120, 120, 128, 0.1);
        border-radius: 8px;
        padding: 2rem;
        height: 100%;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: default;
    }
    
    .feature-card:hover {
        transform: translateY(-4px) scale(1.02);
        background: rgba(120, 120, 128, 0.08);
        border-color: rgba(120, 120, 128, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    }

    .feature-icon { font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.8; }
    .feature-title { font-weight: 600; font-size: 1.25rem; margin-bottom: 0.5rem; letter-spacing: -0.01em; }
    .feature-text { font-size: 0.95rem; line-height: 1.5; color: #86868b; font-weight: 400; }

    /* Hide sidebar button when on splash screen */
    .hide-sidebar [data-testid="collapsedControl"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# STATE 1: SPLASH SCREEN (LANDING PAGE)
# ============================================================================
if not st.session_state.entered_app:
    # Hide the sidebar and header completely on the splash screen
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        header { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="splash-container">
        <div class="splash-title">StrataAI.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the Enter button using columns
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Enter Workspace", use_container_width=True, type="primary"):
            st.session_state.entered_app = True
            st.rerun()


# ============================================================================
# STATE 2: MAIN DASHBOARD
# ============================================================================
else:
    # Hero Section
    st.markdown("""
    <div class="stagger-1" style="text-align: center; padding: 3rem 0;">
        <div style="font-size: 3rem; font-weight: 700; letter-spacing: -0.04em;">Intelligence for your documents.</div>
        <div style="font-size: 1.2rem; color: #86868b; margin-top: 1rem;">Upload, analyze, and comprehend at the speed of thought.</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    # Capabilities Grid
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card stagger-2">
            <div class="feature-icon">❖</div>
            <div class="feature-title">Ingestion Engine</div>
            <div class="feature-text">High-fidelity extraction of text from complex PDF documents, preparing raw data for intelligent chunking.</div>
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
            <div class="feature-text">Context-aware explanations, dynamic quiz generation, and intelligent study plans synthesized by advanced LLMs.</div>
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

    # About Section
    st.markdown("""
    <div class="stagger-4" style="margin-top: 5rem; padding-top: 3rem; border-top: 1px solid rgba(120, 120, 128, 0.2);">
        <div style="font-size: 2rem; font-weight: 600; margin-bottom: 1rem;">Built for deep comprehension.</div>
        <div style="font-size: 1.1rem; line-height: 1.6; color: #86868b; max-width: 800px;">
            StrataAI is an enterprise-grade study assistant engineered from the ground up using state-of-the-art Retrieval-Augmented Generation (RAG) and Agentic frameworks. By breaking down complex academic and technical documents, it creates an adaptive learning environment tailored to rigorous intellectual pursuit.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Design
    with st.sidebar:
        st.markdown("### System Status")
        st.markdown("<span style='color: #86868b; font-size: 0.9rem;'>Phase 1: Foundation (Active)</span>", unsafe_allow_html=True)
        st.progress(0.08)
        st.write("")
        
        st.markdown("### Architecture Stack")
        st.markdown("""
        <div style="font-family: monospace; font-size: 0.85rem; color: #86868b; line-height: 1.8;">
        ├─ UI: Streamlit<br>
        ├─ Logic: Python 3.13<br>
        ├─ Memory: ChromaDB<br>
        ├─ State: SQLite<br>
        ├─ Brain: Gemini / Groq<br>
        └─ Agents: LangGraph
        </div>
        """, unsafe_allow_html=True)
