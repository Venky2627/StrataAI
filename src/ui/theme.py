"""
StrataAI - Premium Theme Engine
================================
Shared CSS that powers the visual identity across ALL pages.
Every page calls get_base_css() to inject the universal theme,
then layers its own page-specific CSS on top.
"""

def get_base_css():
    """Returns the universal premium CSS theme injected into every page."""
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ============================================
   CUSTOM CURSOR - Precision Targeting Dot
   A red dot with a faint ring. Feels like
   a heads-up display from a sci-fi cockpit.
============================================ */

html, body, .stApp, [class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] *,
button, input, textarea, a, label, p, span, div,
[data-testid="stChatInput"] textarea,
.stMarkdown, .stButton > button,
[data-testid="stFileUploader"],
[data-testid="stExpander"] {
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='3' fill='%23ff5d5d'/%3E%3Ccircle cx='16' cy='16' r='8' fill='none' stroke='%23ff5d5d' stroke-width='1' opacity='0.5'/%3E%3C/svg%3E") 16 16, crosshair !important;
}

/* ============================================
   GLOBAL RESET & TYPOGRAPHY
============================================ */

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Nuclear option: Force ALL layout containers to be transparent */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > div,
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stChatInputContainer"],
.stBottomBlockContainer,
.stChatInputContainer,
footer {
    background: transparent !important;
    background-color: transparent !important;
}

/* Hide the blinking cursor globally */
* {
    caret-color: transparent !important;
}

/* Re-enable the caret ONLY for active text inputs */
input, textarea, [contenteditable="true"] {
    caret-color: #ff5d5d !important;
}

/* ============================================
   PREMIUM DARK BACKGROUND
============================================ */

.stApp {
    background: linear-gradient(
        135deg,
        #030712 0%,
        #050816 40%,
        #0a0a1a 70%,
        #030712 100%
    ) !important;
    overflow-x: hidden;
    min-height: 100vh;
}

/* ============================================
   CUSTOM SCROLLBAR
============================================ */

::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(255,93,93,0.4), rgba(255,140,93,0.2));
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, rgba(255,93,93,0.7), rgba(255,140,93,0.4));
}
* {
    scrollbar-width: thin;
    scrollbar-color: rgba(255,93,93,0.3) transparent;
}

/* ============================================
   CUSTOM TEXT SELECTION
============================================ */

::selection {
    background: rgba(255,93,93,0.3);
    color: #ffffff;
}
::-moz-selection {
    background: rgba(255,93,93,0.3);
    color: #ffffff;
}

/* ============================================
   SIDEBAR - DEEP FROSTED GLASS
============================================ */

section[data-testid="stSidebar"] {
    background: rgba(6,6,16,0.88) !important;
    backdrop-filter: blur(30px) saturate(1.4) !important;
    -webkit-backdrop-filter: blur(30px) saturate(1.4) !important;
    border-right: 1px solid rgba(255,255,255,0.03) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    padding-top: 1rem;
}

/* Sidebar alert cards */
section[data-testid="stSidebar"] .stAlert {
    background: linear-gradient(135deg, rgba(0,120,255,0.06), rgba(0,200,255,0.03)) !important;
    border: 1px solid rgba(0,150,255,0.12) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(10px);
}

/* ============================================
   BUTTONS - PREMIUM GLOW WITH SWEEP
============================================ */

.stButton > button {
    border-radius: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    position: relative !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #ff5d5d, #ff4040) !important;
    box-shadow: 0 4px 15px rgba(255,93,93,0.2);
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 40px rgba(255,93,93,0.35) !important;
}

/* Shine sweep on hover */
.stButton > button::before {
    content: "";
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.12), transparent);
    transition: left 0.6s ease;
}
.stButton > button:hover::before {
    left: 100%;
}

/* ============================================
   PROGRESS BAR - ANIMATED
============================================ */

