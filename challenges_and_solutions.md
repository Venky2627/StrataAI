# StrataAI: Challenges & Solutions Log

This document tracks the technical challenges encountered during the development of StrataAI and the architectural solutions implemented to counter them. This will serve as the foundation for the final Project Report.

## Week 1: The Streamlit "Goldfish" Curse
**Challenge:** Streamlit is designed as a stateless data-dashboard framework. Every time a user interacts with a button or input, the entire Python script reruns from top to bottom, wiping out variables.
**Solution:** Implemented `st.session_state` to create a persistent memory "backpack" that survives reruns. This allowed us to keep the user's "entered" state and later track the Chat History without it wiping every time they hit enter.

## Week 2: The Context Window Fragmentation
**Challenge:** When chunking PDFs, breaking text strictly by character count often splits sentences or critical paragraphs right down the middle, destroying the semantic meaning for the AI.
**Solution:** Implemented LangChain's `RecursiveCharacterTextSplitter` with an explicit `chunk_overlap` of 200 characters. This ensures the ending of one chunk overlaps with the beginning of the next, preserving the context of long sentences.

## Week 4: The Robotic "Syllabus" RAG Response
**Challenge:** When the user asked a conceptual question ("What is probability?"), the AI refused to answer because the retrieved PDF chunk only listed it as a syllabus topic without defining it. The System Prompt was too strict ("Your ONLY job is to answer from the text").
**Solution:** Prompt Engineering. We relaxed the constraints and assigned a new persona: "Expert Tutor". The prompt now instructs the AI to prioritize the text, but explicitly allows it to use its own knowledge to teach concepts if the document only mentions them briefly.

## Week 4: API Quota Exhaustion (Model Deprecation)
**Challenge:** Received a `429 RESOURCE_EXHAUSTED` limit 0 error when attempting to call `gemini-2.0-flash`. 
**Solution:** Pushed an architectural configuration change in `config/settings.py` to target `gemini-2.5-flash`, which is actively supported and provides generous free-tier limits on the newly generated API key format (`AQ.`).
