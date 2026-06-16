# ============================================================================
# STRATAAI - MAIN APPLICATION ENTRY POINT (app.py)
# ============================================================================
# WHY THIS FILE EXISTS:
# This is the FIRST file Streamlit runs when you execute:
#   streamlit run app.py
#
# It serves as the HOME PAGE of our application — the "front door" that
# users see when they first open StrataAI. It displays the landing page
# with app branding, feature overview, and getting-started instructions.
#
# ARCHITECTURE DECISION:
# app.py should be THIN — it only handles the home page UI.
# All business logic (PDF processing, RAG, quiz generation, etc.)
# lives in the src/ directory and is called by individual pages in pages/.
#
# STREAMLIT RE-RUN MODEL:
# Every time a user interacts with ANY widget (button, slider, text input),
# Streamlit re-runs this ENTIRE file from top to bottom. This means:
#   - Variables defined here are recreated every time
#   - Heavy operations (loading models, reading files) should be cached
#   - Use st.session_state to persist data across re-runs
# For now our app is simple, so we don't need caching yet. Week 3+ will add it.
# ============================================================================

import streamlit as st
# Streamlit is our ENTIRE frontend framework.
# The 'st' object provides every UI widget we'll ever need:
#   st.title()       → big heading
#   st.write()       → text/markdown output
#   st.sidebar       → left sidebar
#   st.columns()     → side-by-side layout
#   st.file_uploader → file upload widget
#   st.chat_input    → chat text box
# We import it as 'st' by convention (like pandas as pd, numpy as np).