.stProgress > div > div > div {
    background: linear-gradient(90deg, #ff5d5d, #ff8a5d, #ff5d5d) !important;
    background-size: 200% auto;
    animation: shimmer 2s linear infinite;
    border-radius: 10px !important;
}

/* ============================================
   EXPANDERS - GLASS
============================================ */

[data-testid="stExpander"] {
    background: rgba(255,255,255,0.015) !important;
    border: 1px solid rgba(255,255,255,0.04) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.025) !important;
}

/* ============================================
   METRICS & ALERTS
============================================ */

.stAlert {
    border-radius: 14px !important;
    backdrop-filter: blur(8px);
}

/* Success messages */
[data-testid="stAlert"][data-baseweb*="positive"],
div[data-testid="stNotification"][aria-label*="Success"] {
    background: rgba(0,200,100,0.08) !important;
    border: 1px solid rgba(0,200,100,0.2) !important;
}

/* ============================================
   TABS
============================================ */

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    background: rgba(255,93,93,0.15) !important;
}

/* ============================================
   ANIMATION LIBRARY
============================================ */

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

@keyframes shimmer {
    from { background-position: -200% center; }
    to   { background-position:  200% center; }
}

@keyframes pulseGlow {
    0%   { box-shadow: 0 0 5px  rgba(255,93,93,0.2); }
    50%  { box-shadow: 0 0 25px rgba(255,93,93,0.4), 0 0 50px rgba(255,93,93,0.1); }
    100% { box-shadow: 0 0 5px  rgba(255,93,93,0.2); }
}

@keyframes pulseStatus {
    0%   { box-shadow: 0 0 0    rgba(0,255,136,0); }
    50%  { box-shadow: 0 0 20px rgba(0,255,136,0.35); }
    100% { box-shadow: 0 0 0    rgba(0,255,136,0); }
}

@keyframes floatLogo {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-14px); }
    100% { transform: translateY(0px); }
}

@keyframes orbFloat1 {
    0%   { transform: translate(0, 0) scale(1); }
    25%  { transform: translate(40px, -60px) scale(1.05); }
    50%  { transform: translate(-20px, -30px) scale(0.95); }
    75%  { transform: translate(30px, 20px) scale(1.02); }
    100% { transform: translate(0, 0) scale(1); }
}

@keyframes orbFloat2 {
    0%   { transform: translate(0, 0) scale(1); }
    25%  { transform: translate(-50px, 40px) scale(0.97); }
    50%  { transform: translate(30px, -50px) scale(1.03); }
    75%  { transform: translate(-20px, -20px) scale(1); }
    100% { transform: translate(0, 0) scale(1); }
}

@keyframes orbFloat3 {
    0%   { transform: translate(0, 0) rotate(0deg); }
    33%  { transform: translate(50px, 25px) rotate(120deg); }
    66%  { transform: translate(-35px, -50px) rotate(240deg); }
    100% { transform: translate(0, 0) rotate(360deg); }
}

@keyframes aurora {
    0%   { transform: rotate(0deg) scale(1); }
    50%  { transform: rotate(180deg) scale(1.15); }
    100% { transform: rotate(360deg) scale(1); }
}

@keyframes scanline {
    0%   { top: -10%; }
    100% { top: 110%; }
}

@keyframes borderGlow {
    0%   { border-color: rgba(255,93,93,0.1); }
    50%  { border-color: rgba(255,93,93,0.4); }
    100% { border-color: rgba(255,93,93,0.1); }
}

