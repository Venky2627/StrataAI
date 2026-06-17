import streamlit as st
from config.settings import APP_TITLE
from src.rag.chain import answer_question

st.set_page_config(page_title=f"Chat - {APP_TITLE}", page_icon="💬")

st.title("Chat with Documents")
st.markdown('<p style="color:#86868b;">Talk directly to your uploaded knowledge base.</p>', unsafe_allow_html=True)

# 1. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display all previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If this message was from the AI and had source chunks, display them!
        if "sources" in message and message["sources"]:
            with st.expander("View Source Documents"):
                for idx, chunk in enumerate(message["sources"]):
                    st.info(f"**Chunk {idx+1}:**\n\n{chunk}")

# 3. Handle New User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 4. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Searching database and thinking..."):
            try:
                # Milestone 2: FULL RAG!
                ai_answer, sources = answer_question(prompt)
                
                # Show the answer
                st.markdown(ai_answer)
                
                # Show the sources in a dropdown expander
                if sources:
                    with st.expander("View Source Documents"):
                        for idx, chunk in enumerate(sources):
                            st.info(f"**Chunk {idx+1}:**\n\n{chunk}")
                
                # Save BOTH the answer and the sources to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_answer,
                    "sources": sources
                })
                
            except Exception as e:
                st.error(f"Error communicating with AI: {str(e)}")
