import streamlit as st
import time
from config.settings import APP_TITLE, UPLOAD_DIR
from src.pdf.extractor import extract_text_from_pdf
from src.rag.chunker import chunk_text
from src.embeddings.generator import generate_embeddings
from src.rag.vectorstore import store_documents

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
                    chunks = chunk_text(text)
                    
                    # Update spinner text so the user knows what's happening
                    embeddings = generate_embeddings(chunks)
                    
                    # --- NEW: Save permanently to ChromaDB! ---
                    store_documents(file.name, chunks, embeddings)
                    
                    if "documents" not in st.session_state:
                        st.session_state.documents = {}
                        
                    # Save the text, chunks, AND embeddings
                    st.session_state.documents[file.name] = {
                        "text": text,
                        "chunks": chunks,
                        "embeddings": embeddings
                    }
                    success_count += 1
                    
                except Exception as e:
                    st.error(f"Failed to process {file.name}: {str(e)}")
            
            if success_count > 0:
                st.success(f"Successfully processed {success_count} document(s).")
                
                st.markdown("### Processing Summary")
                
                for filename, data in st.session_state.documents.items():
                    num_chunks = len(data['chunks'])
                    vector_length = len(data['embeddings'][0]) if num_chunks > 0 else 0
                    
                    with st.expander(f"📄 {filename} ({num_chunks} chunks generated)"):
                        st.markdown("**1. Text Chunk Preview:**")
                        st.text(data['chunks'][0] + "...\n")
                        
                        st.markdown("**2. Mathematical Embedding (Vector) Preview:**")
                        st.markdown(f"*(This chunk was converted into exactly **{vector_length}** numbers! Here are the first 5...)*")
                        
                        # Show just the first 5 numbers of the 384-dimensional vector so we don't spam the screen
                        first_5_numbers = [round(num, 4) for num in data['embeddings'][0][:5]]
                        st.code(str(first_5_numbers) + " ... ]", language="python")