@keyframes textGlow {
    0%   { text-shadow: 0 0 10px rgba(255,93,93,0.2); }
    50%  { text-shadow: 0 0 25px rgba(255,93,93,0.45), 0 0 50px rgba(255,93,93,0.1); }
    100% { text-shadow: 0 0 10px rgba(255,93,93,0.2); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to   { opacity: 1; transform: translateX(0); }
}

@keyframes breathe {
    0%   { opacity: 0.4; }
    50%  { opacity: 1; }
    100% { opacity: 0.4; }
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Stagger delay utility classes */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.25s; }
.stagger-3 { animation-delay: 0.45s; }
/* ============================================
   MINIMALIST SPINNER (Tiny Bouncing Balls)
============================================ */
[data-testid="stSpinner"] > div {
    display: none !important;
}

[data-testid="stSpinner"] {
    margin: 1rem 0 !important;
    display: flex !important;
    align-items: center !important;
    height: 30px !important;
    padding-left: 5px !important;
}

[data-testid="stSpinner"]::after {
    content: "";
    display: block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #a0a0a0;
    box-shadow: 12px 0 0 0 #a0a0a0, 24px 0 0 0 #a0a0a0;
    animation: typingBalls 1s infinite alternate;
}

@keyframes typingBalls {
    0% {
        background-color: rgba(160, 160, 160, 1);
        box-shadow: 12px 0 0 0 rgba(160, 160, 160, 0.2), 24px 0 0 0 rgba(160, 160, 160, 0.2);
    }
    50% {
        background-color: rgba(160, 160, 160, 0.2);
        box-shadow: 12px 0 0 0 rgba(160, 160, 160, 1), 24px 0 0 0 rgba(160, 160, 160, 0.2);
    }
    100% {
        background-color: rgba(160, 160, 160, 0.2);
        box-shadow: 12px 0 0 0 rgba(160, 160, 160, 0.2), 24px 0 0 0 rgba(160, 160, 160, 1);
    }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ============================================
   PAGE-SPECIFIC STYLES (Merged for Cleanliness)
============================================ */

/* Floating Orbs (Global Background) */
.stApp::before {
    content: ""; position: fixed; width: 550px; height: 550px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,80,80,0.10), transparent 65%);
    top: -200px; right: -120px; animation: orbFloat1 18s ease-in-out infinite;
    pointer-events: none; z-index: -1;
}
.stApp::after {
    content: ""; position: fixed; width: 450px; height: 450px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,180,255,0.08), transparent 65%);
    bottom: -180px; left: -120px; animation: orbFloat2 22s ease-in-out infinite;
    pointer-events: none; z-index: -1;
}