# We import our centralized settings so app configuration comes from ONE place.
# If we ever rename the app or change the icon, we update config/settings.py
# and every file that imports from it automatically gets the new values.
from config.settings import APP_TITLE, APP_ICON, APP_DESCRIPTION


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
# st.set_page_config() MUST be the first Streamlit command in the script.
# If you put ANY st.* call before this, Streamlit will throw an error.
# It configures the browser tab (title, favicon) and page layout.
#
# Parameters explained:
#   page_title    → Text shown in the browser tab
#   page_icon     → Favicon (emoji or image URL) shown in the browser tab
#   layout="wide" → Uses full screen width instead of a narrow centered column.
#                   "wide" is better for dashboards and data-heavy apps.
#                   "centered" (default) is better for simple text-focused apps.
#   initial_sidebar_state → Whether the sidebar starts open or collapsed.
#                           "expanded" = visible by default on desktop.
# ============================================================================
st.set_page_config(
    page_title=f"{APP_TITLE} - {APP_DESCRIPTION}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# CUSTOM STYLING
# ============================================================================
# Streamlit's default styling is functional but plain. To make our app look
# premium and polished, we inject custom CSS using st.markdown().
#
# st.markdown(unsafe_allow_html=True) lets us write raw HTML/CSS.
# The <style> tag contains CSS rules that override Streamlit's defaults.
#
# WHY INLINE CSS AND NOT A SEPARATE FILE?
# Streamlit doesn't have a built-in way to load external CSS files easily.
# The standard approach in the Streamlit community is to inject CSS via
# st.markdown(). For larger apps, you could load from a file and inject,
# but for now inline is simpler and keeps everything in one place.
# ============================================================================
st.markdown(
    """
    <style>
    /* ---- Hide Streamlit's default UI clutter ---- */
    /* The hamburger menu, "Made with Streamlit" footer, and header decoration
       add visual noise. Hiding them makes the app look more professional
       and custom-built rather than "obviously a Streamlit app". */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---- Feature card styling ---- */
    /* Each feature (Chat, Quiz, Explain, etc.) is displayed in a styled card.
       The gradient background, rounded corners, and hover effect make the
       landing page feel modern and premium rather than a plain list. */
    .feature-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.5);
    }

    /* ---- Hero section (the big title area) ---- */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.3rem;
        color: #a0aec0;
        margin-bottom: 2rem;
    }

    /* ---- Status badge ---- */
    /* A small pill-shaped badge that shows the project is in active development.
       The green dot animation draws attention and signals activity. */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 999px;
        padding: 0.3rem 1rem;
        font-size: 0.85rem;
        color: #10b981;
        margin-bottom: 1.5rem;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ---- Sidebar styling ---- */
    .sidebar-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    .tech-pill {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 999px;
        padding: 0.2rem 0.7rem;
        font-size: 0.8rem;
        color: #818cf8;
        margin: 0.2rem;
    }
    </style>
    """,
    # unsafe_allow_html=True is required for Streamlit to render raw HTML.
    # By default, st.markdown() strips HTML for security. We explicitly
    # opt in because we trust our own HTML (it's not user-provided input).
    unsafe_allow_html=True,
)


# ============================================================================
# SIDEBAR
# ============================================================================
# The sidebar is a collapsible panel on the left side of the screen.
# It's perfect for secondary information — project details, navigation,
# settings — that shouldn't clutter the main content area.
#
# st.sidebar.* mirrors the main st.* API:
#   st.sidebar.title()  → title in the sidebar
#   st.sidebar.write()  → text in the sidebar
#   st.sidebar.image()  → image in the sidebar
# Anything you can do on the main page, you can do in the sidebar.
# ============================================================================
with st.sidebar:
    # st.markdown() renders Markdown AND raw HTML (when unsafe_allow_html=True).
    # We use it here instead of st.title() to apply our custom CSS classes.
    st.markdown(f"# {APP_ICON} {APP_TITLE}")
    st.markdown(f"*{APP_DESCRIPTION}*")

    st.divider()  # A horizontal line to visually separate sections.

    st.markdown('<p class="sidebar-header">🛠️ Tech Stack</p>', unsafe_allow_html=True)

    # Display the tech stack as styled pill badges.
    # Each technology gets its own pill for a clean, modern look.
    tech_stack = [
        "Python", "Streamlit", "LangChain", "ChromaDB",
        "Gemini", "Groq", "LangGraph", "SQLite",
    ]
    # We build one big HTML string with all the pills, then render it once.
    # Calling st.markdown() in a loop would work but is less efficient
    # (each call triggers a re-render cycle).
    pills_html = " ".join(
        f'<span class="tech-pill">{tech}</span>' for tech in tech_stack
    )
    st.markdown(pills_html, unsafe_allow_html=True)

    st.divider()

    st.markdown('<p class="sidebar-header">📅 Roadmap Progress</p>', unsafe_allow_html=True)

    # st.progress() creates an animated progress bar.
    # Value is between 0.0 (empty) and 1.0 (full).
    # 1/12 = Week 1 out of 12 weeks = ~8% complete.
    st.progress(1 / 12, text="Week 1 of 12")

    st.divider()

    st.markdown('<p class="sidebar-header">📊 Project Stats</p>', unsafe_allow_html=True)

    # st.metric() displays a number with a label, perfect for KPIs/stats.
    # delta shows a change indicator (green up arrow or red down arrow).
    # We use columns to place two metrics side by side.
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Features", value="0/9", delta="In Progress")
    with col2:
        st.metric(label="Week", value="1", delta="Setup")


# ============================================================================
# MAIN CONTENT - HERO SECTION
# ============================================================================
# The hero section is the first thing users see — it should immediately
# communicate WHAT the app does and WHO it's for. We use large text,
# a gradient title, and a clear description.
# ============================================================================

# Status badge — shows the project is in active development.
st.markdown(
    '<div class="status-badge"><span class="pulse-dot"></span> In Active Development</div>',
    unsafe_allow_html=True,
)

# Hero title with gradient effect (applied via CSS class .hero-title)
st.markdown(
    f'<div class="hero-title">{APP_ICON} {APP_TITLE}</div>',
    unsafe_allow_html=True,
)

# Subtitle explaining what the app does in one sentence.
st.markdown(
    '<div class="hero-subtitle">'
    "Upload your study materials. Chat with them. Get explanations, quizzes, "
    "and a personalized study plan — all powered by AI."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================================
# FEATURE CARDS
# ============================================================================
# We display each planned feature as a visually styled card.
# This gives users (and portfolio viewers) a clear overview of the app's
# capabilities, even before all features are built.
#
# st.columns(3) creates 3 equal-width columns for a grid layout.
# We use 'with col:' context manager to place widgets inside each column.
# ============================================================================

# Each feature is a tuple: (emoji, title, description, week)
# Storing them as data (not hardcoded UI) makes it easy to add/remove features.
features = [
    (
        "📄", "PDF Processing",
        "Upload multiple PDFs. Text is extracted, cleaned, and chunked for AI processing.",
        "Week 2",
    ),
    (
        "🔍", "Semantic Search",
        "Find relevant information using meaning-based search, not just keywords.",
        "Week 3",
    ),
    (
        "💬", "Chat with PDFs",
        "Ask questions about your documents and get accurate, sourced answers.",
        "Week 4",
    ),
    (
        "📝", "Smart Explanations",
        "Get explanations in formal, simple, or Hinglish style to match your preference.",
        "Week 5",
    ),
    (
        "❓", "Quiz Generation",
        "Auto-generate MCQs and short-answer questions to test your understanding.",
        "Week 6",
    ),
    (
        "✅", "Answer Evaluation",
        "Submit answers and receive AI-powered scoring with detailed feedback.",
        "Week 7",
    ),
    (
        "📅", "Study Plans",
        "Get a personalized, day-by-day study schedule based on your goals and timeline.",
        "Week 8",
    ),
    (
        "📊", "Progress Tracking",
        "Track your quiz scores, see improvement trends, and identify weak areas.",
        "Week 9",
    ),
    (
        "🤖", "AI Agents",
        "Intelligent routing that automatically decides how to help based on your request.",
        "Week 10",
    ),
]

# Create a 3-column grid layout for the feature cards.
# We process features in groups of 3 (one per row).
# range(0, len(features), 3) gives us: 0, 3, 6 — the start of each row.
for i in range(0, len(features), 3):
    cols = st.columns(3)
    # For each position in the row (0, 1, 2), place a feature card
    # if one exists at that index. The 'if' check handles the last row
    # which might have fewer than 3 features.
    for j, col in enumerate(cols):
        if i + j < len(features):
            emoji, title, desc, week = features[i + j]
            with col:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: #e2e8f0;
                            margin-bottom: 0.5rem;">{title}</div>
                        <div style="font-size: 0.85rem; color: #94a3b8;
                            margin-bottom: 0.75rem;">{desc}</div>
                        <div style="font-size: 0.75rem; color: #818cf8;">{week}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================================
# GETTING STARTED SECTION
# ============================================================================
# A quick guide for first-time visitors. In future milestones, this section
# will be replaced with actual interactive widgets (file uploader, chat input).
# ============================================================================

st.markdown("---")  # Horizontal divider

st.markdown("## 🚀 Getting Started")
st.markdown(
    """
    > **This app is under active development.** New features are added weekly
    > following a 12-week engineering roadmap.

    **Coming up next:**
    1. 📄 **PDF Upload** — Drag and drop your study materials
    2. 🔍 **Semantic Search** — Find information by meaning
    3. 💬 **AI Chat** — Ask questions, get sourced answers
    """
)


# ============================================================================
# FOOTER
# ============================================================================
# A simple footer with project attribution.
# We use Streamlit's built-in divider and centered text.
# ============================================================================

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    f"{APP_ICON} {APP_TITLE} — Built with ❤️ to master AI Engineering"
    "</div>",
    unsafe_allow_html=True,
)
