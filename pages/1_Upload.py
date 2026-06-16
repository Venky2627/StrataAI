import streamlit as st
import time
from config.settings import APP_TITLE, UPLOAD_DIR
from src.pdf.extractor import extract_text_from_pdf

# Configure the page
st.set_page_config(page_title=f"Upload - {APP_TITLE}", page_icon="❖")

# Inject minimal CSS for this page
st.markdown("""
<style>
    /* Minimalist Typography */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .subtext {
        color: #86868b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    /* Style the expander */
    .streamlit-expanderHeader {
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Upload Documents</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtext">Select and upload your PDF materials for processing.</p>', unsafe_allow_html=True)

# ============================================================================
# FILE UPLOADER WIDGET
# ============================================================================
uploaded_files = st.file_uploader(
    "Drag and drop files", 
    type=["pdf"], 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Only run extraction if the user has actually uploaded files
if uploaded_files:
    if st.button("Process Documents", type="primary"):
        
        with st.spinner("Extracting text..."):
            success_count = 0
            
            for file in uploaded_files:
                try:
                    raw_bytes = file.read()
                    text = extract_text_from_pdf(raw_bytes)
                    
                    if "documents" not in st.session_state:
                        st.session_state.documents = {}
                        
                    st.session_state.documents[file.name] = text
                    success_count += 1
                    
                except Exception as e:
                    st.error(f"Failed to process {file.name}: {str(e)}")
            
            if success_count > 0:
                st.success(f"Successfully processed {success_count} document(s).")
                
                st.markdown("### Extraction Preview")
                
                for filename, content in st.session_state.documents.items():
                    with st.expander(f"Preview: {filename}"):
                        st.text(content[:500] + "...\n\n[Text truncated]")