/* Study Space UI */
.study-header { text-align: center; padding: 1.5rem 0 2rem; animation: fadeUp 0.8s ease; }
.ai-status { display: inline-block; color: #00ff88; font-size: 0.75rem; font-weight: 600; letter-spacing: 3px; padding: 0.35rem 1rem; border-radius: 999px; border: 1px solid rgba(0,255,136,0.2); background: rgba(0,255,136,0.04); margin-bottom: 1.2rem; animation: pulseStatus 2.5s ease infinite; text-transform: uppercase; }
.study-title { font-size: 3.5rem; font-weight: 800; letter-spacing: -2px; color: white; text-shadow: 0 0 40px rgba(255,255,255,0.06); line-height: 1.1; }
.study-subtitle { color: #6a6a75; font-size: 1.05rem; margin-top: 0.7rem; font-weight: 400; }
.stChatMessageAvatar, [data-testid="chatAvatarIcon-user"], [data-testid="chatAvatarIcon-assistant"] { display: none !important; }
[data-testid="stChatMessage"] { background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; gap: 0 !important; margin-bottom: 1.5rem !important; }
[data-testid="stChatInput"] { border-radius: 18px !important; border: 1px solid rgba(255,255,255,0.05) !important; background: rgba(255,255,255,0.025) !important; backdrop-filter: blur(25px) !important; -webkit-backdrop-filter: blur(25px) !important; transition: all 0.3s ease; }
[data-testid="stChatInput"]:focus-within { border-color: rgba(255,93,93,0.3) !important; box-shadow: 0 0 30px rgba(255,93,93,0.08) !important; }
[data-testid="stChatInput"] textarea { color: #e0e0e0 !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #4a4a55 !important; }
[data-testid="stChatMessage"] [data-testid="stExpander"] { background: rgba(0,150,255,0.03) !important; border: 1px solid rgba(0,150,255,0.08) !important; border-radius: 14px !important; }
.tip-card { background: linear-gradient(135deg, rgba(255,93,93,0.06), rgba(0,150,255,0.04)); border: 1px solid rgba(255,93,93,0.1); border-radius: 16px; padding: 1.2rem; margin-top: 0.5rem; }
.tip-card-title { font-size: 0.85rem; font-weight: 700; color: #ff8a8a; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.8rem; }
.tip-item { color: #9a9aaa; font-size: 0.88rem; line-height: 1.9; padding-left: 0.5rem; border-left: 2px solid rgba(255,93,93,0.15); margin-bottom: 0.4rem; padding-top: 0.1rem; padding-bottom: 0.1rem; }
.tip-item em { color: #c0c0d0; }

/* Document Vault UI */
.vault-header { text-align: center; padding: 2rem 0; animation: fadeUp 0.8s ease; }
.vault-badge { display: inline-block; color: #c0a0ff; font-size: 0.75rem; font-weight: 600; letter-spacing: 3px; padding: 0.35rem 1rem; border-radius: 999px; border: 1px solid rgba(140,80,255,0.2); background: rgba(140,80,255,0.04); margin-bottom: 1.2rem; text-transform: uppercase; }
.vault-title { font-size: 3.2rem; font-weight: 800; letter-spacing: -2px; color: white; text-shadow: 0 0 30px rgba(140,80,255,0.08); }
.vault-subtitle { color: #6a6a75; font-size: 1.05rem; margin-top: 0.7rem; }
.doc-card { background: rgba(255,255,255,0.018); border: 1px solid rgba(255,255,255,0.04); border-radius: 18px; padding: 1.5rem; margin-bottom: 1rem; backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); animation: fadeUp 0.6s ease; }
.doc-card:hover { border-color: rgba(140,80,255,0.25); background: rgba(255,255,255,0.03); box-shadow: 0 15px 40px rgba(140,80,255,0.08); transform: translateY(-4px); }
.doc-name { font-size: 1.15rem; font-weight: 700; color: white; margin-bottom: 0.4rem; }
.doc-meta { display: flex; gap: 0.8rem; margin-top: 0.6rem; }
.meta-badge { font-size: 0.78rem; font-weight: 600; padding: 0.25rem 0.7rem; border-radius: 8px; letter-spacing: 0.5px; }
.badge-chunks { background: rgba(0,200,100,0.08); color: #00cc66; border: 1px solid rgba(0,200,100,0.15); }
.badge-vectors { background: rgba(0,150,255,0.08); color: #4da6ff; border: 1px solid rgba(0,150,255,0.15); }
.badge-type { background: rgba(255,180,50,0.08); color: #ffb432; border: 1px solid rgba(255,180,50,0.15); }
.empty-state { text-align: center; padding: 6rem 2rem; animation: fadeUp 1s ease; }
.empty-icon { font-size: 4rem; margin-bottom: 1.5rem; animation: breathe 3s ease-in-out infinite; }
.empty-title { font-size: 1.5rem; font-weight: 700; color: #aaa; margin-bottom: 0.5rem; }
.empty-text { color: #666; font-size: 1rem; }
.vector-preview { font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.82rem; color: #7a7a8a; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 0.8rem; margin-top: 0.5rem; overflow-x: auto; }
.vector-preview .num { color: #ff8a8a; }
.chunk-preview { color: #9a9aaa; font-size: 0.9rem; line-height: 1.7; background: rgba(255,255,255,0.015); border-left: 3px solid rgba(140,80,255,0.3); padding: 0.8rem 1rem; border-radius: 0 10px 10px 0; margin-top: 0.5rem; }

/* ==========================================
   APP.PY SPECIFIC STYLES (Moved from app.py)
========================================== */

/* Aurora Background */
.stApp::before {
    content: "";
    position: fixed;
    width: 250%;
    height: 250%;
    top: -75%;
    left: -75%;
    background:
        radial-gradient(circle at 20% 30%, rgba(255,80,80,0.12), transparent 25%),
        radial-gradient(circle at 80% 40%, rgba(80,80,255,0.08), transparent 25%),
        radial-gradient(circle at 50% 80%, rgba(255,255,255,0.03), transparent 20%),
        radial-gradient(circle at 70% 20%, rgba(255,120,50,0.06), transparent 20%);
    animation: aurora 40s ease infinite;
    z-index: -20;
    pointer-events: none;
}

/* Grid Overlay */
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    background:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 60px 60px;
    mask-image: radial-gradient(circle, white, transparent 80%);
    z-index: -19;
    pointer-events: none;
}

/* Splash Screen */
.splash-container {
    height: 72vh;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.splash-container::before {
    content: "";
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,93,93,0.08), transparent 60%);
    animation: breathe 4s ease-in-out infinite;
    pointer-events: none;
}

.splash-title {
    font-size: 8rem;
    font-weight: 900;
    letter-spacing: -5px;
    background: linear-gradient(90deg, #ffffff, #bdbdbd, #ffffff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation:
        shimmer 8s linear infinite,
        floatLogo 6s ease-in-out infinite;
    position: relative;
    z-index: 1;
}

/* Hero Section */
.hero-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 800;
    margin-top: 2rem;
    letter-spacing: -2px;
    color: white;
    animation: fadeUp 1s ease;
    text-shadow: 0 0 40px rgba(255,255,255,0.06);
}

.hero-subtitle {
    text-align: center;
    color: #8a8a93;
    font-size: 1.2rem;
    margin-top: 0.8rem;
    margin-bottom: 3rem;
    animation: fadeUp 1.4s ease;
}

/* Feature Cards */
.feature-card {
    position: relative;
    padding: 2rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    min-height: 220px;
    opacity: 0;
    animation: fadeUp 0.8s ease forwards;
}

.feature-card:hover {
    transform: translateY(-12px) scale(1.02);
    border-color: rgba(255,93,93,0.3);
    box-shadow:
        0 20px 60px rgba(255,93,93,0.12),
        0 0 0 1px rgba(255,93,93,0.1),
        inset 0 1px 0 rgba(255,255,255,0.05);
}

.feature-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: -150%;
    width: 120%;
    height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.06), transparent);
    transition: 1s;
}

.feature-card:hover::before {
    left: 150%;
}

.feature-card::after {
    content: "";
    position: absolute;
    left: 0;
    top: -10%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,93,93,0.4), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.feature-card:hover::after {
    opacity: 1;
    animation: scanline 2s linear infinite;
}

.feature-icon {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    animation: textGlow 3s ease infinite;
}

.feature-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
}

.feature-text {
    color: #86868b;
    line-height: 1.8;
    font-size: 0.95rem;
}

/* About Section */
.about-section {
    margin-top: 5rem;
    padding-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    position: relative;
}

.about-section::before {
    content: "";
    position: absolute;
    top: -1px;
    left: 0;
    width: 120px;
    height: 2px;
    background: linear-gradient(90deg, #ff5d5d, transparent);
}

.about-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: white;
}

.about-text {
    font-size: 1.1rem;
    line-height: 1.7;
    color: #86868b;
    max-width: 800px;
}

/* Sidebar Stack Tree */
.stack-tree {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.82rem;
    color: #6a6a75;
    line-height: 2;
    padding: 0.5rem;
    background: rgba(255,255,255,0.015);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.03);
}

.stack-tree .accent {
    color: #ff5d5d;
}

/* Hide sidebar on splash */
.hide-sidebar [data-testid="collapsedControl"] { display: none; }

</style>
"""
