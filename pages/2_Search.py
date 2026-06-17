import streamlit as st
from config.settings import APP_TITLE
from src.embeddings.generator import generate_embeddings
from src.rag.vectorstore import search_documents

st.set_page_config(page_title=f"Search - {APP_TITLE}", page_icon="⚲")

# Minimal CSS to keep our Apple/Google premium aesthetic
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

st.title("Semantic Search")
st.markdown('<p class="subtext">Ask a question. StrataAI will convert it to math and find the exact chunk containing the answer.</p>', unsafe_allow_html=True)

# The user types their question here
query = st.text_input("Enter your search query (e.g., 'What is this document about?'):")

# We only run the search if the user pressed Enter or the button
if query:
    if st.button("Search Database", type="primary"):
        with st.spinner("Converting query to math and scanning database..."):
            
            # 1. Convert English query into a 384-dimension vector
            # generate_embeddings expects a list of strings, so we wrap query in brackets
            # It returns a list of lists, so we grab the first item [0]
            query_vector = generate_embeddings([query])[0]
            
            # 2. Ask ChromaDB to find the 3 closest math vectors!
            results = search_documents(query_vector, n_results=3)
            
            # 3. Display the results beautifully
            if not results['documents'][0]:
                st.warning("No documents found in the database. Did you upload a PDF first?")
            else:
                st.success("Found matching chunks!")
                
                # Chroma returns lists of lists. We grab the inner lists.
                chunks = results['documents'][0]
                metadata = results['metadatas'][0]
                distances = results['distances'][0]
                
                for i in range(len(chunks)):
                    # Distance: 0.0 is a perfect identical match. 1.0+ is completely unrelated.
                    st.markdown(f"### Result {i+1}")
                    st.markdown(f"**Source File:** `{metadata[i]['source']}` | **Math Distance:** `{distances[i]:.4f}`")
                    st.info(chunks[i])
